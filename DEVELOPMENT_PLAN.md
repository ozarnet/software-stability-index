# Software Stability Index (SSI) - Development Plan

This document outlines the modular implementation plan for the Software Stability Index (SSI) project. The goal is to create a reproducible, data-driven system for scoring the stability of software development technologies.

## Core Modules

The implementation is broken down into the following modules. Each module is responsible for a specific part of the data gathering and analysis pipeline.

| Module                    | Description                                                                                             | Metrics Covered         |
| ------------------------- | ------------------------------------------------------------------------------------------------------- | ----------------------- |
| `fetch-registry-stats`    | Gathers package information (e.g., release velocity, download health, ecosystem adoption) from package managers like npm, PyPI, and Packagist. | S1, S4, U1              |
| `release-diff-analyzer`   | Runs Abstract Syntax Tree (AST) or semantic version diffs on tagged versions to detect silent or undocumented breaking changes. | S1, S6                  |
| `qa-freshness-auditor`    | Tests top tutorials, Stack Overflow answers, and code snippets against latest stable versions of a technology using LLMs and sandboxed environments. | L1, L4, S3              |
| `issue-tracker-scanner`   | Calculates Mean Time to Resolution (MTTR) and issue backlog metrics from GitHub or GitLab issue trackers. | S2, S5                  |
| `lockfile-rebuilder`      | Uses containerized environments (e.g., Docker) to rebuild projects from old lockfiles to test for reproducibility failures over time. | S4                      |
| `reverse-dependency-grapher`| Analyzes the reverse dependency graph to calculate the blast radius of a change in a core package. | U1, S4                  |
| `index-aggregator`        | Computes the final SSI scores using the defined weighting formula, aggregating data from all other modules. | FSS                     |
| `snapshot-publisher`      | Outputs monthly SSI scores, delta charts, and embeddable badges for README files and dashboards.         | Visualization           |

## Stack

-   **Data Processing & Scripting**: Python (with Pandas, Matplotlib, Plotly)
-   **Automation & CI/CD**: GitHub Actions
-   **Data Storage**: JSON or YAML for metric definitions, SQLite for historical data.
-   **Crawlers & Analyzers**: Go or Rust (for performance-intensive tasks like AST diffing in the future).

## Next Steps

1.  Finalize the core metric definitions in the `docs/` directory.
2.  Implement the initial `scoring/compute_ssi.py` script to work with a sample dataset.
3.  Develop the `fetch-registry-stats` module to gather real data for a pilot technology (e.g., React or Python).
4.  Continuously refine the weighting and formulas as more data becomes available. 