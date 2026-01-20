#!/usr/bin/env python3
"""
Adversarial Spec Debate CLI

Run multi-model debates to refine product specifications through structured critique.
"""

import sys
import argparse
import difflib
from pathlib import Path
from datetime import datetime

from prompts import get_doc_type_name
from providers import (
    list_providers,
    list_profiles,
    list_focus_areas,
    list_personas,
    load_profile,
    save_profile,
    handle_bedrock_command,
)
from models import (
    CostTracker,
    run_critique_round,
    export_tasks_from_spec,
)
from session import SessionState, save_checkpoint

# Try to import telegram support
try:
    from telegram_bot import is_configured as telegram_configured, send_message, notify_and_wait
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    telegram_configured = lambda: False


def print_response_summary(responses, round_num: int):
    """Print a summary of model responses."""
    print(f"\n{'='*60}")
    print(f"Round {round_num} Results:")
    print(f"{'='*60}")

    for r in responses:
        status = "[AGREE]" if r.agrees else "[CRITIQUE]"
        if r.error:
            status = f"[ERROR: {r.error[:50]}...]" if len(r.error) > 50 else f"[ERROR: {r.error}]"

        cost_str = f"${r.cost:.4f}" if r.cost > 0 else "n/a"
        tokens_str = f"{r.input_tokens:,}in/{r.output_tokens:,}out" if r.input_tokens else "n/a"

        print(f"\n{r.model}: {status}")
        print(f"  Tokens: {tokens_str}, Cost: {cost_str}")

        if not r.error and not r.agrees:
            # Show first few lines of critique
            lines = r.critique.split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"  > {line[:80]}...")
                    break


def run_debate(args):
    """Run the main debate loop."""
    # Load spec from stdin or file
    if args.file:
        spec = Path(args.file).read_text()
    else:
        spec = sys.stdin.read()

    if not spec.strip():
        print("Error: No specification provided", file=sys.stderr)
        sys.exit(1)

    # Parse models
    models = [m.strip() for m in args.models.split(',')]

    # Initialize cost tracker
    cost_tracker = CostTracker()

    # Session management
    session = None
    if args.session:
        session = SessionState(
            session_id=args.session,
            spec=spec,
            round=0,
            doc_type=args.doc_type,
            models=models,
            focus=args.focus,
            persona=args.persona,
            preserve_intent=args.preserve_intent,
            created_at=datetime.now().isoformat(),
        )

    # Context files
    context_files = None
    if args.context:
        context_files = [c.strip() for c in args.context.split(',')]

    print(f"Starting adversarial spec debate")
    print(f"  Document type: {get_doc_type_name(args.doc_type)}")
    print(f"  Models: {', '.join(models)}")
    if args.focus:
        print(f"  Focus: {args.focus}")
    if args.persona:
        print(f"  Persona: {args.persona}")
    if args.preserve_intent:
        print(f"  Preserve intent: enabled")
    print()

    current_spec = spec
    round_num = 0
    max_rounds = args.max_rounds or 10

    while round_num < max_rounds:
        round_num += 1

        # Save checkpoint
        save_checkpoint(current_spec, round_num, args.session)

        # Determine if we should press for confirmation
        press = args.press or (round_num <= 2)

        # Run critique round
        responses, revised_spec = run_critique_round(
            spec=current_spec,
            models=models,
            doc_type=args.doc_type,
            round_num=round_num,
            focus=args.focus,
            persona=args.persona,
            context_files=context_files,
            preserve_intent=args.preserve_intent,
            press=press and round_num > 1,
            cost_tracker=cost_tracker,
        )

        # Print summary
        print_response_summary(responses, round_num)

        # Check for errors
        errors = [r for r in responses if r.error]
        if len(errors) == len(responses):
            print("\nAll models returned errors. Aborting.", file=sys.stderr)
            sys.exit(1)

        # Check for consensus
        valid_responses = [r for r in responses if not r.error]
        all_agree = all(r.agrees for r in valid_responses)

        if all_agree:
            print(f"\n{'='*60}")
            print("CONSENSUS REACHED!")
            print(f"{'='*60}")
            print(f"All {len(valid_responses)} model(s) agree the spec is production-ready.")
            print()
            print(cost_tracker.summary())
            break

        # Update spec with revisions
        if revised_spec:
            current_spec = revised_spec
            print(f"\nSpec updated based on critiques. Continuing to round {round_num + 1}...")
        else:
            # No revisions but no agreement - use the first non-agreeing response's spec
            for r in valid_responses:
                if r.spec:
                    current_spec = r.spec
                    break

        # Update session
        if session:
            session.spec = current_spec
            session.round = round_num
            session.history.append({
                "round": round_num,
                "agreements": sum(1 for r in valid_responses if r.agrees),
                "total": len(valid_responses),
            })
            session.save()

        # Telegram notification (optional)
        if args.telegram and telegram_configured():
            msg = f"Round {round_num} complete. {sum(1 for r in valid_responses if r.agrees)}/{len(valid_responses)} models agree."
            result = notify_and_wait(msg, timeout=60)
            if result.get("response"):
                print(f"\nUser feedback: {result['response']}")

    else:
        print(f"\nMax rounds ({max_rounds}) reached without consensus.", file=sys.stderr)
        print(cost_tracker.summary())

    # Output final spec
    print(f"\n{'='*60}")
    print("FINAL SPECIFICATION:")
    print(f"{'='*60}\n")
    print(current_spec)

    # Save to file
    output_file = "tech-spec-output.md" if args.doc_type == "tech" else "spec-output.md"
    Path(output_file).write_text(current_spec)
    print(f"\nSaved to: {output_file}")


def run_resume(args):
    """Resume a saved session."""
    try:
        session = SessionState.load(args.resume)
    except FileNotFoundError:
        print(f"Error: Session '{args.resume}' not found", file=sys.stderr)
        sys.exit(1)

    print(f"Resuming session: {session.session_id}")
    print(f"  Round: {session.round}")
    print(f"  Doc type: {session.doc_type}")
    print(f"  Models: {', '.join(session.models)}")

    # Create args from session
    class SessionArgs:
        pass

    resume_args = SessionArgs()
    resume_args.models = ','.join(session.models)
    resume_args.doc_type = session.doc_type
    resume_args.focus = session.focus
    resume_args.persona = session.persona
    resume_args.preserve_intent = session.preserve_intent
    resume_args.context = None
    resume_args.session = session.session_id
    resume_args.press = args.press
    resume_args.max_rounds = args.max_rounds
    resume_args.telegram = args.telegram
    resume_args.file = None

    # Inject the spec via stdin simulation
    import io
    sys.stdin = io.StringIO(session.spec)

    run_debate(resume_args)


def run_diff(args):
    """Show diff between two spec versions."""
    if not args.previous or not args.current:
        print("Error: --previous and --current are required", file=sys.stderr)
        sys.exit(1)

    previous = Path(args.previous).read_text().splitlines(keepends=True)
    current = Path(args.current).read_text().splitlines(keepends=True)

    diff = difflib.unified_diff(
        previous,
        current,
        fromfile=args.previous,
        tofile=args.current,
    )

    print(''.join(diff))


def run_export_tasks(args):
    """Export tasks from a spec."""
    if args.file:
        spec = Path(args.file).read_text()
    else:
        spec = sys.stdin.read()

    if not spec.strip():
        print("Error: No specification provided", file=sys.stderr)
        sys.exit(1)

    result = export_tasks_from_spec(
        spec=spec,
        doc_type=args.doc_type,
        model=args.model or "gpt-4o",
        output_json=args.json,
    )

    print(result)


def run_save_profile(args):
    """Save a debate profile."""
    if not args.profile_name:
        print("Error: Profile name required", file=sys.stderr)
        sys.exit(1)

    config = {}
    if args.models:
        config["models"] = args.models
    if args.doc_type:
        config["doc_type"] = args.doc_type
    if args.focus:
        config["focus"] = args.focus
    if args.persona:
        config["persona"] = args.persona
    if args.preserve_intent:
        config["preserve_intent"] = True

    save_profile(args.profile_name, config)


def list_sessions():
    """List all saved sessions."""
    sessions = SessionState.list_sessions()

    if not sessions:
        print("No saved sessions found.")
        return

    print("Saved Sessions:\n")
    for s in sessions:
        print(f"  {s['id']}")
        print(f"    Round: {s['round']}, Type: {s['doc_type']}")
        print(f"    Updated: {s['updated_at']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Adversarial spec debate CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic critique
  cat spec.md | python3 debate.py critique --models gpt-4o --doc-type tech

  # Multi-model with focus
  python3 debate.py critique --models gpt-4o,gemini/gemini-2.0-flash --doc-type prd --focus security < spec.md

  # Resume a session
  python3 debate.py critique --resume my-session

  # Check providers
  python3 debate.py providers
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Critique command
    critique_parser = subparsers.add_parser("critique", help="Run critique debate")
    critique_parser.add_argument("--models", "-m", help="Comma-separated list of models")
    critique_parser.add_argument("--doc-type", "-t", choices=["prd", "tech"], default="tech", help="Document type")
    critique_parser.add_argument("--focus", "-f", help="Focus area (security, scalability, performance, ux, reliability, cost)")
    critique_parser.add_argument("--persona", "-p", help="Reviewer persona")
    critique_parser.add_argument("--context", "-c", help="Comma-separated context files")
    critique_parser.add_argument("--preserve-intent", action="store_true", help="Require justification for removals")
    critique_parser.add_argument("--session", "-s", help="Session name for persistence")
    critique_parser.add_argument("--resume", "-r", help="Resume a saved session")
    critique_parser.add_argument("--profile", help="Load settings from a saved profile")
    critique_parser.add_argument("--press", action="store_true", help="Press for thorough review confirmation")
    critique_parser.add_argument("--max-rounds", type=int, default=10, help="Maximum debate rounds")
    critique_parser.add_argument("--telegram", action="store_true", help="Enable Telegram notifications")
    critique_parser.add_argument("--file", help="Read spec from file instead of stdin")

    # Providers command
    subparsers.add_parser("providers", help="List available providers and API key status")

    # Profiles command
    subparsers.add_parser("profiles", help="List saved profiles")

    # Focus areas command
    subparsers.add_parser("focus-areas", help="List available focus areas")

    # Personas command
    subparsers.add_parser("personas", help="List available personas")

    # Sessions command
    subparsers.add_parser("sessions", help="List saved sessions")

    # Save profile command
    save_profile_parser = subparsers.add_parser("save-profile", help="Save a debate profile")
    save_profile_parser.add_argument("profile_name", help="Profile name")
    save_profile_parser.add_argument("--models", "-m", help="Models to save")
    save_profile_parser.add_argument("--doc-type", "-t", choices=["prd", "tech"], help="Document type")
    save_profile_parser.add_argument("--focus", "-f", help="Focus area")
    save_profile_parser.add_argument("--persona", "-p", help="Persona")
    save_profile_parser.add_argument("--preserve-intent", action="store_true", help="Preserve intent mode")

    # Diff command
    diff_parser = subparsers.add_parser("diff", help="Show diff between spec versions")
    diff_parser.add_argument("--previous", help="Previous spec file")
    diff_parser.add_argument("--current", help="Current spec file")

    # Export tasks command
    export_parser = subparsers.add_parser("export-tasks", help="Extract tasks from a spec")
    export_parser.add_argument("--doc-type", "-t", choices=["prd", "tech"], default="tech", help="Document type")
    export_parser.add_argument("--model", "-m", default="gpt-4o", help="Model to use for extraction")
    export_parser.add_argument("--json", action="store_true", help="Output as JSON")
    export_parser.add_argument("--file", help="Read spec from file instead of stdin")

    # Bedrock command
    bedrock_parser = subparsers.add_parser("bedrock", help="Manage AWS Bedrock configuration")
    bedrock_parser.add_argument("subcommand", choices=["status", "enable", "disable", "add-model", "remove-model", "alias", "list-models"], help="Bedrock subcommand")
    bedrock_parser.add_argument("arg", nargs="?", help="Argument for subcommand")
    bedrock_parser.add_argument("--region", help="AWS region for Bedrock")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "providers":
        list_providers()

    elif args.command == "profiles":
        list_profiles()

    elif args.command == "focus-areas":
        list_focus_areas()

    elif args.command == "personas":
        list_personas()

    elif args.command == "sessions":
        list_sessions()

    elif args.command == "save-profile":
        run_save_profile(args)

    elif args.command == "diff":
        run_diff(args)

    elif args.command == "export-tasks":
        run_export_tasks(args)

    elif args.command == "bedrock":
        handle_bedrock_command(args.subcommand, args.arg, args.region)

    elif args.command == "critique":
        # Handle resume
        if args.resume:
            run_resume(args)
            return

        # Load profile if specified
        if args.profile:
            profile = load_profile(args.profile)
            args.models = args.models or profile.get("models")
            args.doc_type = args.doc_type or profile.get("doc_type", "tech")
            args.focus = args.focus or profile.get("focus")
            args.persona = args.persona or profile.get("persona")
            args.preserve_intent = args.preserve_intent or profile.get("preserve_intent", False)

        # Validate required args
        if not args.models:
            print("Error: --models is required", file=sys.stderr)
            print("Example: --models gpt-4o,gemini/gemini-2.0-flash", file=sys.stderr)
            sys.exit(1)

        run_debate(args)


if __name__ == "__main__":
    main()
