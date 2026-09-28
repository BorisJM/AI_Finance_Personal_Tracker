import streamlit as st

from database.services.budget_service import BudgetService


def render_budgets(session):
    st.header("Budgets", text_alignment="center")

    budget_service = BudgetService(session)
    budgets = budget_service.get_all_budgets()

    with st.expander("Create new budget"):
        categories = budget_service.get_categories()

        category_options = {
            "All expenses": None,
            **{category.name: category.id for category in categories},
        }

        selected_category = st.selectbox(
            "Category",
            options=list(category_options.keys()),
        )

        monthly_limit = st.number_input(
            "Monthly limit",
            min_value=0.01,
            value=1000.00,
            step=50.00,
        )

        start_date = st.date_input(
            "Start date",
        )

        end_date = st.date_input(
            "End date",
        )

        if st.button("Create budget", width="stretch"):
            try:
                budget_service.create_budget(
                    monthly_limit=monthly_limit,
                    start_date=start_date,
                    end_date=end_date,
                    category_id=category_options[selected_category],
                )

                st.success("Budget created successfully.")
                st.rerun()

            except ValueError as error:
                st.error(str(error))

    if not budgets:
        st.info("No budgets created yet.")
        return

    for budget in budgets:
        status = budget_service.get_budget_status(budget.id)

        if status is None:
            continue

        category_name = (
            budget.category.name
            if budget.category is not None
            else "All expenses"
        )

        spent = status["total_spent"]
        limit = status["budget"].monthly_limit
        remaining = status["remaining"]
        percentage_used = status["spent_percentage"]

        st.subheader(category_name)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Budget",
                f"{limit:.2f} zł",
            )

        with col2:
            st.metric(
                "Spent",
                f"{spent:.2f} zł",
            )

        with col3:
            if remaining >= 0:
                st.metric(
                    "Remaining",
                    f"{remaining:.2f} zł",
                )
            else:
                st.metric(
                    "Over budget",
                    f"{abs(remaining):.2f} zł",
                )
        progress = min(float(percentage_used) / 100, 1.0)

        if percentage_used >= 100:
            status_text = "🔴 Over budget"
        elif percentage_used >= 80:
            status_text = "🟠 Budget almost reached"
        else:
            status_text = "🟢 Within budget"

        st.progress(progress)

        st.caption(
            f"{status_text} · "
            f"{percentage_used:.2f}% used · "
            f"{budget.start_date} – {budget.end_date}"
        )
        st.divider()