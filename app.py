import streamlit as st

from planner import (
    FASTING_CONFIGS,
    generate_meal_plan,
)
from meals import MEALS


st.set_page_config(
    page_title="Fibroid-Friendly Anti-Inflammatory Planner",
    layout="wide"
)

st.title("🧡 Fibroid-Friendly Anti-Inflammatory Meal Planner")

st.markdown(
    """
This app creates a rotating meal plan using **anti-inflammatory, fibroid-supporting meals**.

> ⚠️ This is **not medical advice** and cannot guarantee shrinking fibroids.  
> Always work with your doctor for diagnosis and treatment.
"""
)

# ============= SIDEBAR CONTROLS =============

st.sidebar.header("Your settings")

pattern_ids = list(FASTING_CONFIGS.keys())
selected_pattern_id = st.sidebar.selectbox(
    "Fasting pattern",
    options=pattern_ids,
    format_func=lambda pid: FASTING_CONFIGS[pid].label,
)

st.sidebar.caption(FASTING_CONFIGS[selected_pattern_id].description)

eat_window_start_hour = st.sidebar.slider(
    "Eating window start (hour of day)",
    min_value=6,
    max_value=14,
    value=11,
    help="Hour of your first meal in the day, e.g. 11 = 11:00.",
)

fibroid_focus = st.sidebar.checkbox(
    "Prioritise fibroid-friendly meals (high fibre, cruciferous, hormone support)",
    value=True,
)

anemia_risk = st.sidebar.checkbox(
    "Prioritise iron-supporting meals (for heavy bleeding / low iron)",
    value=True,
)

days = st.sidebar.slider(
    "Number of days to plan",
    min_value=7,
    max_value=30,
    value=30,
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"Meals in database: **{len(MEALS)}**")

# ============= MAIN ACTION =============

if st.sidebar.button("Generate meal plan 🚀"):
    plan = generate_meal_plan(
        days=days,
        fasting_pattern_id=selected_pattern_id,
        eat_window_start_hour=eat_window_start_hour,
        fibroid_focus=fibroid_focus,
        anemia_risk=anemia_risk,
    )

    st.subheader(f"📅 Your {days}-day meal plan")

    for day_plan in plan:
        st.markdown(f"## 📅 {day_plan.day.isoformat()}")

        if not day_plan.meals:
            st.info("No meals found for this day with the current settings.")
            continue

        for slot in day_plan.meals:
            meal = slot.meal
            tags_display = ", ".join(meal.tags) if meal.tags else "no tags"

            with st.container():
                # Header line
                st.markdown(
                    f"**{slot.time_str} · {meal.meal_type.title()} · {meal.name}**"
                )

                # Scores line
                st.caption(
                    f"Anti-inflammatory score: {meal.anti_inflammatory_score} · "
                    f"Iron support: {meal.iron_support} · "
                    f"Fibre score: {meal.fiber_score}"
                )

                # Tags
                st.caption(f"Tags: {tags_display}")

                # Full recipe: ingredients + step-by-step method
                if meal.ingredients or meal.instructions:
                    with st.expander("📋 View full recipe"):
                        # Ingredients
                        if meal.ingredients:
                            st.markdown("**Ingredients**")
                            for ing in meal.ingredients:
                                amount = ing.get("amount", "").strip()
                                item = ing.get("item", "").strip()
                                if amount:
                                    st.markdown(f"- {amount} {item}")
                                else:
                                    st.markdown(f"- {item}")

                        # Steps
                        if meal.instructions:
                            st.markdown("**Step-by-step**")
                            for idx, step in enumerate(meal.instructions, start=1):
                                st.markdown(f"{idx}. {step}")

        st.markdown("---")

else:
    st.info(
        "Use the controls on the left to pick your fasting pattern and focus, "
        "then click **Generate meal plan 🚀**."
    )
