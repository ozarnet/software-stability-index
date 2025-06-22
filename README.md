# Software Stability Index (SSI)

**An objective, data-driven methodology to score the long-term stability of software.**

---

## The Problem: The "Beta-fication" of Production Software

In today's fast-paced digital landscape, there is immense pressure to innovate and release new software constantly. This has led to a troubling trend: major software publishers, including tech giants, often release products with known bugs, effectively turning their user base into a distributed, unpaid quality assurance team.

As an article from [GOZmosis](https://gozmosis.blogspot.com/2023/04/tech-giants-and-consumers-role-in.html) points out, this cycle of "rapid, potentially problematic releases" can disrupt workflows, cause productivity loss, and erode trust. Yet, this growing problem is not discussed nearly enough, leaving developers and technical leaders to navigate a volatile ecosystem with very little objective data.

The **Software Stability Index (SSI)** was created to address this gap.

## Our Mission: Towards Objective Stability Metrics

The goal of SSI is to move beyond marketing hype and anecdotal evidence, providing an objective, quantifiable score for the real-world stability of the tools we use every day.

We aim to:

1.  **Empower Developers & Leaders**: Provide clear, data-driven insights to help them make informed technology choices.
2.  **Promote Accountability**: Encourage tool maintainers to prioritize long-term stability over feature velocity.
3.  **Create a New Heuristic**: Establish a transparent, reproducible, and community-driven standard for measuring software health.

## How It Works: A Multi-Dimensional Score

The SSI gives each tool or platform a normalized score from **0.0 to 10.0**. This score is a weighted average of three core dimensions:

-   **Sustainability (45%)**: The long-term viability, dependency stability, and backward compatibility of the technology.
-   **Learnability (30%)**: The availability and freshness of high-quality learning resources.
-   **Applicability (25%)**: The breadth of use cases and the health of the surrounding ecosystem.

Each dimension is broken down into measurable sub-metrics like release volatility, mean time to resolve issues, and tutorial freshness, which are pulled from live sources like GitHub, package registries, and community forums.

For a detailed breakdown of the metrics, see the `docs/` directory.

## Why This Matters

-   Tutorials break. Stack Overflow answers age out—too soon.
-   Frameworks churn. Packages abandon their users—too soon.
-   LLMs give wrong advice because *their training data go stale—too soon*.

**Software engineering deserves better metrics.**

## Get Involved: Help Us Build a Better Heuristic!

Tired of frameworks that break on patch releases? Frustrated by tutorials that are already outdated? You're not alone.

The SSI is an ambitious open-source project aiming to bring transparency and accountability to the software ecosystem. But a project this big requires a community. We need your expertise to build a truly comprehensive and objective index.

**You can help!**

*   **⭐ Star this repository** to show your support and follow our progress.
*   **🍴 Fork the code** and add a data source for your favorite language or framework.
*   **⬆️ Send a Pull Request** to refine the scoring algorithm, add a new metric, or improve documentation.
*   **🗣️ Open an Issue** to suggest a technology you'd like to see scored.

Together, we can build a standard that empowers developers and pushes the industry toward a more stable future.

## Current Status & Roadmap

The project is currently in **Phase 2: Data Collection**. We have implemented the core scoring logic and data fetchers for PyPI, Packagist, npm, and GitHub issue metrics.

You can run the proof-of-concept scoring script:
```bash
python scoring/compute_ssi.py
```

Our roadmap is tracked in `DEVELOPMENT_PLAN.md`.

## Example SSI Scores

*This table is generated from a mix of sample data and live data fetched by the script.*

| Stack / Tool             | Learnability | Applicability | Sustainability | SSI  |
| ------------------------ | ------------ | ------------- | -------------- | ---- |
| HTML                     | 9.5          | 10.0          | 10.0           | 9.83 |
| Node.js                  | 7.0          | 9.5           | 2.0            | 6.16 |
| Python (core only)       | 9.0          | 9.1           | 4.75           | 7.62 |
| Python (w/ ML packages)  | 1.2          | 0.5           | 0.25           | 0.65 |
| Python + Django          | 7.0          | 8.0           | 5.5            | 6.83 |
| Laravel                  | 3.75         | 5.49          | 4.5            | 4.58 |
| CodeIgniter              | 7.5          | 9.0           | 5.4            | 7.3  |
| React + Next.js          | 6.5          | 9.0           | 2.5            | 6.0  |
| Angular                  | 5.0          | 8.5           | 3.5            | 5.67 |
| Java + Spring Boot       | 6.0          | 8.0           | 7.5            | 7.17 |
| ASP.NET Core             | 7.0          | 8.5           | 6.0            | 7.17 |
| WPF (.NET Framework)     | 4.5          | 6.0           | 7.0            | 5.83 |
| WinUI                    | 2.0          | 6.0           | 3.0            | 3.67 |
| SwiftUI                  | 1.0          | 4.5           | 2.5            | 2.67 |
| Kotlin + Jetpack Compose | 6.0          | 7.5           | 4.0            | 5.83 |

---

## Author & License

This project was initiated by **Gökhan Ozar** ([https://ozar.net](https://ozar.net)) out of frustration with breakage fatigue—and a desire to push back with measurable engineering rigor.

Licensed under the **MIT License**. See `LICENSE` for details.

```


