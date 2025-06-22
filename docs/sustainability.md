# Sustainability (S)

**Weight: 45%**

Sustainability is the most heavily weighted category, as it measures the long-term viability, maintainability, and resilience of a technology. A high sustainability score indicates that a system built with the technology will be stable, predictable, and cost-effective to maintain over time.

This metric is a weighted average of the following sub-components, each scored on a scale of 0.0 to 10.0.

## Sub-Metrics

### S1: Frequency of Breaking Changes
-   **Description**: Measures how often the technology introduces breaking changes in its official releases, violating Semantic Versioning (SemVer) or failing to provide backward compatibility layers.
-   **Data Sources**: Automated analysis of Git repository changelogs, release notes, and AST (Abstract Syntax Tree) diffs between major/minor versions.

### S2: Unresolved Issue Backlog
-   **Description**: Calculates the percentage of unresolved issues (bugs, feature requests) in the official repository over the last 12-24 months. A large or growing backlog indicates a lack of maintainer resources or responsiveness.
-   **Data Sources**: GitHub/GitLab API to query the number of open vs. closed issues over a specific time period.

### S3: LLM Problem-Solving Success Rate
-   **Description**: Measures the success rate of leading LLMs in fixing real-world bugs or implementing features for the technology. This is a proxy for how "known" and "stable" the problem space is.
-   **Data Sources**: A standardized test bank of bug-fix and implementation prompts run against major LLM APIs. Success is measured by whether the generated code passes predefined tests.

### S4: Dependency Graph Volatility
-   **Description**: Assesses the stability of the technology's core dependencies. High volatility in foundational packages (e.g., a core compiler, web server, or utility library) introduces significant downstream risk.
-   **Data Sources**: Analysis of `package.json`, `composer.json`, `go.mod`, etc., to track the frequency and magnitude of updates to critical dependencies.

### S5: Community Support Resolution Time
-   **Description**: Measures the average time it takes for a developer to receive a correct and helpful answer from community channels.
-   **Data Sources**: Scraping and analysis of platforms like Stack Overflow and Reddit to calculate the median time between a question being posted and an accepted answer being provided.

### S6: Backward Compatibility Support
-   **Description**: Evaluates the project's official policy and track record for supporting older versions. A long support window (e.g., Python's support for 3.x versions) reduces maintenance pressure.
-   **Data Sources**: Official documentation, release notes, and community announcements regarding Long-Term Support (LTS) versions.
