# Software Stability Index (SSI)

A scientific, data-driven methodology and scoring system for evaluating the **stability, applicability, and learnability** of software development tools — including programming languages, SDKs, frameworks, APIs, and IDEs.

> “Dependencies rot. Docs decay. APIs break. SSI will help you see it coming.”

---

## 🚀 What Is SSI?

The **Software Stability Index (SSI)** gives each tool or platform a normalized score from **0.0 to 10.0**, based on how:

- Easy it is to learn and get productive with (Learnability)
- Broad and effective it is in real-world use (Applicability)
- Reliable and future-proof it is over time (Sustainability)

These three dimensions are broken down into measurable sub-metrics like:
- Release volatility
- SemVer violation rate
- LLM answer success rate
- Tutorial freshness
- Lockfile reproducibility
- Time to resolve regressions

> SSI helps developers and teams choose tech stacks *intelligently*, not reactively.

---

## 🧠 Why SSI Matters

- Tutorials break. Stack Overflow answers age out, and too soon.  
- Frameworks churn. Packages abandon their users - too soon.  
- LLMs give wrong advice because *their training data turn stale, too soon*.  

**Software engineering deserves better metrics.**

---

## 📊 Example Output

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

## 🧠 Why SSI Matters

- Tutorials break. Stack Overflow answers age out, and too soon.  
- Frameworks churn. Packages abandon their users - too soon.  
- LLMs give wrong advice because *their training data turn stale, too soon*.  

**Software engineering deserves better metrics.**

---

## 📁 Repo Structure

```bash
ssi/
├── docs/          # Metric definitions
├── scoring/       # Scoring scripts and formula logic
├── examples/      # Sample stack evaluations
├── automation/    # Optional CI/data-gathering logic
├── CONTEXT.md     # Project context and intent
├── README.md      # This file
└── LICENSE

---

## 🧪 How It Works

Each tool is scored across three core dimensions:

* **Learnability**: Tutorial freshness, LLM completion accuracy, StackOverflow obsolescence
* **Applicability**: Integration coverage, usage diversity, plugin ecosystem maturity
* **Sustainability**: Release volatility, SemVer violations, ecosystem abandonment, lockfile reproducibility

Each sub-metric is normalized, weighted, and contributes to the final **SSI score**.

---

## 📦 Status

🔧 Alpha — currently defining the metric framework and scoring scripts
📈 JSON/CSV sample scores in progress
🤝 Contributions, validation, criticism welcome

---

## 🔒 License

This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## 👤 Author

**Gökhan Ozar**
[https://ozar.net](https://ozar.net)
Initiator of CodeIgniter Wizard, DMARC Aide, and other pragmatic tools
This project was born out of frustration with breakage fatigue — and a desire to push back with measurable engineering rigor.

```


