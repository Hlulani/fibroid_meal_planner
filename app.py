from datetime import date
import random

import streamlit as st

from planner import FASTING_CONFIGS, generate_meal_plan
from meals import MEALS
from fermented import FERMENTED_RECIPES


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Fibroid-Friendly Meal Planner",
    page_icon="🧡",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# =========================
# GLOBAL STATE
# =========================

if "plan_data" not in st.session_state:
    st.session_state["plan_data"] = None

# Determine current tab from query params (?tab=home|plan|recipes)
raw_tab = st.query_params.get("tab", "home")
if isinstance(raw_tab, list):
    current_tab = raw_tab[0] if raw_tab else "home"
else:
    current_tab = raw_tab or "home"

if current_tab not in {"home", "plan", "recipes"}:
    current_tab = "home"


# =========================
# GLOBAL CSS
# =========================

st.markdown(
    """
    <style>
    /* Background + general layout */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #f5f2e9 0%, #ffffff 40%);
        padding-top: 0.5rem;
        padding-bottom: 4rem; /* space for bottom nav */
    }

    .main-block {
        max-width: 860px;
        margin: 0 auto;
    }

    /* Hero card - deep green */
    .hero-card {
        background: linear-gradient(135deg, #446c4a, #31523a);
        padding: 18px 16px;
        border-radius: 22px;
        margin: 10px 0 18px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.18);
        color: #fdfaf4;
    }
    .hero-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 4px;
        color: #fdfaf4;
    }
    .hero-sub {
        font-size: 14px;
        color: #e2e0d8;
    }

    /* Category chips - soft sage */
    .chip-row {
        display: flex;
        gap: 8px;
        overflow-x: auto;
        padding-bottom: 4px;
        margin-bottom: 10px;
    }
    .chip {
        flex: 0 0 auto;
        background: #e4efe6;
        border: 1px solid #c5ddcd;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 12px;
        color: #355b3f;
        white-space: nowrap;
    }

    /* Meal cards - subtle green border */
    .meal-card {
        border-radius: 18px;
        padding: 14px 14px 10px 14px;
        margin-bottom: 8px;
        background: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #e0eadf;
    }
    .meal-header-line {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2px;
    }
    .meal-name {
        font-weight: 600;
        font-size: 15px;
        color: #294534;
    }
    .meal-heart {
        font-size: 14px;
        color: #f4976c;
    }
    .meal-meta {
        font-size: 12px;
        color: #6b7b6f;
        margin-bottom: 4px;
    }
    .meal-tags {
        font-size: 11px;
        color: #9aa99b;
    }

    .day-header {
        margin-top: 1.1rem;
        margin-bottom: 0.4rem;
        font-size: 1.0rem;
        font-weight: 700;
        color: #2d4736;
    }

    /* Bottom navigation bar */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #314a38;  /* deep green */
        border-top: 1px solid #1f3124;
        display: flex;
        justify-content: space-around;
        padding: 6px 10px 10px 10px;
        z-index: 9999;
    }

    .nav-item {
        flex: 1;
        background: transparent;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        padding: 6px 0;
        border-radius: 999px;
        margin: 0 4px;
        cursor: pointer;
        text-decoration: none;
    }

    .nav-icon {
        font-size: 18px;
        margin-bottom: 1px;
    }

    a.nav-item,
    a.nav-item:link,
    a.nav-item:visited {
        color: #d8e5db;
        text-decoration: none;
    }

    a.nav-item.active,
    a.nav-item.active:link,
    a.nav-item.active:visited {
        background: #e4efe6;     /* soft sage pill */
        color: #314a38;
        font-weight: 600;
        text-decoration: none;
    }

    a.nav-item span {
        color: inherit;
        text-decoration: none;
    }

    /* Expander styling – match theme green */
    [data-testid="stExpander"] > details > summary {
        background-color: #314a38 !important;   /* same deep green as bottom nav */
        color: #ffffff !important;
        padding: 10px 14px;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 500;
        list-style: none;
    }

    [data-testid="stExpander"] > details > summary::-webkit-details-marker {
        display: none;
    }

    [data-testid="stExpander"] > details > summary svg {
        stroke: #ffffff !important;
    }

    [data-testid="stExpander"] > details[open] {
        border-left: 3px solid #314a38;
        border-radius: 0 0 8px 8px;
        margin-bottom: 10px;
        background-color: #f6fbf8;
        padding-bottom: 8px;
    }

    @media (max-width: 768px) {
        h1 {
            font-size: 1.6rem !important;
        }
        .hero-title {
            font-size: 20px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# PAGE RENDERERS
# =========================

def render_home() -> None:
    st.markdown('<div class="main-block">', unsafe_allow_html=True)

    # Greeting section
    st.markdown(
        """
        <div style="padding: 10px 0 4px 0; text-align:left;">
            <div style="font-size:13px; color:#6c7a6e;">Good to see you 🌿</div>
            <h2 style="margin: 0; font-size:24px; color:#263a2d;">
                What nourishment shall we choose today?
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hero card
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Fibroid-friendly, anti-inflammatory meals</div>
            <div class="hero-sub">
                Gentle, supportive recipes designed around fasting windows,
                hormones and digestion.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Search bar (visual only)
    _ = st.text_input(
        "Search recipes",
        "",
        placeholder="Search a meal or ingredient (coming soon)…",
        label_visibility="collapsed",
    )

    # Category chips
    st.markdown(
        """
        <div style="margin-top:2px; margin-bottom:4px; font-size:13px; color:#506254;">
            Focus for today
        </div>
        <div class="chip-row">
            <div class="chip">Hormone support</div>
            <div class="chip">Low inflammation</div>
            <div class="chip">Gut reset</div>
            <div class="chip">Iron support</div>
            <div class="chip">Energy boost</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # CTA button → switch to plan tab
    if st.button("✨ Build My Meal Plan", use_container_width=True):
        st.query_params["tab"] = "plan"
        st.rerun()

    # Recommendations (sample 2 meals)
    st.markdown("### Recommended for you today")

    sample_meals = random.sample(MEALS, k=min(2, len(MEALS)))
    for meal in sample_meals:
        tags_display = ", ".join(meal.tags) if meal.tags else "no tags"
        st.markdown(
            f"""
            <div class="meal-card">
                <div class="meal-header-line">
                    <div class="meal-name">{meal.name}</div>
                    <div class="meal-heart">💛</div>
                </div>
                <div class="meal-meta">
                    {meal.meal_type.title()} · 🌿 Anti-inflammatory score: {meal.anti_inflammatory_score}
                </div>
                <div class="meal-tags">
                    Tags: {tags_display}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("👩‍🍳 See full recipe"):
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

    st.markdown("</div>", unsafe_allow_html=True)


def render_plan() -> None:
    st.markdown('<div class="main-block">', unsafe_allow_html=True)

    st.markdown(
        """
        <div style="padding: 10px 0 4px 0; text-align:left;">
            <h2 style="margin: 0; font-size:24px; color:#263a2d;">Your healing plan</h2>
            <div style="font-size:13px; color:#6c7a6e;">
                Tell me how you like to eat and I’ll build a fibroid-supportive plan for you.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("✨ Personalise My Plan", expanded=True):
        st.markdown(
            "Answer these quickly so I can create meals that support your hormones, "
            "digestion and inflammation 💛"
        )

        st.subheader("🕒 Eating style")
        pattern_ids = list(FASTING_CONFIGS.keys())
        selected_pattern_id = st.selectbox(
            "Fasting style",
            options=pattern_ids,
            format_func=lambda pid: FASTING_CONFIGS[pid].label,
        )

        eat_window_start_hour = st.slider(
            "When do you like your first meal?",
            min_value=8,
            max_value=14,
            value=12,
        )

        st.caption(FASTING_CONFIGS[selected_pattern_id].description)

        st.subheader("🎯 Focus areas")
        fibroid_focus = st.checkbox(
            "Support fibroids with fibre & cruciferous veggies", value=True
        )
        anemia_risk = st.checkbox(
            "Support iron levels (for heavy periods / low iron)", value=True
        )

        st.subheader("📆 Plan duration")
        days = st.slider("How many days should I plan for?", 7, 30, 30)

        if st.button("✨ Generate My Healing Plan", use_container_width=True):
            plan = generate_meal_plan(
                days=days,
                fasting_pattern_id=selected_pattern_id,
                eat_window_start_hour=eat_window_start_hour,
                fibroid_focus=fibroid_focus,
                anemia_risk=anemia_risk,
            )
            st.session_state["plan_data"] = plan
            st.success("New plan created. Scroll down to see it 💚")

    plan = st.session_state.get("plan_data")

    if not plan:
        st.info("Once you generate a plan, your meals will appear here.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Today's plan
    today = date.today()
    today_plan = next((p for p in plan if p.day == today), None)

    if today_plan:
        st.markdown("### 🌞 Today’s meals")
        if not today_plan.meals:
            st.write("No meals for today with the current filters.")
        else:
            for slot in today_plan.meals:
                meal = slot.meal
                tags_display = ", ".join(meal.tags) if meal.tags else "no tags"
                st.markdown(
                    f"""
                    <div class="meal-card">
                        <div class="meal-header-line">
                            <div class="meal-name">{slot.time_str} · {meal.name}</div>
                            <div class="meal-heart">🌿</div>
                        </div>
                        <div class="meal-meta">
                            {meal.meal_type.title()} · 🕑 {slot.time_str} ·
                            💪 Iron: {meal.iron_support}/5 ·
                            🌾 Fibre: {meal.fiber_score}/5
                        </div>
                        <div class="meal-tags">
                            Tags: {tags_display}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with st.expander("👩‍🍳 See full recipe"):
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
    else:
        st.markdown("### 🌞 Today’s meals")
        st.write("Your plan doesn’t start today, but you can still view all days below.")

    # Full plan (all days)
    with st.expander("📅 View full plan (all days)"):
        for day_plan in plan:
            st.markdown(
                f'<div class="day-header">📆 {day_plan.day.isoformat()}</div>',
                unsafe_allow_html=True,
            )
            if not day_plan.meals:
                st.write("No meals for this day.")
                continue

            for slot in day_plan.meals:
                meal = slot.meal
                tags_display = ", ".join(meal.tags) if meal.tags else "no tags"

                st.markdown(
                    f"""
                    <div class="meal-card">
                        <div class="meal-header-line">
                            <div class="meal-name">{slot.time_str} · {meal.name}</div>
                            <div class="meal-heart">💚</div>
                        </div>
                        <div class="meal-meta">
                            {meal.meal_type.title()} · 🕑 {slot.time_str} ·
                            🌿 Anti-inflammatory: {meal.anti_inflammatory_score}/5 ·
                            💪 Iron: {meal.iron_support}/5 ·
                            🌾 Fibre: {meal.fiber_score}/5
                        </div>
                        <div class="meal-tags">
                            Tags: {tags_display}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with st.expander("👩‍🍳 See full recipe"):
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

    st.markdown("</div>", unsafe_allow_html=True)


def render_recipes() -> None:
    st.markdown('<div class="main-block">', unsafe_allow_html=True)

    st.markdown(
        """
        <div style="padding: 10px 0 4px 0; text-align:left;">
            <h2 style="margin: 0; font-size:24px; color:#263a2d;">Recipes</h2>
            <div style="font-size:13px; color:#6c7a6e;">
                Browse anti-inflammatory meals or fermented add-ons to boost your gut and hormones.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "What would you like to explore?",
        options=["Meals", "Fermented add-ons"],
        horizontal=True,
    )

    if mode == "Meals":
        col1, col2 = st.columns([2, 1])
        meal_type_filter = col1.selectbox(
            "Meal type",
            ["All", "Breakfast", "Lunch", "Dinner", "Snack"],
        )
        tag_filter = col2.selectbox(
            "Focus",
            ["Any", "anti_inflammatory", "fibroid_friendly", "high_fiber", "iron_rich"],
        )

        for meal in MEALS:
            if meal_type_filter != "All" and meal.meal_type.lower() != meal_type_filter.lower():
                continue
            if tag_filter != "Any" and tag_filter not in meal.tags:
                continue

            tags_display = ", ".join(meal.tags) if meal.tags else "no tags"

            st.markdown(
                f"""
                <div class="meal-card">
                    <div class="meal-header-line">
                        <div class="meal-name">{meal.name}</div>
                        <div class="meal-heart">👩‍🍳</div>
                    </div>
                    <div class="meal-meta">
                        {meal.meal_type.title()} · 🌿 Anti-inflammatory: {meal.anti_inflammatory_score}/5
                        · 💪 Iron: {meal.iron_support}/5
                    </div>
                    <div class="meal-tags">
                        Tags: {tags_display}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("👩‍🍳 See full recipe"):
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
    else:
        st.subheader("Fermented add-ons")
        st.caption(
            "These are small ferments you can prepare ahead and add to meals for extra fibre, "
            "beneficial bacteria and flavour."
        )

        for fr in FERMENTED_RECIPES:
            brine_text = (
                f" · {fr.brine_percent:.1f}% brine" if fr.brine_percent is not None else ""
            )

            st.markdown(
                f"""
                <div class="meal-card">
                    <div class="meal-header-line">
                        <div class="meal-name">{fr.name}</div>
                        <div class="meal-heart">🧪</div>
                    </div>
                    <div class="meal-meta">
                        Ferment · ⏱ At least {fr.min_days} days{brine_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("👩‍🍳 See full recipe"):
                if fr.notes:
                    st.markdown(f"*{fr.notes}*")

                if fr.ingredients:
                    st.markdown("**Ingredients**")
                    for line in fr.ingredients:
                        st.markdown(f"- {line}")

                if fr.steps:
                    st.markdown("**How to make it**")
                    for idx, step in enumerate(fr.steps, start=1):
                        st.markdown(f"{idx}. {step}")

                st.markdown(f"**Fermentation time**: at least {fr.min_days} days.")

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# ROUTING
# =========================

if current_tab == "home":
    render_home()
elif current_tab == "plan":
    render_plan()
elif current_tab == "recipes":
    render_recipes()
else:
    render_home()


# =========================
# BOTTOM NAVIGATION
# =========================

home_class = "nav-item active" if current_tab == "home" else "nav-item"
plan_class = "nav-item active" if current_tab == "plan" else "nav-item"
recipes_class = "nav-item active" if current_tab == "recipes" else "nav-item"

st.markdown(
    f"""
    <div class="bottom-nav">
        <a class="{home_class}" href="?tab=home">
            <span class="nav-icon">🏠</span>
            <span>Home</span>
        </a>
        <a class="{plan_class}" href="?tab=plan">
            <span class="nav-icon">📅</span>
            <span>My Plan</span>
        </a>
        <a class="{recipes_class}" href="?tab=recipes">
            <span class="nav-icon">👩‍🍳</span>
            <span>Recipes</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)


# from datetime import date
# import random
#
# import streamlit as st
#
# from planner import FASTING_CONFIGS, generate_meal_plan
# from meals import MEALS
#
#
# # =========================
# # PAGE CONFIG
# # =========================
#
# st.set_page_config(
#     page_title="Fibroid-Friendly Meal Planner",
#     page_icon="🧡",
#     layout="centered",
#     initial_sidebar_state="collapsed",
# )
#
#
# # =========================
# # GLOBAL STATE
# # =========================
#
# if "plan_data" not in st.session_state:
#     st.session_state["plan_data"] = None
#
# # Get current tab from query params (can be list or str)
# raw_tab = st.query_params.get("tab", "home")
# if isinstance(raw_tab, list):
#     current_tab = raw_tab[0] if raw_tab else "home"
# else:
#     current_tab = raw_tab or "home"
#
# if current_tab not in {"home", "plan", "recipes"}:
#     current_tab = "home"
#
#
# # =========================
# # GLOBAL CSS + NAV JS
# # =========================
#
# st.markdown(
#     """
#     <style>
#     /* Background + general layout */
#     [data-testid="stAppViewContainer"] {
#         background: linear-gradient(180deg, #f5f2e9 0%, #ffffff 40%);
#         padding-top: 0.5rem;
#         padding-bottom: 4rem; /* space for bottom nav */
#     }
#
#     .main-block {
#         max-width: 860px;
#         margin: 0 auto;
#     }
#
#     /* Hero card - deep green */
#     .hero-card {
#         background: linear-gradient(135deg, #446c4a, #31523a);
#         padding: 18px 16px;
#         border-radius: 22px;
#         margin: 10px 0 18px 0;
#         box-shadow: 0 4px 12px rgba(0,0,0,0.18);
#         color: #fdfaf4;
#     }
#     .hero-title {
#         font-size: 22px;
#         font-weight: 700;
#         margin-bottom: 4px;
#         color: #fdfaf4;
#     }
#     .hero-sub {
#         font-size: 14px;
#         color: #e2e0d8;
#     }
#
#     /* Category chips - soft sage */
#     .chip-row {
#         display: flex;
#         gap: 8px;
#         overflow-x: auto;
#         padding-bottom: 4px;
#         margin-bottom: 10px;
#     }
#     .chip {
#         flex: 0 0 auto;
#         background: #e4efe6;
#         border: 1px solid #c5ddcd;
#         padding: 6px 12px;
#         border-radius: 999px;
#         font-size: 12px;
#         color: #355b3f;
#         white-space: nowrap;
#     }
#
#     /* Meal cards - subtle green border */
#     .meal-card {
#         border-radius: 18px;
#         padding: 14px 14px 10px 14px;
#         margin-bottom: 8px;
#         background: #ffffff;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.04);
#         border: 1px solid #e0eadf;
#     }
#     .meal-header-line {
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         margin-bottom: 2px;
#     }
#     .meal-name {
#         font-weight: 600;
#         font-size: 15px;
#         color: #294534;
#     }
#     .meal-heart {
#         font-size: 14px;
#         color: #f4976c;
#     }
#     .meal-meta {
#         font-size: 12px;
#         color: #6b7b6f;
#         margin-bottom: 4px;
#     }
#     .meal-tags {
#         font-size: 11px;
#         color: #9aa99b;
#     }
#
#     .day-header {
#         margin-top: 1.1rem;
#         margin-bottom: 0.4rem;
#         font-size: 1.0rem;
#         font-weight: 700;
#         color: #2d4736;
#     }
#
#     /* Bottom navigation bar - aligned with green theme */
#     .bottom-nav {
#         position: fixed;
#         bottom: 0;
#         left: 0;
#         right: 0;
#         background: #314a38;  /* deep green bar */
#         border-top: 1px solid #1f3124;
#         display: flex;
#         justify-content: space-around;
#         padding: 6px 10px 10px 10px;
#         z-index: 9999;
#     }
#     .nav-item {
#     flex: 1;
#     background: transparent;
#     display: flex;
#     flex-direction: column;
#     align-items: center;
#     justify-content: center;
#     font-size: 11px;
#     padding: 6px 0;
#     border-radius: 999px;
#     margin: 0 4px;
#     cursor: pointer;
#
#     /* remove link styling */
#     text-decoration: none;
#     color: #e6f0e7 !important;
# }
#
# /* active pill */
# .nav-item.active {
#     background: #e4efe6;  /* soft sage */
#     color: #314a38 !important; /* dark green text */
#     font-weight: 600;
# }
#
# /* ensure icons and text adopt the correct theme */
# .nav-item span {
#     text-decoration: none !important;
#     color: inherit !important;
# }
#
#
#
#     .nav-icon {
#         font-size: 18px;
#         margin-bottom: 1px;
#     }
#
#     @media (max-width: 768px) {
#         h1 {
#             font-size: 1.6rem !important;
#         }
#         .hero-title {
#             font-size: 20px;
#         }
#     }
#     </style>
#
#
#     """,
#     unsafe_allow_html=True,
# )
#
#
# # =========================
# # PAGE RENDERERS
# # =========================
#
# def render_home() -> None:
#     st.markdown('<div class="main-block">', unsafe_allow_html=True)
#
#     # Greeting section
#     st.markdown(
#         """
#         <div style="padding: 10px 0 4px 0; text-align:left;">
#             <div style="font-size:13px; color:#6c7a6e;">Good to see you 🌿</div>
#             <h2 style="margin: 0; font-size:24px; color:#263a2d;">
#                 What nourishment shall we choose today?
#             </h2>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#
#     # Hero card
#     st.markdown(
#         """
#         <div class="hero-card">
#             <div class="hero-title">Fibroid-friendly, anti-inflammatory meals</div>
#             <div class="hero-sub">
#                 Gentle, supportive recipes designed around fasting windows,
#                 hormones and digestion.
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#
#     # Search bar (visual only for now)
#     _ = st.text_input(
#         "Search recipes",
#         "",
#         placeholder="Search a meal or ingredient (coming soon)…",
#         label_visibility="collapsed",
#     )
#
#     # Category chips
#     st.markdown(
#         """
#         <div style="margin-top:2px; margin-bottom:4px; font-size:13px; color:#506254;">
#             Focus for today
#         </div>
#         <div class="chip-row">
#             <div class="chip">Hormone support</div>
#             <div class="chip">Low inflammation</div>
#             <div class="chip">Gut reset</div>
#             <div class="chip">Iron support</div>
#             <div class="chip">Energy boost</div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#
#     # CTA button → switch to plan tab
#     if st.button("✨ Build My Meal Plan", use_container_width=True):
#         st.query_params["tab"] = "plan"
#         st.rerun()
#
#     # Recommendations (sample 2 meals)
#     st.markdown("### Recommended for you today")
#
#     sample_meals = random.sample(MEALS, k=min(2, len(MEALS)))
#     for meal in sample_meals:
#         tags_display = ", ".join(meal.tags) if meal.tags else "no tags"
#         st.markdown(
#             f"""
#             <div class="meal-card">
#                 <div class="meal-header-line">
#                     <div class="meal-name">{meal.name}</div>
#                     <div class="meal-heart">💛</div>
#                 </div>
#                 <div class="meal-meta">
#                     {meal.meal_type.title()} · 🌿 Anti-inflammatory score: {meal.anti_inflammatory_score}
#                 </div>
#                 <div class="meal-tags">
#                     Tags: {tags_display}
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
#
#         with st.expander("👩‍🍳 See full recipe"):
#             if meal.ingredients:
#                 st.markdown("**Ingredients**")
#                 for ing in meal.ingredients:
#                     amount = ing.get("amount", "").strip()
#                     item = ing.get("item", "").strip()
#                     if amount:
#                         st.markdown(f"- {amount} {item}")
#                     else:
#                         st.markdown(f"- {item}")
#
#             if meal.instructions:
#                 st.markdown("**Step-by-step**")
#                 for idx, step in enumerate(meal.instructions, start=1):
#                     st.markdown(f"{idx}. {step}")
#
#     st.markdown("</div>", unsafe_allow_html=True)
#
#
# def render_plan() -> None:
#     st.markdown('<div class="main-block">', unsafe_allow_html=True)
#
#     st.markdown(
#         """
#         <div style="padding: 10px 0 4px 0; text-align:left;">
#             <h2 style="margin: 0; font-size:24px; color:#263a2d;">Your healing plan</h2>
#             <div style="font-size:13px; color:#6c7a6e;">
#                 Tell me how you like to eat and I’ll build a fibroid-supportive plan for you.
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#
#     with st.expander("✨ Personalise My Plan", expanded=True):
#         st.markdown(
#             "Answer these quickly so I can create meals that support your hormones, "
#             "digestion and inflammation 💛"
#         )
#
#         st.subheader("🕒 Eating style")
#         pattern_ids = list(FASTING_CONFIGS.keys())
#         selected_pattern_id = st.selectbox(
#             "Fasting style",
#             options=pattern_ids,
#             format_func=lambda pid: FASTING_CONFIGS[pid].label,
#         )
#
#         eat_window_start_hour = st.slider(
#             "When do you like your first meal?",
#             min_value=8,
#             max_value=14,
#             value=12,
#         )
#
#         st.caption(FASTING_CONFIGS[selected_pattern_id].description)
#
#         st.subheader("🎯 Focus areas")
#         fibroid_focus = st.checkbox("Support fibroids with fibre & cruciferous veggies", value=True)
#         anemia_risk = st.checkbox("Support iron levels (for heavy periods / low iron)", value=True)
#
#         st.subheader("📆 Plan duration")
#         days = st.slider("How many days should I plan for?", 7, 30, 30)
#
#         if st.button("✨ Generate My Healing Plan", use_container_width=True):
#             plan = generate_meal_plan(
#                 days=days,
#                 fasting_pattern_id=selected_pattern_id,
#                 eat_window_start_hour=eat_window_start_hour,
#                 fibroid_focus=fibroid_focus,
#                 anemia_risk=anemia_risk,
#             )
#             st.session_state["plan_data"] = plan
#             st.success("New plan created. Scroll down to see it 💚")
#
#     plan = st.session_state.get("plan_data")
#
#     if not plan:
#         st.info("Once you generate a plan, your meals will appear here.")
#         st.markdown("</div>", unsafe_allow_html=True)
#         return
#
#     # Today's plan
#     today = date.today()
#     today_plan = next((p for p in plan if p.day == today), None)
#
#     if today_plan:
#         st.markdown("### 🌞 Today’s meals")
#         if not today_plan.meals:
#             st.write("No meals for today with the current filters.")
#         else:
#             for slot in today_plan.meals:
#                 meal = slot.meal
#                 tags_display = ", ".join(meal.tags) if meal.tags else "no tags"
#                 st.markdown(
#                     f"""
#                     <div class="meal-card">
#                         <div class="meal-header-line">
#                             <div class="meal-name">{slot.time_str} · {meal.name}</div>
#                             <div class="meal-heart">🌿</div>
#                         </div>
#                         <div class="meal-meta">
#                             {meal.meal_type.title()} · 🕑 {slot.time_str} ·
#                             💪 Iron: {meal.iron_support}/5 ·
#                             🌾 Fibre: {meal.fiber_score}/5
#                         </div>
#                         <div class="meal-tags">
#                             Tags: {tags_display}
#                         </div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )
#
#                 with st.expander("👩‍🍳 See full recipe"):
#                     if meal.ingredients:
#                         st.markdown("**Ingredients**")
#                         for ing in meal.ingredients:
#                             amount = ing.get("amount", "").strip()
#                             item = ing.get("item", "").strip()
#                             if amount:
#                                 st.markdown(f"- {amount} {item}")
#                             else:
#                                 st.markdown(f"- {item}")
#
#                     if meal.instructions:
#                         st.markdown("**Step-by-step**")
#                         for idx, step in enumerate(meal.instructions, start=1):
#                             st.markdown(f"{idx}. {step}")
#     else:
#         st.markdown("### 🌞 Today’s meals")
#         st.write("Your plan doesn’t start today, but you can still view all days below.")
#
#     # Full plan (all days)
#     with st.expander("📅 View full plan (all days)"):
#         for day_plan in plan:
#             st.markdown(
#                 f'<div class="day-header">📆 {day_plan.day.isoformat()}</div>',
#                 unsafe_allow_html=True,
#             )
#             if not day_plan.meals:
#                 st.write("No meals for this day.")
#                 continue
#
#             for slot in day_plan.meals:
#                 meal = slot.meal
#                 tags_display = ", ".join(meal.tags) if meal.tags else "no tags"
#
#                 st.markdown(
#                     f"""
#                     <div class="meal-card">
#                         <div class="meal-header-line">
#                             <div class="meal-name">{slot.time_str} · {meal.name}</div>
#                             <div class="meal-heart">💚</div>
#                         </div>
#                         <div class="meal-meta">
#                             {meal.meal_type.title()} · 🕑 {slot.time_str} ·
#                             🌿 Anti-inflammatory: {meal.anti_inflammatory_score}/5 ·
#                             💪 Iron: {meal.iron_support}/5 ·
#                             🌾 Fibre: {meal.fiber_score}/5
#                         </div>
#                         <div class="meal-tags">
#                             Tags: {tags_display}
#                         </div>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )
#
#                 with st.expander("👩‍🍳 See full recipe"):
#                     if meal.ingredients:
#                         st.markdown("**Ingredients**")
#                         for ing in meal.ingredients:
#                             amount = ing.get("amount", "").strip()
#                             item = ing.get("item", "").strip()
#                             if amount:
#                                 st.markdown(f"- {amount} {item}")
#                             else:
#                                 st.markdown(f"- {item}")
#
#                     if meal.instructions:
#                         st.markdown("**Step-by-step**")
#                         for idx, step in enumerate(meal.instructions, start=1):
#                             st.markdown(f"{idx}. {step}")
#
#     st.markdown("</div>", unsafe_allow_html=True)
#
#
# def render_recipes() -> None:
#     st.markdown('<div class="main-block">', unsafe_allow_html=True)
#
#     st.markdown(
#         """
#         <div style="padding: 10px 0 4px 0; text-align:left;">
#             <h2 style="margin: 0; font-size:24px; color:#263a2d;">All recipes</h2>
#             <div style="font-size:13px; color:#6c7a6e;">
#                 Browse each meal and see ingredients and step-by-step instructions.
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#
#     col1, col2 = st.columns([2, 1])
#     meal_type_filter = col1.selectbox(
#         "Meal type",
#         ["All", "Breakfast", "Lunch", "Dinner", "Snack"],
#     )
#     tag_filter = col2.selectbox(
#         "Focus",
#         ["Any", "anti_inflammatory", "fibroid_friendly", "high_fiber", "iron_rich"],
#     )
#
#     for meal in MEALS:
#         if meal_type_filter != "All" and meal.meal_type.lower() != meal_type_filter.lower():
#             continue
#         if tag_filter != "Any" and tag_filter not in meal.tags:
#             continue
#
#         tags_display = ", ".join(meal.tags) if meal.tags else "no tags"
#
#         st.markdown(
#             f"""
#             <div class="meal-card">
#                 <div class="meal-header-line">
#                     <div class="meal-name">{meal.name}</div>
#                     <div class="meal-heart">👩‍🍳</div>
#                 </div>
#                 <div class="meal-meta">
#                     {meal.meal_type.title()} · 🌿 Anti-inflammatory: {meal.anti_inflammatory_score}/5
#                     · 💪 Iron: {meal.iron_support}/5
#                 </div>
#                 <div class="meal-tags">
#                     Tags: {tags_display}
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
#
#         with st.expander("👩‍🍳 See full recipe"):
#             if meal.ingredients:
#                 st.markdown("**Ingredients**")
#                 for ing in meal.ingredients:
#                     amount = ing.get("amount", "").strip()
#                     item = ing.get("item", "").strip()
#                     if amount:
#                         st.markdown(f"- {amount} {item}")
#                     else:
#                         st.markdown(f"- {item}")
#
#             if meal.instructions:
#                 st.markdown("**Step-by-step**")
#                 for idx, step in enumerate(meal.instructions, start=1):
#                     st.markdown(f"{idx}. {step}")
#
#     st.markdown("</div>", unsafe_allow_html=True)
#
#
# # =========================
# # ROUTING
# # =========================
#
# if current_tab == "home":
#     render_home()
# elif current_tab == "plan":
#     render_plan()
# elif current_tab == "recipes":
#     render_recipes()
# else:
#     render_home()
#
#
# # =========================
# # BOTTOM NAVIGATION
# # =========================
#
# home_class = "nav-item active" if current_tab == "home" else "nav-item"
# plan_class = "nav-item active" if current_tab == "plan" else "nav-item"
# recipes_class = "nav-item active" if current_tab == "recipes" else "nav-item"
#
# st.markdown(
#     f"""
#     <div class="bottom-nav">
#         <a class="{home_class}" href="?tab=home">
#             <span class="nav-icon">🏠</span>
#             <span>Home</span>
#         </a>
#         <a class="{plan_class}" href="?tab=plan">
#             <span class="nav-icon">📅</span>
#             <span>My Plan</span>
#         </a>
#         <a class="{recipes_class}" href="?tab=recipes">
#             <span class="nav-icon">👩‍🍳</span>
#             <span>Recipes</span>
#         </a>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# ===========================================================

#
# import streamlit as st
#
# from planner import (
#     FASTING_CONFIGS,
#     generate_meal_plan,
# )
# from meals import MEALS
#
#
# # =========================
# # BASE CONFIG
# # =========================
#
# st.set_page_config(
#     page_title="Fibroid-Friendly Meal Planner",
#     page_icon="🧡",
#     layout="centered",
#     initial_sidebar_state="collapsed",
# )
#
# # =========================
# # GLOBAL CSS (MOBILE FIRST)
# # =========================
#
# st.markdown(
#     """
#     <style>
#     .main-block {
#         max-width: 800px;
#         margin: 0 auto;
#     }
#
#     .meal-card {
#         border-radius: 12px;
#         padding: 0.75rem 0.9rem;
#         margin-bottom: 0.75rem;
#         background: #ffffff10;
#         border: 1px solid #ffffff20;
#     }
#
#     .meal-header {
#         font-weight: 600;
#         margin-bottom: 0.1rem;
#     }
#
#     .meal-meta {
#         font-size: 0.8rem;
#         color: #888;
#         margin-bottom: 0.25rem;
#     }
#
#     .meal-tags {
#         font-size: 0.8rem;
#         color: #aaa;
#     }
#
#     .day-header {
#         margin-top: 1.25rem;
#         margin-bottom: 0.5rem;
#         font-size: 1.05rem;
#         font-weight: 700;
#     }
#
#     [data-testid="stAppViewContainer"] {
#         padding-top: 0.5rem;
#         padding-bottom: 1.5rem;
#     }
#
#     @media (max-width: 768px) {
#         h1 {
#             font-size: 1.6rem !important;
#         }
#         .day-header {
#             font-size: 1rem;
#         }
#         .meal-header {
#             font-size: 0.95rem;
#         }
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
#
# # =========================
# # TITLE / INTRO
# # =========================
#
# st.markdown('<div class="main-block">', unsafe_allow_html=True)
#
# st.title("🧡 Fibroid-Friendly Anti-Inflammatory Planner")
#
# st.markdown(
#     """
# This planner creates **anti-inflammatory, fibroid-supporting meal days**
# while respecting your **fasting window**.
#
# > This is not medical advice. Always work with your doctor for diagnosis and treatment.
# """
# )
#
# # =========================
# # SETTINGS (NO SIDEBAR)
# # =========================
#
# with st.expander("✨ Personalise My Plan", expanded=True):
#     st.write(
#         "Choose your fasting style and focus areas so I can build a supportive meal plan for you ✨"
#     )
#
#     col1, col2 = st.columns(2)
#
#     pattern_ids = list(FASTING_CONFIGS.keys())
#     selected_pattern_id = col1.selectbox(
#         "Fasting pattern",
#         options=pattern_ids,
#         format_func=lambda pid: FASTING_CONFIGS[pid].label,
#     )
#
#     eat_window_start_hour = col2.slider(
#         "Eating window start (hour)",
#         min_value=8,
#         max_value=14,
#         value=12,
#         help="Hour of your first meal in the day. For 16:8 with 2 meals, 11–13 works well.",
#     )
#
#     st.caption(FASTING_CONFIGS[selected_pattern_id].description)
#
#     fibroid_focus = st.checkbox(
#         "Prioritise fibroid support (fibre, cruciferous, liver support)",
#         value=True,
#     )
#
#     anemia_risk = st.checkbox(
#         "Prioritise iron-support meals",
#         value=True,
#     )
#
#     days = st.slider(
#         "Days to plan",
#         min_value=7,
#         max_value=30,
#         value=30,
#     )
#
#     st.markdown(f"Meals in database: **{len(MEALS)}**")
#
#     generate_clicked = st.button("Generate meal plan 🚀", use_container_width=True)
#
# # =========================
# # MAIN CONTENT
# # =========================
#
# if generate_clicked:
#     plan = generate_meal_plan(
#         days=days,
#         fasting_pattern_id=selected_pattern_id,
#         eat_window_start_hour=eat_window_start_hour,
#         fibroid_focus=fibroid_focus,
#         anemia_risk=anemia_risk,
#     )
#
#     st.subheader(f"📅 Your {days}-day plan")
#
#     for day_plan in plan:
#         # Day header
#         st.markdown(
#             f'<div class="day-header">📆 {day_plan.day.isoformat()}</div>',
#             unsafe_allow_html=True,
#         )
#
#         if not day_plan.meals:
#             st.info("No meals found for this day with the current settings.")
#             continue
#
#         for slot in day_plan.meals:
#             meal = slot.meal
#             tags_display = ", ".join(meal.tags) if meal.tags else "no tags"
#
#             # Card wrapper
#             st.markdown('<div class="meal-card">', unsafe_allow_html=True)
#
#             # Header line
#             st.markdown(
#                 f'<div class="meal-header">{slot.time_str} · '
#                 f'{meal.meal_type.title()} · {meal.name}</div>',
#                 unsafe_allow_html=True,
#             )
#
#             # Scores line
#             st.markdown(
#                 f'<div class="meal-meta">'
#                 f'Anti-inflammatory score: {meal.anti_inflammatory_score} · '
#                 f'Iron support: {meal.iron_support} · '
#                 f'Fibre score: {meal.fiber_score}'
#                 f'</div>',
#                 unsafe_allow_html=True,
#             )
#
#             # Tags
#             st.markdown(
#                 f'<div class="meal-tags">Tags: {tags_display}</div>',
#                 unsafe_allow_html=True,
#             )
#
#             # Full recipe in expander
#             if meal.ingredients or meal.instructions:
#                 with st.expander("📋 How to make this"):
#                     if meal.ingredients:
#                         st.markdown("**Ingredients**")
#                         for ing in meal.ingredients:
#                             amount = ing.get("amount", "").strip()
#                             item = ing.get("item", "").strip()
#                             if amount:
#                                 st.markdown(f"- {amount} {item}")
#                             else:
#                                 st.markdown(f"- {item}")
#
#                     if meal.instructions:
#                         st.markdown("**Step-by-step**")
#                         for idx, step in enumerate(meal.instructions, start=1):
#                             st.markdown(f"{idx}. {step}")
#
#             st.markdown("</div>", unsafe_allow_html=True)  # close meal-card
#
#         st.markdown("---")
#
# else:
#     st.info(
#         "Adjust your settings above, then tap **Generate meal plan 🚀**."
#     )
#
# st.markdown("</div>", unsafe_allow_html=True)  # close main-block
#



# import streamlit as st
#
# from planner import (
#     FASTING_CONFIGS,
#     generate_meal_plan,
# )
# from meals import MEALS
#
# # =========================
# # BASE CONFIG
# # =========================
#
# st.set_page_config(
#     page_title="Fibroid-Friendly Meal Planner",
#     page_icon="🧡",
#     layout="centered",
# )
#
# # =========================
# # GLOBAL CSS + JS (MOBILE MENU + STYLING)
# # =========================
#
# st.markdown(
#     """
#     <style>
#     /* Hide default tiny sidebar toggle */
#     button[data-testid="baseButton-secondary"] {
#         display: none !important;
#     }
#
#     /* Floating menu button */
#     .menu-toggle {
#         position: fixed;
#         top: 12px;
#         left: 12px;
#         background: #ff6b6b;
#         color: white;
#         padding: 10px 14px;
#         font-size: 14px;
#         border-radius: 10px;
#         font-weight: 600;
#         border: none;
#         box-shadow: 0px 2px 6px rgba(0,0,0,0.25);
#         z-index: 9999;
#     }
#
#     /* Only show on small screens */
#     @media (min-width: 768px) {
#         .menu-toggle {
#             display: none;
#         }
#     }
#
#     /* Slide animation for the sidebar */
#     [data-testid="stSidebar"] {
#         transition: transform 0.3s ease-in-out;
#     }
#
#     /* Main content width */
#     .main-block {
#         max-width: 800px;
#         margin: 0 auto;
#     }
#
#     /* Card styling for each meal */
#     .meal-card {
#         border-radius: 12px;
#         padding: 0.75rem 0.9rem;
#         margin-bottom: 0.75rem;
#         background: #ffffff10;
#         border: 1px solid #ffffff20;
#     }
#
#     .meal-header {
#         font-weight: 600;
#         margin-bottom: 0.1rem;
#     }
#
#     .meal-meta {
#         font-size: 0.8rem;
#         color: #888;
#         margin-bottom: 0.25rem;
#     }
#
#     .meal-tags {
#         font-size: 0.8rem;
#         color: #aaa;
#     }
#
#     .day-header {
#         margin-top: 1.25rem;
#         margin-bottom: 0.5rem;
#         font-size: 1.05rem;
#         font-weight: 700;
#     }
#
#     /* Tighter padding on the whole app */
#     [data-testid="stAppViewContainer"] {
#         padding-top: 0.5rem;
#         padding-bottom: 1.5rem;
#     }
#
#     /* Smaller headings on mobile */
#     @media (max-width: 768px) {
#         h1 {
#             font-size: 1.6rem !important;
#         }
#         .day-header {
#             font-size: 1rem;
#         }
#         .meal-header {
#             font-size: 0.95rem;
#         }
#     }
#     </style>
#
#     <script>
#     (function() {
#         function setupSidebar() {
#             const sidebar = document.querySelector("[data-testid='stSidebar']");
#             if (!sidebar) return;
#
#             // Avoid duplicate button on reruns
#             if (document.querySelector(".menu-toggle")) return;
#
#             // Start with sidebar hidden off-screen on mobile
#             sidebar.style.transform = "translateX(-300px)";
#
#             function isOpen() {
#                 return sidebar.style.transform === "translateX(0px)";
#             }
#
#             function toggleSidebar(forceOpen) {
#                 if (typeof forceOpen === "boolean") {
#                     sidebar.style.transform = forceOpen
#                         ? "translateX(0px)"
#                         : "translateX(-300px)";
#                 } else {
#                     sidebar.style.transform = isOpen()
#                         ? "translateX(-300px)"
#                         : "translateX(0px)";
#                 }
#             }
#
#             // Create floating menu button
#             const btn = document.createElement("button");
#             btn.innerText = "☰ Menu";
#             btn.className = "menu-toggle";
#             btn.type = "button";
#             btn.addEventListener("click", function(e) {
#                 e.stopPropagation();
#                 toggleSidebar();
#             });
#             document.body.appendChild(btn);
#
#             // Swipe detection
#             let touchStartX = 0;
#             let touchStartY = 0;
#
#             document.addEventListener("touchstart", function(e) {
#                 if (!e.touches || e.touches.length === 0) return;
#                 touchStartX = e.touches[0].clientX;
#                 touchStartY = e.touches[0].clientY;
#             }, { passive: true });
#
#             document.addEventListener("touchend", function(e) {
#                 if (!e.changedTouches || e.changedTouches.length === 0) return;
#                 const dx = e.changedTouches[0].clientX - touchStartX;
#                 const dy = e.changedTouches[0].clientY - touchStartY;
#
#                 // Ignore mostly vertical swipes or tiny moves
#                 if (Math.abs(dx) < 50 || Math.abs(dx) < Math.abs(dy)) return;
#
#                 // Swipe right from left edge to open
#                 if (dx > 50 && touchStartX < 40) {
#                     toggleSidebar(true);
#                 }
#
#                 // Swipe left anywhere to close
#                 if (dx < -50) {
#                     toggleSidebar(false);
#                 }
#             }, { passive: true });
#         }
#
#         // Wait until Streamlit has rendered sidebar
#         const interval = setInterval(function() {
#             if (document.readyState !== "complete") return;
#             setupSidebar();
#         }, 500);
#
#         // Stop checking after a while
#         setTimeout(function() { clearInterval(interval); }, 10000);
#     })();
#     </script>
#     """,
#     unsafe_allow_html=True,
# )
#
# # =========================
# # TITLE / INTRO
# # =========================
#
# st.markdown('<div class="main-block">', unsafe_allow_html=True)
#
# st.title("🧡 Fibroid-Friendly Anti-Inflammatory Planner")
#
# st.markdown(
#     """
# This planner creates **anti-inflammatory, fibroid-supporting meal days** that
# respect your **fasting window**.
#
# > This is not medical advice. Always work with your doctor for diagnosis and treatment.
# """
# )
#
# # =========================
# # SIDEBAR CONTROLS
# # =========================
#
# st.sidebar.header("Settings")
#
# pattern_ids = list(FASTING_CONFIGS.keys())
# selected_pattern_id = st.sidebar.selectbox(
#     "Fasting pattern",
#     options=pattern_ids,
#     format_func=lambda pid: FASTING_CONFIGS[pid].label,
# )
#
# st.sidebar.caption(FASTING_CONFIGS[selected_pattern_id].description)
#
# eat_window_start_hour = st.sidebar.slider(
#     "Eating window start (hour)",
#     min_value=8,
#     max_value=14,
#     value=12,
#     help="Hour of your first meal in the day. For 16:8 with 2 meals, 11 to 13 works well.",
# )
#
# fibroid_focus = st.sidebar.checkbox(
#     "Prioritise fibroid support (fibre, cruciferous, liver support)",
#     value=True,
# )
#
# anemia_risk = st.sidebar.checkbox(
#     "Prioritise iron-support meals",
#     value=True,
# )
#
# days = st.sidebar.slider(
#     "Days to plan",
#     min_value=7,
#     max_value=30,
#     value=30,
# )
#
# st.sidebar.markdown("---")
# st.sidebar.markdown(f"Meals in database: **{len(MEALS)}**")
#
# generate_clicked = st.sidebar.button("Generate meal plan 🚀")
#
# # =========================
# # MAIN CONTENT
# # =========================
#
# if generate_clicked:
#     plan = generate_meal_plan(
#         days=days,
#         fasting_pattern_id=selected_pattern_id,
#         eat_window_start_hour=eat_window_start_hour,
#         fibroid_focus=fibroid_focus,
#         anemia_risk=anemia_risk,
#     )
#
#     st.subheader(f"📅 Your {days}-day plan")
#
#     for day_plan in plan:
#         # Day header
#         st.markdown(
#             f'<div class="day-header">📆 {day_plan.day.isoformat()}</div>',
#             unsafe_allow_html=True,
#         )
#
#         if not day_plan.meals:
#             st.info("No meals found for this day with the current settings.")
#             continue
#
#         for slot in day_plan.meals:
#             meal = slot.meal
#             tags_display = ", ".join(meal.tags) if meal.tags else "no tags"
#
#             # Card wrapper
#             st.markdown('<div class="meal-card">', unsafe_allow_html=True)
#
#             # Header line
#             st.markdown(
#                 f'<div class="meal-header">{slot.time_str} · '
#                 f'{meal.meal_type.title()} · {meal.name}</div>',
#                 unsafe_allow_html=True,
#             )
#
#             # Scores line
#             st.markdown(
#                 f'<div class="meal-meta">'
#                 f'Anti-inflammatory score: {meal.anti_inflammatory_score} · '
#                 f'Iron support: {meal.iron_support} · '
#                 f'Fibre score: {meal.fiber_score}'
#                 f'</div>',
#                 unsafe_allow_html=True,
#             )
#
#             # Tags
#             st.markdown(
#                 f'<div class="meal-tags">Tags: {tags_display}</div>',
#                 unsafe_allow_html=True,
#             )
#
#             # Full recipe in expander
#             if meal.ingredients or meal.instructions:
#                 with st.expander("📋 How to make this"):
#                     if meal.ingredients:
#                         st.markdown("**Ingredients**")
#                         for ing in meal.ingredients:
#                             amount = ing.get("amount", "").strip()
#                             item = ing.get("item", "").strip()
#                             if amount:
#                                 st.markdown(f"- {amount} {item}")
#                             else:
#                                 st.markdown(f"- {item}")
#
#                     if meal.instructions:
#                         st.markdown("**Step-by-step**")
#                         for idx, step in enumerate(meal.instructions, start=1):
#                             st.markdown(f"{idx}. {step}")
#
#             st.markdown("</div>", unsafe_allow_html=True)  # close meal-card
#
#         st.markdown("---")
#
# else:
#     st.info(
#         "Use the sidebar to choose your fasting pattern and focus, "
#         "then tap **Generate meal plan 🚀**."
#     )
#
# st.markdown("</div>", unsafe_allow_html=True)  # close main-block
