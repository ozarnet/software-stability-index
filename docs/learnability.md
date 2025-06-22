# Learnability (L)

**Weight: 30%**

Learnability measures the ease of learning and the availability of valid, up-to-date educational resources for a given technology. A high learnability score indicates that a developer can quickly become proficient, relying on accessible and accurate materials.

This metric is a weighted average of the following sub-components, each scored on a scale of 0.0 to 10.0.

## Sub-Metrics

### L1: Tutorial & Documentation Freshness
-   **Description**: Measures how up-to-date the official documentation and community tutorials are. It is evaluated by analyzing the last-updated dates of official docs, blog posts, and guides, and penalizing for outdated code snippets or deprecated APIs.
-   **Data Sources**: Website scraping of official documentation, popular tutorial sites (e.g., DigitalOcean, Smashing Magazine), and developer blogs. Git history of documentation repositories.

### L2: MOOC & Video Platform Coverage
-   **Description**: Assesses the quantity and quality of courses available on major Massive Open Online Course (MOOC) platforms and video-sharing sites.
-   **Data Sources**: APIs or scraping of platforms like Coursera, Udemy, Pluralsight, and YouTube to count relevant courses and assess their ratings and last-updated dates.

### L3: Diversity of Learning Formats
-   **Description**: Evaluates the availability of different types of learning resources, catering to various learning styles.
-   **Data Sources**: Manual or automated checks for the existence of official documentation, interactive sandboxes (e.g., CodeSandbox, StackBlitz), example project repositories, and video tutorials.

### L4: LLM Answer Freshness & Success Rate
-   **Description**: Measures the ability of leading Large Language Models (LLMs) to generate accurate and currently valid solutions to common problems. A low success rate indicates knowledge obsolescence in the model's training data.
-   **Data Sources**: A standardized test bank of prompts related to the technology is run against major LLM APIs (e.g., GPT-4, Gemini, Claude). The generated code is then linted and tested for correctness.
