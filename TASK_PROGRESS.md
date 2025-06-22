# SSI Project - Task Progress

This file tracks the progress of major development milestones for the Software Stability Index.

- `[ ]` To Do
- `[-]` In Progress
- `[v]` Completed
- `[x]` Failed or Blocked

---

## Milestone 1: Initial Scaffolding & Core Logic

-   `[v]` Set up `feature/ssi-development` branch.
-   `[v]` Create `DEVELOPMENT_PLAN.md`.
-   `[v]` Create `TASK_PROGRESS.md` and add to `.gitignore`.
-   `[v]` Create `docs/` for `learnability.md`, `applicability.md`, and `sustainability.md`.
-   `[v]` Populate `docs/` with metric definitions.
-   `[v]` Create `examples/sample_scores.json` with initial data.
-   `[v]` Implement `scoring/compute_ssi.py` to calculate scores from the sample file.
-   `[v]` Define stability bands (e.g., Ultra-stable, Stable) in the scoring script.

## Milestone 2: Data Collection - Registries & APIs

-   `[v]` **Module: `fetch-registry-stats`**
    -   `[v]` Implement PyPI client to fetch package metadata.
    -   `[v]` Implement npm client to fetch package metadata.
    -   `[v]` Implement Packagist client to fetch package metadata.
-   `[-]` **Module: `issue-tracker-scanner`**
    -   `[ ]` Implement GitHub API client to fetch issue data (backlog, MTTR).

## Milestone 3: Advanced Analysis Modules

-   `[ ]` **Module: `release-diff-analyzer`**
    -   `[ ]` Research AST diffing libraries for Python/Go/Rust.
    -   `[ ]` Implement prototype for detecting breaking changes between versions.
-   `[ ]` **Module: `qa-freshness-auditor`**
    -   `[ ]` Design a prompt test bank for evaluating LLM answer freshness.

## Milestone 4: CI & Publishing

-   `[ ]` **Module: `index-aggregator`**
    -   `[ ]` Refine the aggregation formula and weights.
-   `[ ]` **Module: `snapshot-publisher`**
    -   `[ ]` Generate a markdown report of the latest SSI scores.
    -   `[ ]` Create a GitHub Action to run the full pipeline monthly. 