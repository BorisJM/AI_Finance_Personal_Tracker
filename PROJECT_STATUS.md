# AI Finance Personal Tracker — Project Status

> Last reviewed: October 21, 2026  
> Repository: \`BorisJM/AI_Finance_Personal_Tracker\`  
> Scope: reviewed public \`main\` branch  
> Status: Work in progress

## 1. Product Vision

AI Finance Personal Tracker aims to become a Personal Finance Intelligence System.

The application is intended to help users:
- Understand their financial behavior.
- Automatically classify transactions.
- Identify unnecessary spending and potential waste.
- Discover spending patterns and trends.
- Generate useful financial insights.
- Evaluate alternative uses of money.
- Eventually use ML/NLP, forecasting, anomaly detection, and personalized recommendations.

The long-term vision is described in the project Master Plan. The features listed below distinguish existing code from planned or unverified functionality.

## 2. Current Technical Structure

The repository contains components for data loading and cleaning, rule-based classification, a processing pipeline, SQLite and SQLAlchemy persistence, financial analytics, insights, a dashboard, and ML experiments.

The intended flow is:

Bank CSV → Load and clean → Identify bank and classify transactions → Persist in SQLite → Analyze financial data → Generate insights → Display results in the dashboard.

In the reviewed version, \`src/pipeline/data_pipeline.py\` calls the rule-based classification function. The ML experiment is not yet confirmed as the production classifier used by the import pipeline.

## 3. Existing Components

The following components are present in the reviewed repository. Their presence does not guarantee that the full application currently starts or passes tests.

### 3.1 Data import and cleaning

- Bank CSV loading.
- Bank identification.
- Transaction cleaning and description normalization.
- Rule-based transaction classification.
- A shared processing pipeline.

Relevant areas: \`data/\`, \`src/cleaning/\`, \`src/classification/\`, and \`src/pipeline/\`.

### 3.2 Database and persistence

- SQLite database configuration.
- SQLAlchemy models for transactions, accounts, categories, merchants, imports, and budgets.
- Repository classes for database access.
- An import service that creates or retrieves related records.
- Transaction identifiers and duplicate checks.
- Import status and row-count tracking.

Relevant areas: \`database/models/\`, \`database/repositories/\`, and \`database/services/\`.

### 3.3 Financial analytics

Existing analytics modules include calculations for:
- Total and monthly income.
- Total and monthly expenses.
- Expenses by category.
- Category percentages and monthly category percentages.
- Top spending categories.
- Largest expenses and top transactions.
- Average monthly expenses.

Relevant area: \`src/analytics/\`.

### 3.4 Insights and dashboard

- Insight-related modules exist under \`src/insights/\`.
- Streamlit dashboard components exist under \`app/\`.
- The repository includes UI components for financial metrics, categories, transactions, trends, and insights.

End-to-end runtime behavior and consistency between displayed metrics and calculations still need verification.

## 4. Machine Learning Status

### Work already present

\`src/machine_learning/category_classification.py\` contains an ML classification experiment using:
- TF-IDF text features.
- Logistic Regression.
- Stratified K-fold cross-validation.
- Accuracy and macro F1.
- Classification reports.
- Work toward identifying uncertain predictions for manual review.

### Current limitations

The reviewed file contains Git merge-conflict markers and competing implementations. The experiment should not be treated as a coherent, production-ready classifier until this is resolved.

The production pipeline still uses rule-based classification. The following remain to be verified or completed:
- A reproducible training and evaluation workflow.
- Reliable metrics for each category.
- Evaluation against a rule-based baseline.
- Leakage-resistant validation.
- A measured threshold for manual review.
- Model and vectorizer persistence, if required.
- Integration into the import flow.
- Handling of unknown categories and user corrections.

Previous experimental metrics should not be treated as production performance without a reproducible evaluation.

## 5. Blockers and Risks

### Critical — Code consistency

The reviewed versions of \`main.py\` and \`src/machine_learning/category_classification.py\` contain merge-conflict markers.

Both files need to be reconciled before the affected execution paths can be considered reliable.

### High — Reproducibility

- \`main.py\` includes a machine-specific Windows path to a CSV file.
- \`requirements.txt\` appears incomplete relative to imports in the code.
- Installation, initialization, and application startup need to be verified in a clean environment.

### High — Financial data privacy

Database/data artifacts, including \`database.db\` and \`test.parquet\`, are visible in the reviewed repository snapshot.

Their contents and intended role should be checked before deciding whether they belong in version control. \`.gitignore\` does not remove already tracked files or erase their history.

### High — Import reliability

Verify:
- Input validation and malformed-file handling.
- Duplicate-import behavior.
- Database rollback on failures.
- Transaction, merchant, account, category, and import relationships.
- Consistency of import status and row counts.

### Medium — Automated tests

Review the existing test suite and add coverage for core pipeline behavior, import integrity, database rules, and financial calculations.

Do not claim tests pass unless they have actually been run.

## 6. Product Version Status

### V1 — MVP

**Partially implemented; end-to-end status requires verification.**

Code exists for import, cleaning, rule-based classification, analytics, insight logic, and dashboard components.

The remaining work is to resolve repository blockers, verify end-to-end behavior, and confirm that the required MVP flows work reliably.

### V2 — Advanced Analytics

**Partially implemented / needs feature-level audit.**

Some analytics and insight components exist. Financial Discipline Score, Opportunity Cost Analysis, and the full planned trend-analysis scope need explicit verification against the Master Plan.

### V3 — Machine Learning & NLP

**Experimental; not confirmed as integrated production functionality.**

An ML classification experiment exists, but its implementation needs conflict resolution, reliable evaluation, and a deliberate integration decision. Predictions, anomaly detection, and forecasting require separate validation.

### V4 — Smart Recommendation System

**Long-term planned scope.**

Personalized saving recommendations and external data integrations should follow reliable core analytics and validated model behavior.

## 7. Immediate Priorities

1. Resolve merge conflicts without losing required behavior.
2. Audit tracked data and database artifacts for privacy.
3. Verify dependencies, paths, database initialization, and application startup.
4. Test CSV import, duplicate handling, and database consistency.
5. Establish a small regression test suite.
6. Complete ML evaluation and compare against rule-based classification.
7. Integrate ML only when its behavior is measurable and sufficiently reliable.
8. Audit V2 features and proceed toward V3 and V4 incrementally.

See \`docs/ROADMAP.md\` for task-level scope and acceptance criteria.

## 8. Development Principles

- Build iteratively rather than implementing every feature at once.
- Keep production code separate from experiments until integration is justified.
- Prefer understandable solutions and measurable results.
- Preserve financial data privacy.
- Use tests to protect business rules and data integrity.
- Learn through implementation, debugging, and code review.
- Update this document when meaningful progress is verified.
