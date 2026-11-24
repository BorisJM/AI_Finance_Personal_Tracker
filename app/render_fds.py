import streamlit as st

from src.analytics.financial_discipline_score import get_financial_discipline_score


def _format_points(points, max_points):
    return "—" if points is None else f"{points} / {max_points}"


def _format_pln(amount):
    return f"{amount:,.2f} zł".replace(",", " ")


def render_fds(session):
    st.header("Financial Discipline Score", text_alignment="center")

    # Calculation lives in src/analytics; this function only displays the result
    fds = get_financial_discipline_score(session)
    period = f"{fds['start_date']:%d.%m.%Y} – {fds['end_date']:%d.%m.%Y}"

    st.caption(
        f"Last 6 full months ({period}). "
        "Sidebar filters do not apply. Transfers are excluded."
    )

    if fds["score"] is None:
        st.info(f"Score not available: {fds['reason']}")
    else:
        st.progress(fds["score"] / 100, text=f"**{fds['score']} / 100** — {fds['label']}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Savings", _format_points(fds["savings_points"], 40))
    col2.metric("Budgets", _format_points(fds["budget_points"], 35))
    col3.metric("Stability", _format_points(fds["stability_points"], 25))

    with st.expander("How is this calculated?"):
        st.markdown(
            f"""
- **Savings (max 40):** income {_format_pln(fds['total_income'])},
  expenses {_format_pln(fds['total_expenses'])}.
- **Budgets (max 35):** average budget usage
  {"—" if fds['budget_utilization'] is None else f"{fds['budget_utilization']:.0f}%"}.
  Without budgets the score is savings + stability, rescaled to 100.
- **Stability (max 25):** how much monthly expenses vary.
  Monthly expenses: {"—" if fds['monthly_expenses'] is None
                     else ", ".join(_format_pln(m) for m in fds['monthly_expenses'])}.

The score describes spending patterns in your data, not your character.
"""
        )
