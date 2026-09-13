# AI Personal Finance Analyzer --- Project Status

> Current development snapshot\
> Last updated: September 2026

## Overview

AI Personal Finance Analyzer is a personal finance intelligence system
designed to go beyond traditional budget tracking.

The goal is to transform raw bank transaction data into structured
information, financial analytics and actionable insights that help
understand spending behavior and make better financial decisions.

The project is currently in the **MVP / foundation stage**. The core
data flow is working, while the backend, dashboard and analytics are
still being actively developed and refined.

------------------------------------------------------------------------

## Current Data Flow

``` text
Bank CSV
   ↓
Data Import
   ↓
Preprocessing & Cleaning
   ↓
Merchant Identification
   ↓
Transaction Classification
   ↓
SQLite Database
   ↓
Analytics
   ↓
Financial Insights
   ↓
Streamlit Dashboard
```

------------------------------------------------------------------------

## Implemented

### 1. Data Import

-   Bank transaction CSV import
-   Automatic bank identification
-   Data validation and normalization
-   Support for multiple imported files
-   Import tracking

### 2. Data Cleaning & Preprocessing

-   Column normalization
-   Data type conversion
-   Date handling
-   Transaction description cleaning
-   Regex-based text cleaning
-   Lowercase normalization
-   Removal of unnecessary characters and numbers
-   Stopword handling
-   Edge-case handling

Example:

``` text
BIEDRONKA 4432 RADOM
        ↓
biedronka
```

### 3. Transaction Classification

The current classification system is rule-based.

Implemented:

-   Merchant identification
-   Merchant normalization
-   Merchant aliases
-   Category assignment
-   Income vs. expense separation
-   Dictionary-based classification rules

Current categories include:

-   Income
-   Groceries
-   Food
-   Transport
-   Housing
-   Entertainment
-   Health & Fitness
-   Shopping
-   Travel
-   Subscriptions
-   Financial
-   Car
-   Other

### 4. Database

The project uses:

-   SQLite
-   SQLAlchemy

Main entities:

-   Transaction
-   Account
-   Category
-   Merchant
-   Import / Source File
-   Budget

The database layer also contains:

-   SQLAlchemy models
-   Relationships
-   Repository Pattern
-   Import service
-   Database session management
-   Business rules and validation

### 5. Analytics

Implemented analytics include:

-   Total expenses
-   Total income
-   Monthly expenses
-   Monthly income
-   Expenses by category
-   Category percentages
-   Category percentages by month
-   Top categories
-   Largest expenses
-   Top transactions
-   Average monthly expenses
-   Savings
-   Savings rate
-   Spending trends

### 6. Financial Insights

The project contains a dedicated insights layer for generating automated
observations.

Current areas include:

-   Expense insights
-   Income insights
-   Savings insights
-   Trend insights
-   Waste / potential money leak insights
-   Combined AI insight presentation layer

The current insights are primarily based on rules and statistical
analysis rather than machine learning.

### 7. Dashboard

The application uses Streamlit.

Current dashboard functionality includes:

-   Financial KPIs
-   Total income
-   Total expenses
-   Savings
-   Savings rate
-   Transaction count
-   Expense breakdown by category
-   Monthly income vs. expenses
-   Spending trends
-   Average transaction value
-   Top expenses
-   Recent transactions
-   Financial insights
-   Date filtering
-   Category filtering
-   Interactive Plotly visualizations

------------------------------------------------------------------------

## Architecture

The project is structured into separate layers:

``` text
app/
    Dashboard and UI rendering

src/
    cleaning/
    classification/
    analytics/
    insights/
    pipeline/

database/
    models/
    repositories/
    services/

data/
    raw/
    processed/
    dictionaries/
```

The architecture is being developed with separation of responsibilities
in mind, rather than keeping all logic inside the dashboard or a single
script.

------------------------------------------------------------------------

## Current Development Focus

The project is **not finished**.

The current priority is to strengthen the foundation before moving into
advanced Machine Learning features.

### Backend & Services

-   Complete and improve the service layer
-   Improve interactions between pipeline, database and application
    layers
-   Add missing validation and edge-case handling
-   Improve error handling

### Architecture & Code Quality

-   Refactor existing code where necessary
-   Improve separation of responsibilities
-   Reduce duplicated logic
-   Improve maintainability
-   Add tests
-   Improve project documentation

### Dashboard

-   Improve existing dashboard components
-   Add and refine visualizations
-   Improve filtering and user experience
-   Add additional analytics and insights

### Analytics & Insights

-   Extend financial behavior analysis
-   Improve trend detection
-   Improve waste detection
-   Add more meaningful financial insights

------------------------------------------------------------------------

## Planned Advanced Features

Once the current foundation is stable, the project will gradually move
towards Machine Learning and NLP.

### Machine Learning & NLP

-   TF-IDF for transaction descriptions
-   Logistic Regression for transaction classification
-   ML-based merchant/category prediction
-   NLP-based transaction understanding

### Advanced Analytics

-   Anomaly detection
-   Spending forecasting
-   Overspending risk detection
-   More advanced behavioral analysis

### Smart Recommendations

-   Personalized saving recommendations
-   Spending optimization suggestions
-   Opportunity cost analysis
-   Investment scenario simulations

------------------------------------------------------------------------

## Technology Stack

### Core

-   Python
-   Pandas
-   NumPy

### Database

-   SQLite
-   SQLAlchemy

### Dashboard & Visualization

-   Streamlit
-   Plotly
-   Matplotlib

### Machine Learning

-   scikit-learn
-   XGBoost (planned)

### Development

-   Git
-   GitHub
-   VS Code
-   Jupyter Notebook

------------------------------------------------------------------------

## Project Philosophy

The project is being developed incrementally.

The goal is not to add Machine Learning as quickly as possible, but to
first build a reliable foundation:

**Clean data → solid architecture → reliable analytics → meaningful
insights → Machine Learning**

The project is also being used as a practical way to develop Data
Science and software engineering skills through building, debugging,
refactoring and continuously improving a real application.

------------------------------------------------------------------------

## Long-Term Vision

The final goal is to create a **Personal Finance Intelligence System**
that can answer more than:

> "How much did I spend?"

It should eventually help answer:

> "Why am I spending this way, what patterns can be identified, where
> can I improve, and what could happen if I changed my behavior?"

------------------------------------------------------------------------

## Status

**Current stage:** MVP / Foundation + Analytics + Dashboard

**Completed:** Core data pipeline, cleaning, rule-based classification,
database layer, analytics, insights and initial dashboard

**In progress:** Backend/service layer, architecture improvements,
validation, dashboard improvements, analytics and insights

**Next major stage:** Machine Learning & NLP

**Overall status:** 🚧 Work in progress
