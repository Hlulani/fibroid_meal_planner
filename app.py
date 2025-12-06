
import streamlit as st

from planner import (
    FASTING_CONFIGS,
    generate_meal_plan,
)
from meals import MEALS


# =========================
# BASE CONFIG
# =========================

st.set_page_config(
    page_title="Fibroid-Friendly Meal Planner",
    page_icon="🧡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================
# GLOBAL CSS (MOBILE FIRST)
# =========================

st.markdown(
    """
    <style>
    .main-block {
        max-width: 800px;
        margin: 0 auto;
    }

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

    .day-header {
        margin-top: 1.25rem;
        margin-bottom: 0.5rem;
        font-size: 1.05rem;
        font-weight: 700;
    }

    [data-testid="stAppViewContainer"] {
        padding-top: 0.5rem;
        padding-bottom: 1.5rem;
    }

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

# =========================
# TITLE / INTRO
# =========================

st.markdown('<div class="main-block">', unsafe_allow_html=True)

st.title("🧡 Fibroid-Friendly Anti-Inflammatory Planner")

st.markdown(
    """
This planner creates **anti-inflammatory, fibroid-supporting meal days**
while respecting your **fasting window**.

> This is not medical advice. Always work with your doctor for diagnosis and treatment.
"""
)

# =========================
# SETTINGS (NO SIDEBAR)
# =========================

with st.expander("✨ Personalise My Plan", expanded=True):
    st.write(
        "Choose your fasting style and focus areas so I can build a supportive meal plan for you ✨"
    )

    col1, col2 = st.columns(2)

    pattern_ids = list(FASTING_CONFIGS.keys())
    selected_pattern_id = col1.selectbox(
        "Fasting pattern",
        options=pattern_ids,
        format_func=lambda pid: FASTING_CONFIGS[pid].label,
    )

    eat_window_start_hour = col2.slider(
        "Eating window start (hour)",
        min_value=8,
        max_value=14,
        value=12,
        help="Hour of your first meal in the day. For 16:8 with 2 meals, 11–13 works well.",
    )

    st.caption(FASTING_CONFIGS[selected_pattern_id].description)

    fibroid_focus = st.checkbox(
        "Prioritise fibroid support (fibre, cruciferous, liver support)",
        value=True,
    )

    anemia_risk = st.checkbox(
        "Prioritise iron-support meals",
        value=True,
    )

    days = st.slider(
        "Days to plan",
        min_value=7,
        max_value=30,
        value=30,
    )

    st.markdown(f"Meals in database: **{len(MEALS)}**")

    generate_clicked = st.button("Generate meal plan 🚀", use_container_width=True)

# =========================
# MAIN CONTENT
# =========================

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

            # Card wrapper
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

            # Full recipe in expander
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

            st.markdown("</div>", unsafe_allow_html=True)  # close meal-card

        st.markdown("---")

else:
    st.info(
        "Adjust your settings above, then tap **Generate meal plan 🚀**."
    )

st.markdown("</div>", unsafe_allow_html=True)  # close main-block




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
