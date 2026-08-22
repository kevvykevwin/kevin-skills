# Kevin Skills

## Recovery
After compaction or session start:
- Read this file and `README.md`.
- Check `git status --short --branch` before editing.
- Inspect the target skill or script before making changes.

## Commands
- Python helper validation: `pytest`
- Python lint: `ruff check`

## Testing
- No centralized test suite is currently defined.
- For script changes, prefer focused CLI/import checks that exercise the changed path.

## Structure
- `.claude-plugin/`: Claude Code plugin metadata.
- `skills/`: installable Claude Code skills and bundled references/scripts.
- Top-level skill folders: legacy or standalone skill content.

## Conventions
- Keep changes scoped to the relevant skill or helper script.
- Do not write generated caches or local config into the repository.
- Preserve plugin skill layout and avoid new top-level directories unless the README structure changes.
