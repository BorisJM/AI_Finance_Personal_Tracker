# AI Finance Personal Tracker — Development Roadmap

> Last reviewed: October 21, 2026  
> Product vision: \`Projekt AI Finance Personal Tracker - PLAN.pdf\`  
> Current status: See \`PROJECT_STATUS.md\`

## Guiding Principles

- Follow the product evolution V1 → V2 → V3 → V4.
- Resolve blockers before expanding functionality.
- Audit existing code before implementing a feature that may already exist.
- Define acceptance criteria for every meaningful task.
- Prefer small, testable increments over large rewrites.
- Use the project as a learning environment: implement, test, review, and refactor.
- Do not mark a feature complete solely because a module exists.

---

# Phase 0 — Repository Stabilization

**Goal:** Make the current codebase coherent, safe to work on, and reproducible.

### Tasks

- [ ] Inspect and resolve merge-conflict markers in \`main.py\`.
- [ ] Inspect and resolve merge-conflict markers in \`src/machine_learning/category_classification.py\`.
- [ ] Review both sides of each conflict and preserve required behavior.
- [ ] Inspect repository status and preserve unrelated changes.
- [ ] Check whether tracked database and data artifacts contain private information.
- [ ] Decide which generated or local data artifacts belong in version control.
- [ ] Audit \`.gitignore\` and already tracked files.
- [ ] Verify dependency declarations and application entry points.
- [ ] Replace machine-specific absolute paths with configurable paths.

### Acceptance criteria

- No unresolved merge-conflict markers remain in the affected source files.
- The chosen implementations are understood and reviewed.
- Sensitive data risks are assessed and documented.
- Dependencies and startup instructions reflect the actual application.
- The repository is ready for reliable feature development.

---

# V1 — MVP

**Goal:** Deliver a working application for importing transactions, analyzing spending, and presenting useful financial information.

## V1.1 — Bank CSV Import

### Tasks

- [ ] Verify CSV import for Millennium bank exports.
- [ ] Support multiple imports over time.
- [ ] Validate required columns, dates, amounts, currencies, and transaction data.
- [ ] Handle empty and malformed files with understandable errors.
- [ ] Verify transaction identifiers and duplicate detection.
- [ ] Verify SQLite persistence and import status tracking.

### Acceptance criteria

- Valid transactions are imported into the database correctly.
- Re-importing the same transactions does not create duplicates.
- Invalid input does not leave partial or inconsistent database records.
- Import behavior is covered by tests.

## V1.2 — Data Cleaning

### Tasks

- [ ] Verify lowercase normalization, digit removal, and special-character handling.
- [ ] Test regex-based cleaning and merchant-name normalization.
- [ ] Check edge cases where aggressive cleaning could remove useful information.
- [ ] Preserve the original transaction description.

### Acceptance criteria

- Cleaned descriptions are consistent and useful for analysis.
- Original descriptions remain available.
- Cleaning behavior is reproducible and tested with representative examples.

## V1.3 — Rule-Based Transaction Classification

### Tasks

- [ ] Audit existing merchant rules, aliases, and category mappings.
- [ ] Verify the required categories: Income, Groceries, Food, Transport, Housing, Entertainment, Health & Fitness, Shopping, Travel, Subscriptions, Financial, Car, and Other.
- [ ] Define a clear fallback for unknown transactions.
- [ ] Review misclassified examples and expand rules where justified.

### Acceptance criteria

- Known transaction patterns map to the expected categories.
- Unknown transactions do not silently receive misleading categories.
- Category labels remain consistent with the database and analytics.

## V1.4 — Financial Dashboard

### Tasks

- [ ] Verify total and monthly income and expenses.
- [ ] Verify spending by category and largest expenses.
- [ ] Verify monthly trends and recent transactions.
- [ ] Check empty-data behavior and applicable filters.
- [ ] Compare dashboard values with the underlying analytics.

### Acceptance criteria

- Core metrics are correct for known test datasets.
- Charts and KPIs use consistent definitions.
- The dashboard remains usable when there are no transactions.

## V1.5 — Smart Insights

### Tasks

- [ ] Audit existing insight logic.
- [ ] Implement or verify comparisons with historical spending.
- [ ] Identify meaningful increases in selected spending categories.
- [ ] Explain the data behind each generated insight.
- [ ] Handle insufficient historical data.

### Acceptance criteria

- Insights are based on actual calculations.
- Comparisons use clearly defined periods and baselines.
- The application does not make unsupported claims from insufficient data.

## V1.6 — Waste Detection

### Tasks

- [ ] Define measurable rules for frequent small payments.
- [ ] Identify spending patterns that may indicate delivery or convenience spending.
- [ ] Explore recurring subscription detection.
- [ ] Distinguish observed spending patterns from assumptions about user intent.

### Acceptance criteria

- Each detection rule has a documented definition.
- Results can be traced to transactions.
- The system presents potential waste as a signal for review, not a definitive judgment.

### V1 Completion Gate

V1 is complete when the main import-to-dashboard workflow is reliable, core analytics are tested, and Smart Insights and waste detection meet their defined acceptance criteria.

---

# V2 — Advanced Analytics

**Goal:** Explain financial behavior more deeply and quantify patterns that can support better decisions.

## V2.1 — Trend Analysis

- [ ] Month-over-month comparisons.
- [ ] Weekday versus weekend spending.
- [ ] Time-of-day spending where timestamps support it.
- [ ] Seasonal and category-specific trends.
- [ ] Clear handling of incomplete historical periods.

**Acceptance criteria:** Each trend has a clear calculation, comparison period, and testable result.

## V2.2 — Financial Discipline Score

- [ ] Define the score on a 0–100 scale.
- [ ] Define measurable factors: spending regularity, impulsivity indicators, saving behavior, spending stability, and potential waste.
- [ ] Establish how each factor contributes to the score.
- [ ] Test behavior with synthetic financial profiles.
- [ ] Explain the score and its limitations to the user.

**Acceptance criteria:** The score is reproducible, interpretable, and not presented as an objective measure of a person's character.

## V2.3 — Opportunity Cost Analysis

- [ ] Define supported historical spending scenarios.
- [ ] Allow comparisons with hypothetical alternative uses of money.
- [ ] Document assumptions, dates, and calculation methods.
- [ ] Consider historical returns, volatility, and limitations of the selected data sources.
- [ ] Clearly distinguish simulations from actual investment outcomes.

Potential scenarios in the Master Plan include ETFs, the S&P 500, NVIDIA, and Bitcoin.

**Acceptance criteria:** Results are reproducible and communicate assumptions and uncertainty. No scenario is presented as a guaranteed return or personalized investment advice.

### V2 Completion Gate

Advanced metrics must be testable, interpretable, and integrated with the existing dashboard without duplicating core calculations.

---

# V3 — Machine Learning & NLP

**Goal:** Improve transaction classification and add validated predictive capabilities.

## V3.1 — Classification Experiment

- [ ] Resolve the existing ML file conflict.
- [ ] Establish a reproducible training and evaluation workflow.
- [ ] Define training labels and category filtering.
- [ ] Evaluate TF-IDF and Logistic Regression.
- [ ] Compare ML performance against the rule-based baseline.
- [ ] Measure accuracy, macro F1, precision, and recall by category.
- [ ] Check class imbalance and repeated transaction descriptions.
- [ ] Prevent data leakage between training and evaluation.
- [ ] Evaluate confidence-based manual review.
- [ ] Record results and experiment configuration.

**Acceptance criteria:** Results can be reproduced, and the model is evaluated on data it did not train on. Performance is not judged by accuracy alone.

## V3.2 — Production Classification

- [ ] Define the prediction interface.
- [ ] Decide how rule-based predictions and ML predictions interact.
- [ ] Handle uncertain predictions and unknown categories.
- [ ] Preserve user corrections.
- [ ] Add model and vectorizer persistence if appropriate.
- [ ] Integrate classification into the import pipeline.
- [ ] Add regression and integration tests.

**Acceptance criteria:** The integrated system is reliable, testable, and has a safe fallback when predictions are uncertain or the model is unavailable.

## V3.3 — Anomaly Detection

- [ ] Define which transaction patterns count as anomalies.
- [ ] Establish simple statistical baselines.
- [ ] Evaluate false positives and missed anomalies.
- [ ] Explain why each transaction or pattern was flagged.

## V3.4 — Expense Forecasting and Overspending Risk

- [ ] Establish a simple forecasting baseline.
- [ ] Define forecast periods and required historical data.
- [ ] Evaluate forecast error on held-out periods.
- [ ] Explore spending and budget-risk indicators.
- [ ] Communicate uncertainty and data limitations.

Potential models should be selected based on evidence, not complexity alone. XGBoost and LightGBM are optional candidates from the Master Plan, not mandatory dependencies.

### V3 Completion Gate

ML and predictive functionality must outperform or meaningfully complement a simpler baseline, have reproducible evaluation, and behave safely when confidence is low.

---

# V4 — Smart Recommendation System

**Goal:** Convert reliable analytics into useful, personalized suggestions.

## V4.1 — Smart Saving Recommendations

- [ ] Identify categories with potential savings.
- [ ] Compare spending patterns between relevant merchants where data supports the comparison.
- [ ] Quantify the contribution of delivery, restaurants, subscriptions, or other categories to spending.
- [ ] Estimate potential savings using explicit assumptions.
- [ ] Explain the transactions and calculations behind each recommendation.

**Acceptance criteria:** Recommendations are actionable, traceable to data, and presented as opportunities rather than guaranteed savings.

## V4.2 — External Data Integration

Potential sources from the Master Plan:

- Fuel prices.
- Promotions.
- Stock-market APIs.
- Economic indicators.

### Tasks

- [ ] Select an integration only when it supports a defined product use case.
- [ ] Verify source availability, access terms, and update frequency.
- [ ] Protect API credentials.
- [ ] Handle missing or stale external data.
- [ ] Document the effect of external data on calculations.

**Acceptance criteria:** The application remains usable if an external service is unavailable, and external data is clearly identified.

### V4 Completion Gate

Recommendations and external integrations must add demonstrable value to the user and remain understandable, reproducible, and privacy-conscious.

---

# Ongoing Engineering Work

These activities support every version:

- [ ] Maintain a regression test suite.
- [ ] Keep dependencies and setup instructions current.
- [ ] Preserve database integrity and import idempotency.
- [ ] Use synthetic or anonymized data in tests and examples.
- [ ] Review security and privacy risks.
- [ ] Keep business logic separate from dashboard rendering.
- [ ] Update \`PROJECT_STATUS.md\` after verified milestones.
- [ ] Keep changes small and reviewable.

## Working Method

For each task:

1. State the goal and acceptance criteria.
2. Inspect the existing implementation.
3. Identify the concepts worth learning.
4. Implement a focused change.
5. Run relevant tests.
6. Review the code and explain important decisions.
7. Update the project status if the change affects it.

Do not start multiple major features simultaneously. Complete meaningful increments and move forward.

## Current Next Step

Begin with Phase 0: resolve the merge conflicts, inspect data artifacts, and verify that the application can be run and tested reproducibly.

This is a technical prerequisite, not a change to the product vision or the V1–V4 roadmap.
