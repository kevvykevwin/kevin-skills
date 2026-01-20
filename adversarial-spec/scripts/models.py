"""Model calling utilities for adversarial spec debate."""

import os
import re
import sys
import json
import time
import subprocess
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import litellm
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False

from prompts import (
    PRESERVE_INTENT_PROMPT,
    FOCUS_AREAS,
    REVIEW_PROMPT_TEMPLATE,
    PRESS_PROMPT_TEMPLATE,
    EXPORT_TASKS_PROMPT,
    get_system_prompt,
    get_doc_type_name,
)
from providers import (
    MODEL_COSTS,
    DEFAULT_COST,
    CODEX_AVAILABLE,
    DEFAULT_CODEX_REASONING,
    is_bedrock_enabled,
    get_bedrock_config,
    resolve_bedrock_model,
)


@dataclass
class ModelResponse:
    """Response from a model critique."""
    model: str
    agrees: bool
    critique: str
    spec: Optional[str] = None
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0
    error: Optional[str] = None


@dataclass
class CostTracker:
    """Track costs across multiple model calls."""
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    by_model: dict = field(default_factory=dict)

    def add(self, model: str, input_tokens: int, output_tokens: int, cost: float):
        """Add usage from a model call."""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost += cost

        if model not in self.by_model:
            self.by_model[model] = {"input": 0, "output": 0, "cost": 0.0}
        self.by_model[model]["input"] += input_tokens
        self.by_model[model]["output"] += output_tokens
        self.by_model[model]["cost"] += cost

    def summary(self) -> str:
        """Return a summary string of costs."""
        lines = ["Cost Summary:"]
        for model, data in self.by_model.items():
            lines.append(f"  {model}: {data['input']:,} in / {data['output']:,} out = ${data['cost']:.4f}")
        lines.append(f"  Total: {self.total_input_tokens:,} in / {self.total_output_tokens:,} out = ${self.total_cost:.4f}")
        return "\n".join(lines)


def load_context_files(context_paths: list[str]) -> str:
    """Load and concatenate context files."""
    if not context_paths:
        return ""

    sections = []
    for path in context_paths:
        p = Path(path)
        if not p.exists():
            print(f"Warning: Context file not found: {path}", file=sys.stderr)
            continue
        content = p.read_text()
        sections.append(f"### Context: {p.name}\n\n{content}")

    if not sections:
        return ""

    return "**Additional Context:**\n\n" + "\n\n".join(sections) + "\n\n"


def parse_response(response_text: str) -> tuple[bool, Optional[str]]:
    """
    Parse a model response to extract agreement status and spec.

    Returns (agrees, spec_content).
    """
    agrees = "[AGREE]" in response_text

    # Extract spec between [SPEC] and [/SPEC] tags
    spec_match = re.search(r'\[SPEC\](.*?)\[/SPEC\]', response_text, re.DOTALL)
    spec = spec_match.group(1).strip() if spec_match else None

    return agrees, spec


def parse_tasks(response_text: str) -> list[dict]:
    """Extract tasks from a response."""
    tasks = []
    task_pattern = re.compile(r'\[TASK\](.*?)\[/TASK\]', re.DOTALL)

    for match in task_pattern.finditer(response_text):
        task_text = match.group(1).strip()
        task = {}

        # Parse fields
        for line in task_text.split('\n'):
            line = line.strip()
            if line.startswith('title:'):
                task['title'] = line[6:].strip()
            elif line.startswith('type:'):
                task['type'] = line[5:].strip()
            elif line.startswith('priority:'):
                task['priority'] = line[9:].strip()
            elif line.startswith('description:'):
                task['description'] = line[12:].strip()
            elif line.startswith('acceptance_criteria:'):
                task['acceptance_criteria'] = []
            elif line.startswith('- ') and 'acceptance_criteria' in task:
                task['acceptance_criteria'].append(line[2:])

        if task.get('title'):
            tasks.append(task)

    return tasks


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate cost for a model call."""
    costs = MODEL_COSTS.get(model, DEFAULT_COST)
    input_cost = (input_tokens / 1_000_000) * costs["input"]
    output_cost = (output_tokens / 1_000_000) * costs["output"]
    return input_cost + output_cost


def call_codex_model(
    model: str,
    system_prompt: str,
    user_prompt: str,
    reasoning: str = DEFAULT_CODEX_REASONING,
    timeout: int = 600,
) -> ModelResponse:
    """Call a model via Codex CLI."""
    if not CODEX_AVAILABLE:
        return ModelResponse(
            model=model,
            agrees=False,
            critique="",
            error="Codex CLI not installed. Run: npm install -g @openai/codex && codex login"
        )

    # Extract the model name after codex/
    codex_model = model.replace("codex/", "")

    # Build the prompt
    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    try:
        result = subprocess.run(
            [
                "codex",
                "--model", codex_model,
                "--reasoning-effort", reasoning,
                "--output-format", "json",
                "--prompt", full_prompt,
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            return ModelResponse(
                model=model,
                agrees=False,
                critique="",
                error=f"Codex CLI error: {result.stderr}"
            )

        # Parse JSON output
        try:
            output = json.loads(result.stdout)
            response_text = output.get("response", result.stdout)
        except json.JSONDecodeError:
            response_text = result.stdout

        agrees, spec = parse_response(response_text)

        return ModelResponse(
            model=model,
            agrees=agrees,
            critique=response_text,
            spec=spec,
            input_tokens=0,  # Codex doesn't report tokens
            output_tokens=0,
            cost=0.0,  # Included in ChatGPT subscription
        )

    except subprocess.TimeoutExpired:
        return ModelResponse(
            model=model,
            agrees=False,
            critique="",
            error=f"Codex CLI timed out after {timeout}s"
        )
    except Exception as e:
        return ModelResponse(
            model=model,
            agrees=False,
            critique="",
            error=f"Codex CLI error: {str(e)}"
        )


def call_single_model(
    model: str,
    system_prompt: str,
    user_prompt: str,
    timeout: int = 600,
    max_retries: int = 3,
) -> ModelResponse:
    """Call a single model via litellm."""
    if not LITELLM_AVAILABLE:
        return ModelResponse(
            model=model,
            agrees=False,
            critique="",
            error="litellm not installed. Run: pip install litellm"
        )

    # Handle Codex CLI models
    if model.startswith("codex/"):
        return call_codex_model(model, system_prompt, user_prompt)

    # Handle Bedrock routing
    actual_model = model
    if is_bedrock_enabled():
        bedrock_config = get_bedrock_config()
        resolved = resolve_bedrock_model(model, bedrock_config)
        if resolved:
            region = bedrock_config.get("region", "us-east-1")
            actual_model = f"bedrock/{resolved}"
            os.environ["AWS_REGION"] = region

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    for attempt in range(max_retries):
        try:
            response = litellm.completion(
                model=actual_model,
                messages=messages,
                timeout=timeout,
            )

            response_text = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens if response.usage else 0
            output_tokens = response.usage.completion_tokens if response.usage else 0

            agrees, spec = parse_response(response_text)
            cost = calculate_cost(model, input_tokens, output_tokens)

            return ModelResponse(
                model=model,
                agrees=agrees,
                critique=response_text,
                spec=spec,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
            )

        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"  {model}: Error, retrying in {wait_time}s... ({e})", file=sys.stderr)
                time.sleep(wait_time)
            else:
                return ModelResponse(
                    model=model,
                    agrees=False,
                    critique="",
                    error=str(e),
                )


def call_models_parallel(
    models: list[str],
    system_prompt: str,
    user_prompt: str,
    timeout: int = 600,
) -> list[ModelResponse]:
    """Call multiple models in parallel."""
    responses = []

    with ThreadPoolExecutor(max_workers=len(models)) as executor:
        future_to_model = {
            executor.submit(call_single_model, model, system_prompt, user_prompt, timeout): model
            for model in models
        }

        for future in as_completed(future_to_model):
            model = future_to_model[future]
            try:
                response = future.result()
                responses.append(response)
            except Exception as e:
                responses.append(ModelResponse(
                    model=model,
                    agrees=False,
                    critique="",
                    error=str(e),
                ))

    return responses


def run_critique_round(
    spec: str,
    models: list[str],
    doc_type: str,
    round_num: int,
    focus: Optional[str] = None,
    persona: Optional[str] = None,
    context_files: Optional[list[str]] = None,
    preserve_intent: bool = False,
    press: bool = False,
    cost_tracker: Optional[CostTracker] = None,
) -> tuple[list[ModelResponse], Optional[str]]:
    """
    Run a single round of critique.

    Returns (responses, best_spec) where best_spec is the most recent revised spec,
    or None if all models agreed.
    """
    # Build system prompt
    system_prompt = get_system_prompt(doc_type, persona)
    if preserve_intent:
        system_prompt = system_prompt + "\n\n" + PRESERVE_INTENT_PROMPT

    # Build context section
    context_section = ""
    if context_files:
        context_section = load_context_files(context_files)

    # Build focus section
    focus_section = ""
    if focus and focus in FOCUS_AREAS:
        focus_section = FOCUS_AREAS[focus] + "\n\n"

    # Build user prompt
    doc_type_name = get_doc_type_name(doc_type)

    if press:
        user_prompt = PRESS_PROMPT_TEMPLATE.format(
            round=round_num,
            doc_type_name=doc_type_name,
            spec=spec,
            context_section=context_section,
        )
    else:
        user_prompt = REVIEW_PROMPT_TEMPLATE.format(
            round=round_num,
            doc_type_name=doc_type_name,
            spec=spec,
            context_section=context_section,
            focus_section=focus_section,
        )

    # Call models
    print(f"\nRound {round_num}: Calling {len(models)} model(s)...", file=sys.stderr)
    responses = call_models_parallel(models, system_prompt, user_prompt)

    # Track costs
    if cost_tracker:
        for r in responses:
            if not r.error:
                cost_tracker.add(r.model, r.input_tokens, r.output_tokens, r.cost)

    # Find the best (most recent) revised spec
    best_spec = None
    for r in responses:
        if r.spec and not r.agrees:
            best_spec = r.spec

    return responses, best_spec


def export_tasks_from_spec(
    spec: str,
    doc_type: str,
    model: str = "gpt-4o",
    output_json: bool = False,
) -> str:
    """Extract tasks from a spec using a model."""
    doc_type_name = get_doc_type_name(doc_type)
    prompt = EXPORT_TASKS_PROMPT.format(
        doc_type_name=doc_type_name,
        spec=spec,
    )

    response = call_single_model(
        model=model,
        system_prompt="You are a project manager extracting tasks from specifications.",
        user_prompt=prompt,
    )

    if response.error:
        return f"Error: {response.error}"

    if output_json:
        tasks = parse_tasks(response.critique)
        return json.dumps(tasks, indent=2)

    return response.critique
