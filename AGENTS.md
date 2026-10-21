# AI Agent Instructions — AI Finance Personal Tracker

## 1. Project Vision

AI Finance Personal Tracker is a Personal Finance Intelligence System, not merely a budget tracker.

Its purpose is to help users understand their financial behavior, automatically categorize transactions, identify unnecessary spending, discover trends, generate financial insights, and make better financial decisions.

The long-term vision includes Machine Learning, NLP, anomaly detection, forecasting, opportunity-cost analysis, and personalized saving recommendations.

Use \`README.md\`, \`PROJECT_STATUS.md\`, \`docs/ROADMAP.md\`, and the project Master Plan as context. The actual code determines what is currently implemented.

## 2. Development and Learning Philosophy

This is both a software product and a hands-on learning project.

- Prefer small, focused tasks with clear acceptance criteria.
- Teach important concepts through implementation rather than giving complete solutions immediately.
- Let the owner implement meaningful features, then review their code.
- Explain errors, design decisions, trade-offs, and edge cases.
- Provide full implementations for incidental boilerplate when it is not worth studying in depth.
- Avoid spending excessive time polishing one feature before moving forward.
- Do not introduce advanced technology merely because it is available.
- Prioritize a working, understandable application over premature perfection.

For substantial tasks, provide:
1. The goal and why it matters.
2. The files and components likely to be affected.
3. The concepts the owner should learn.
4. A concrete implementation assignment.
5. Acceptance criteria and suggested tests.
6. Code review after the owner submits their implementation.

The project plan proposes allocating approximately 70% of learning time to building and debugging the project and 30% to courses, theory, and documentation.

## 3. Product Roadmap

Preserve the product's intended evolution:

- **V1 — MVP:** Bank CSV import, data cleaning, rule-based classification, financial dashboard, Smart Insights, and waste detection.
- **V2 — Advanced Analytics:** Financial Discipline Score, Opportunity Cost Analysis, and deeper spending and behavioral trend analysis.
- **V3 — Machine Learning & NLP:** Text-based transaction classification, model evaluation, predictions, anomaly detection, and spending forecasts.
- **V4 — Smart Recommendations:** Personalized saving recommendations and selected external data integrations.

These are product goals, not claims that all features currently exist. Consult \`PROJECT_STATUS.md\` before selecting the next task.

## 4. Architecture and Existing Components

The repository includes the following areas:

- \`src/cleaning/\` — transaction cleaning.
- \`src/classification/\` — rule-based classification and merchant handling.
- \`src/pipeline/\` — data-processing pipeline.
- \`src/machine_learning/\` — ML classification experiments and services.
- \`src/analytics/\` — financial calculations and analysis.
- \`src/insights/\` — financial insight logic.
- \`src/data/\` — data transformation utilities.
- \`database/models/\` — SQLAlchemy models.
- \`database/repositories/\` — database access.
- \`database/services/\` — application services, including imports.
- \`app/\` — dashboard and UI components.
- \`data/\` — input, processed, and reference data.
- \`main.py\` — current analysis and ML entry point.
- \`database/database_design.md\` — database entities and business rules.

Verify the current implementation before assuming that a module is complete, tested, or integrated with the rest of the application.

## 5. Engineering Principles

### Data pipeline and classification

- Preserve a clear separation between loading, cleaning, classification, persistence, analytics, and presentation.
- Keep the existing rule-based classifier understandable and testable.
- Treat experimental ML code separately from production behavior until validated.
- Define explicit interfaces between pipeline stages.
- Handle malformed files, missing values, and empty datasets deliberately.

### Database and imports

- Follow existing SQLAlchemy models, repository patterns, and business rules.
- Preserve transaction identifiers and duplicate-import protection.
- Use transactions to maintain consistency across related records.
- Test import failures, repeated imports, and invalid records.
- Avoid schema changes without considering migration and existing data compatibility.

### Analytics and insights

- Audit existing calculations before adding new ones.
- Define financial metrics clearly and test edge cases.
- Keep business calculations separate from dashboard rendering.
- Ensure insights can be traced to the data and rules behind them.
- Do not describe a correlation or prediction as a guaranteed financial outcome.

### Machine Learning

- Establish a baseline before evaluating more complex models.
- Evaluate accuracy, macro F1, per-class precision and recall.
- Check class imbalance, repeated descriptions, and data leakage.
- Fit preprocessing only on training data.
- Evaluate confidence-based manual review rather than choosing thresholds arbitrarily.
- Preserve a safe fallback and user corrections when integrating ML.

## 6. Testing and Verification

- Inspect the existing test suite before adding a new testing framework.
- Add focused tests for business logic and changed behavior.
- Prefer synthetic or anonymized transaction data in tests.
- Run relevant tests and report the actual result.
- If verification is not possible, state the limitation explicitly.
- Do not claim that the application works merely because its modules exist.

## 7. Security and Financial Privacy

Bank exports, transaction descriptions, account identifiers, database files, and model artifacts may contain sensitive information.

- Never expose real financial data unnecessarily.
- Never commit credentials or API keys.
- Review tracked files and Git history when investigating sensitive artifacts.
- Remember that \`.gitignore\` does not remove files already tracked by Git.
- Do not upload private financial data to external services without explicit authorization.
- Explain the impact of destructive data or repository operations before performing them.

## 8. Git and Change Management

- Inspect repository status and diffs before modifying files.
- Preserve unrelated work and local changes.
- Resolve merge conflicts by understanding both sides rather than deleting markers blindly.
- Keep changes small and logically grouped.
- Do not commit or push without explicit authorization.
- Update \`PROJECT_STATUS.md\` and \`docs/ROADMAP.md\` when meaningful project status changes occur.

## 9. Definition of Done

A task is complete when:
- Its acceptance criteria are met.
- Relevant tests or verification have been performed.
- Data integrity and existing behavior are preserved.
- Documentation is updated where necessary.
- Limitations and outstanding issues are recorded.
- The owner understands the important decisions and can continue independently.
