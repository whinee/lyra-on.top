# AI Agent Artifact Home: docs/ai/

Canonical home for all documents produced by or for AI agents during the `lyra-on.top` build.

## Directory Structure

```
docs/ai/
  README.md              Index of all AI documents and purposes
  master-context.md      Single source of truth for facts, brand, voice, palette, stack
  orchestrator-prompt.md Orchestration specification and execution rules
  STATE.md               Task ledger and state tracking
  NEEDS.md               Batch requests from workers to orchestrator
  RECON.md               Repository reconnaissance and codebase decisions
  CONTRACT.md            File ownership and component boundaries
  MOTION.md              Motion budget and animation invariants
  DEPLOY.md              Cloudflare Pages deployment guide
  WORKER.md              Cloudflare Python Worker architecture and deploy guide
  tasks/                 Self-contained task specs (<ID>.md)
  issues/                QA findings and defect logs
  reports/               Automated test reports and performance benchmarks
  inputs/                Source art (doodle PNGs) and palette assets
  archive/               Superseded documents (master-context.old.md, OLD-VS-NEW.md)
```

## Inventory of Files

| File | Purpose | Origin |
|---|---|---|
| `master-context.md` | Canonical specification of brand, facts, tokens, routes, content models | Kit |
| `orchestrator-prompt.md` | Master orchestration rules and execution schedule | Kit |
| `README.md` | Index of all documents | Orchestrator |
| `STATE.md` | Task execution ledger, branch mapping, commit history | Orchestrator |
| `CONTRACT.md` | Disjoint file ownership contract per component | Pre-existing (migrated) |
| `RECON.md` | Architectural baseline and codebase inventory | Pre-existing (migrated) |
| `DEPLOY.md` | Cloudflare Pages static deploy runbook | Pre-existing (migrated) |
| `archive/master-context.old.md` | Byte-for-byte archived previous master context | Step -1 Relocation |
| `archive/OLD-VS-NEW.md` | Detailed diff of changes and decisions between old and new master context | Step -1 Relocation |
| `inputs/lyra-doodle-transparent.png` | Source character artwork | Moved from `assets/` |
| `inputs/lyra-doodle-original.png` | Source character artwork with background | Moved from `assets/` |
