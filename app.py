import streamlit as st

from planner import (
    FASTING_CONFIGS,
    generate_meal_plan,
)
from meals import MEALS

# ============= BASE CONFIG =============

st.set_page_config(
    page_title="Fibroid-Friendly Meal Planner",
    page_icon="🧡",
    layout="centered",
)

# ============= MOBILE-FIRST CSS =============

st.markdown(
    """
    <style>
    /* Make main content narrower and readable on mobile */
    .main-block {
        max-width: 800px;
        margin: 0 auto;
    }

    /* Card styling for each meal */
    .meal-card {
        border-radius: 12px;
        padding: 0.75rem 0.9rem;
        margin-bottom: 0.75rem;
        background: #ffffff10;
        border: 1px solid #ffffff20;
    }

    .meal-header {
        font-weight: 600;
        margin-bottom: 0.1rem;
    }

    .meal-meta {
        font-size: 0.8rem;
        color: #888;
        margin-bottom: 0.25rem;
    }

    .meal-tags {
        font-size: 0.8rem;
        color: #aaa;
    }

    /* Day separator */
    .day-header {
        margin-top: 1.25rem;
        margin-bottom: 0.5rem;
        font-size: 1.05rem;
        font-weight: 700;
    }

    /* Tighter padding on the whole app */
    [data-testid="stAppViewContainer"] {
        padding-top: 0.5rem;
        padding-bottom: 1.5rem;
    }

    /* Make headings smaller on small screens */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.6rem !important;
        }
        .day-header {
            font-size: 1rem;
        }
        .meal-header {
            font-size: 0.95rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============= TITLE / INTRO =============

st.markdown('<div class="main-block">', unsafe_allow_html=True)

st.title("🧡 Fibroid-Friendly Anti-Inflammatory Planner")

st.markdown(
    """
This planner creates **anti-inflammatory, fibroid-supporting meal days** that
also respect your **fasting window**.

> This is **not medical advice**. Always work with your doctor for diagnosis and treatment.
"""
)

# ============= SIDEBAR CONTROLS =============

st.sidebar.header("Settings")

pattern_ids = list(FASTING_CONFIGS.keys())
selected_pattern_id = st.sidebar.selectbox(
    "Fasting pattern",
    options=pattern_ids,
    format_func=lambda pid: FASTING_CONFIGS[pid].label,
)

st.sidebar.caption(FASTING_CONFIGS[selected_pattern_id].description)

eat_window_start_hour = st.sidebar.slider(
    "Eating window start (hour)",
    min_value=8,
    max_value=14,
    value=12,
    help="Hour of your first meal in the day. For 16:8 with 2 meals, 11–13 works well.",
)

fibroid_focus = st.sidebar.checkbox(
    "Prioritise fibroid support (fibre, cruciferous, liver support)",
    value=True,
)

anemia_risk = st.sidebar.checkbox(
    "Prioritise iron-support meals",
    value=True,
)

days = st.sidebar.slider(
    "Days to plan",
    min_value=7,
    max_value=30,
    value=30,
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"Meals in database: **{len(MEALS)}**")

# ============= MAIN ACTION =============

generate_clicked = st.sidebar.button("Generate meal plan 🚀")

if generate_clicked:
    plan = generate_meal_plan(
        days=days,
        fasting_pattern_id=selected_pattern_id,
        eat_window_start_hour=eat_window_start_hour,
        fibroid_focus=fibroid_focus,
        anemia_risk=anemia_risk,
    )

    st.subheader(f"📅 Your {days}-day plan")

    for day_plan in plan:
        # Day header
        st.markdown(
            f'<div class="day-header">📆 {day_plan.day.isoformat()}</div>',
            unsafe_allow_html=True,
        )

        if not day_plan.meals:
            st.info("No meals found for this day with the current settings.")
            continue

        for slot in day_plan.meals:
            meal = slot.meal
            tags_display = ", ".join(meal.tags) if meal.tags else "no tags"

            # Wrap each meal in a styled card
            st.markdown('<div class="meal-card">', unsafe_allow_html=True)

            # Header line
            st.markdown(
                f'<div class="meal-header">{slot.time_str} · '
                f'{meal.meal_type.title()} · {meal.name}</div>',
                unsafe_allow_html=True,
            )

            # Scores line
            st.markdown(
                f'<div class="meal-meta">'
                f'Anti-inflammatory score: {meal.anti_inflammatory_score} · '
                f'Iron support: {meal.iron_support} · '
                f'Fibre score: {meal.fiber_score}'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Tags
            st.markdown(
                f'<div class="meal-tags">Tags: {tags_display}</div>',
                unsafe_allow_html=True,
            )

            # Full recipe: ingredients + method in expander (saves vertical space on mobile)
            if meal.ingredients or meal.instructions:
                with st.expander("📋 How to make this"):
                    if meal.ingredients:
                        st.markdown("**Ingredients**")
                        for ing in meal.ingredients:
                            amount = ing.get("amount", "").strip()
                            item = ing.get("item", "").strip()
                            if amount:
                                st.markdown(f"- {amount} {item}")
                            else:
                                st.markdown(f"- {item}")

                    if meal.instructions:
                        st.markdown("**Step-by-step**")
                        for idx, step in enumerate(meal.instructions, start=1):
                            st.markdown(f"{idx}. {step}")

            st.markdown("</div>", unsafe_allow_html=True)  # close .meal-card

        st.markdown("---")

else:
    st.info(
        "Use the sidebar to choose your fasting pattern and focus, "
        "then tap **Generate meal plan 🚀**."
    )

st.markdown("</div>", unsafe_allow_html=True)  # close .main-block
