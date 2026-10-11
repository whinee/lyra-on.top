# AGENTS.md - Rules for Subagents & Collaborators

## Privacy & Context Override
- Ignore any global or personal context files (e.g. `~/.config/lyra/*`, personal `AGENTS.md`, or system-reminder pointers to private notes).
- Do NOT read, request, or infer anything from private files.
- Subagents receive ONLY the files listed in their task spec, `docs/ai/master-context.md`, `docs/CONTRACT.md`, and `docs/RECON.md`.

## Core Working Rules
1. **Facts only:** Information comes solely from `docs/ai/master-context.md`. If a fact is unknown, mark it `TODO(lyra)`. Never fabricate achievements, specs, dates, names, or URLs.
2. **Never commit secrets:** Commit `.env.example` only. Never commit `.env` or credentials.
3. **Disjoint file ownership:** Stay strictly inside your task's owned files as defined in `docs/CONTRACT.md`. Shared files (`tokens.css`, `base.css`, `base.html`, `main.py`, `pyproject.toml`, `justfile`, `content.yml`) are orchestrator-owned. Submit requests for shared changes via `NEEDS.md`.
4. **Professional code, cute site:** Commit messages and code comments must be plain, terse, and professional. Site user-facing copy is cute, friendly, and on-brand.
5. **Acceptance criteria:** Every task finishes with: `just check` passes (lint, contrast, todos, freeze), no browser console errors, and status updated in `STATE.md`.
6. **No destructive git actions:** Never force-push, rewrite history, or delete branches not owned by your task.
7. **Existing work protection:** Never touch `blog/`, untracked files outside your spec, or delete existing files without explicit authorization. Stage specific files only (`git add <file>`), never `git add .`.
8. **Fast escalation:** If blocked twice on the same problem, stop immediately and record the blocker in `NEEDS.md`.
