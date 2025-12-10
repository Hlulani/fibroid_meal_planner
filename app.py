
import os
from datetime import date
import random
from typing import List

import streamlit as st

from planner import FASTING_CONFIGS, generate_meal_plan
from meals import MEALS
from fermented import FERMENTED_RECIPES


# =========================
# OPTIONAL OLLAMA CLIENT
# =========================

OLLAMA_AVAILABLE = False
try:
    from ollama import Client  # type: ignore

    # ollama_client = Client(host="http://localhost:11434")
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_client = Client(host=ollama_host)

    OLLAMA_AVAILABLE = True
except Exception:
    ollama_client = None
    OLLAMA_AVAILABLE = False


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
if "hero_index" not in st.session_state:
    st.session_state["hero_index"] = 0
if "ai_recipe" not in st.session_state:
    st.session_state["ai_recipe"] = None

# Determine current tab from query params (?tab=home|plan|recipes|ai)
raw_tab = st.query_params.get("tab", "home")
if isinstance(raw_tab, list):
    current_tab = raw_tab[0] if raw_tab else "home"
else:
    current_tab = raw_tab or "home"

if current_tab not in {"home", "plan", "recipes", "ai"}:
    current_tab = "home"


# =========================
# HERO IMAGES (CAROUSEL)
# =========================

HERO_IMAGES = [
    {
        "title": "Healthy organic bowl",
        "subtitle": "Leafy greens, good fats and fibre-rich veggies.",
        "url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "title": "Rainbow anti-inflammatory plate",
        "subtitle": "Colourful plants to calm inflammation and support hormones.",
        "url": "https://images.unsplash.com/photo-1543353071-873f17a7a088?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "title": "Nourishing veggie board",
        "subtitle": "Cruciferous veg, healthy oils and real food ingredients.",
        "url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=1200&q=80",
    },
]


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

    /* Hero image card (carousel) */
    .hero-image-card {
        background: #f6fbf8;
        border-radius: 24px;
        padding: 10px 10px 12px 10px;
        margin: 4px 0 14px 0;
        box-shadow: 0 4px 14px rgba(0,0,0,0.10);
        border: 1px solid #d4e4d8;
    }
    .hero-image-card img.hero-image {
        width: 100%;
        border-radius: 20px;
        object-fit: cover;
        max-height: 260px;
    }
    .hero-image-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 8px;
        gap: 10px;
    }
    .hero-image-title {
        font-size: 18px;
        font-weight: 700;
        color: #294534;
        margin-bottom: 2px;
    }
    .hero-image-sub {
        font-size: 13px;
        color: #6c7a6e;
    }
    .hero-image-tag {
        font-size: 12px;
        color: #314a38;
        background: #e4efe6;
        border-radius: 999px;
        padding: 4px 10px;
        white-space: nowrap;
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
# AI GENERATION HELPER (OLLAMA + FALLBACK)
# =========================

AI_SYSTEM_INSTRUCTIONS = """
You are a professional anti-inflammatory and fibroid-supportive nutritionist.
You create recipes that:
- lower inflammation,
- support hormone balance and liver detox,
- are gentle on digestion,
- avoid ultra-processed foods and red/processed meat.

You MUST obey:
- ingredients to include (preferred),
- ingredients to avoid (do not use them),
- selected meal type & vibe.

Output strictly in Markdown:

# Title
One or two sentence description.

## Ingredients
- bullet list

## Method
1. numbered steps

## Notes
- short bullets about fibre, hormones and anti-inflammatory focus.
"""


def _parse_list(raw: str) -> List[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def _build_fallback_recipe(
    meal_type: str,
    servings: int,
    focus: List[str],
    include: str,
    avoid: str,
    time_limit: str,
    style: str,
) -> str:
    """Deterministic recipe builder that actually respects include/avoid and smoothie/non-smoothie."""
    include_items = _parse_list(include)
    avoid_items = [a.lower() for a in _parse_list(avoid)]

    def is_blocked(name: str) -> bool:
        lname = name.lower()
        return any(a in lname for a in avoid_items)

    focus_str = ", ".join(focus) if focus else "fibroid support and low inflammation"

    # Smoothie / drink template
    if "smoothie" in style.lower() or "drink" in style.lower():
        main_bits = [x for x in include_items if not is_blocked(x)]
        if not main_bits:
            main_bits = ["anti-inflammatory green"]
        title_core = ", ".join(main_bits[:2]).title()
        title = f"{title_core} smoothie"

        per_serving = []
        if not is_blocked("unsweetened almond milk"):
            per_serving.append("200 ml unsweetened almond milk or filtered water")
        if not is_blocked("spinach"):
            per_serving.append("1 small handful fresh spinach or other mild leafy green")
        if not is_blocked("berries"):
            per_serving.append("1/2 cup mixed berries (fresh or frozen)")
        if not is_blocked("ground flax"):
            per_serving.append("1 tbsp ground flax or chia seeds")
        if not is_blocked("fresh ginger"):
            per_serving.append("a small slice of fresh ginger (optional)")
        if not is_blocked("banana"):
            per_serving.append("1/2 banana for creaminess (optional)")

        for item in include_items:
            if not is_blocked(item):
                pretty = item[0].upper() + item[1:]
                per_serving.append(f"Extra of your chosen ingredient: {pretty}")

        ingredients_scaled = [f"- x{servings} {line}" for line in per_serving]

        lines: List[str] = []
        lines.append(f"# {title}")
        lines.append("")
        lines.append(
            f"A creamy, fibroid-supportive smoothie tailored to your choices, focusing on {focus_str}."
        )
        lines.append("")
        lines.append("## Ingredients")
        lines.extend(ingredients_scaled)
        lines.append("")
        lines.append("## Method")
        lines.append("1. Add all ingredients to a high-speed blender.")
        lines.append("2. Blend until smooth and creamy, adding more liquid if needed.")
        lines.append("3. Taste and adjust sweetness with a little extra fruit if desired.")
        lines.append("4. Serve immediately, or chill in the fridge for up to 24 hours.")
        lines.append("")
        lines.append("## Notes")
        lines.append("- Ground flax or chia adds fibre and gentle hormone support.")
        lines.append("- Leafy greens support estrogen metabolism and liver detox.")
        lines.append("- Keep it cold but not iced if your digestion is sensitive.")
        if include_items:
            lines.append(f"- You asked to include: {', '.join(include_items)}.")
        if avoid_items:
            lines.append(f"- Avoided: {', '.join(avoid_items)} as requested.")
        return "\n".join(lines)

    # Non-smoothie template (bowls / salads / stews)
    if "salad" in style.lower():
        base_name = "fibre-rich hormone support salad"
    elif "stew" in style.lower():
        base_name = "slow anti-inflammatory veggie stew"
    elif "one-pan" in style.lower():
        base_name = "one-pan anti-inflammatory veggie bowl"
    else:
        base_name = "cosy fibroid-friendly bowl"

    title = base_name.title()

    components: List[str] = []

    if not is_blocked("quinoa"):
        components.append("1 cup cooked quinoa or brown rice per person")
    if not is_blocked("broccoli"):
        components.append("1 cup chopped broccoli or other cruciferous veg per person")
    if not is_blocked("spinach"):
        components.append("1 big handful spinach / kale per person")
    if not is_blocked("chickpeas"):
        components.append("1/2 cup cooked chickpeas, lentils or beans per person")
    if not is_blocked("olive oil"):
        components.append("1–2 tbsp extra-virgin olive oil")
    if not is_blocked("tahini"):
        components.append("1–2 tbsp tahini or seed butter for the dressing")
    if not is_blocked("garlic"):
        components.append("1 small clove garlic, finely grated (optional)")
    if not is_blocked("lemon"):
        components.append("Juice of 1/2–1 lemon")
    if not is_blocked("turmeric"):
        components.append("1/2 tsp ground turmeric + pinch black pepper")

    for item in include_items:
        if not is_blocked(item):
            pretty = item[0].upper() + item[1:]
            components.append(
                f"Your chosen ingredient: {pretty}, chopped or prepared as you like"
            )

    ingredients_scaled = [f"- x{servings} {line}" for line in components]

    lines = [
        f"# {title}",
        "",
        f"A warm, fibroid-supportive bowl that focuses on {focus_str}, "
        f"with a {style.lower()} feel and ready in {time_limit.lower()}.",
        "",
        "## Ingredients",
    ]
    lines.extend(ingredients_scaled)
    lines.append("")
    lines.append("## Method")
    lines.append("1. Cook your grain (quinoa / rice) if not already prepared.")
    lines.append(
        "2. Lightly steam or sauté the vegetables in a splash of water or a little olive oil until just tender."
    )
    lines.append(
        "3. Warm the chickpeas / lentils and add them to the pan, seasoning with salt, pepper and turmeric."
    )
    lines.append(
        "4. In a small bowl, whisk olive oil, tahini, lemon juice and garlic (if using) into a creamy dressing."
    )
    lines.append(
        "5. Assemble bowls with grains at the bottom, veggies and legumes on top, then drizzle generously with the dressing."
    )
    lines.append("6. Taste and adjust acidity, salt and heat to your liking.")
    lines.append("")
    lines.append("## Notes")
    lines.append("- Cruciferous veg and leafy greens support estrogen metabolism.")
    lines.append("- Beans and whole grains add fibre that helps with hormone balance.")
    lines.append("- Healthy fats (olive oil, tahini) support nutrient absorption.")
    if include_items:
        lines.append(f"- You asked to include: {', '.join(include_items)}.")
    if avoid_items:
        lines.append(f"- Ingredients avoided: {', '.join(avoid_items)}.")
    return "\n".join(lines)


def generate_ai_recipe_text(
    meal_type: str,
    servings: int,
    focus: List[str],
    include: str,
    avoid: str,
    time_limit: str,
    style: str,
) -> str:
    """
    Try to use Ollama (llama3) with strict instructions.
    If not available or it fails, fall back to deterministic builder.
    """
    include_items = _parse_list(include)
    avoid_items = _parse_list(avoid)
    focus_str = ", ".join(focus) if focus else "fibroid support and low inflammation"

    user_prompt = f"""
SYSTEM:
{AI_SYSTEM_INSTRUCTIONS}

USER:
Create a {meal_type} recipe for {servings} serving(s).

Focus: {focus_str}.
Style / vibe: {style}.
Time limit: {time_limit}.

Preferred ingredients (include if possible): {include or "none specified"}.
Ingredients to AVOID (must not appear in ingredients list): {avoid or "none specified"}.

The recipe must be:
- anti-inflammatory,
- fibroid-friendly (high fibre, cruciferous veg when appropriate, hormone supportive),
- mostly plant-based (fish/eggs ok, no red or processed meat),
- realistic to cook at home.

Remember:
- Absolutely do not use any of the avoid ingredients.
- Strongly prefer using the included ingredients.

Return only the recipe in Markdown with sections:
# Title
Short 1–2 sentence description.

## Ingredients
- bullet list

## Method
1. numbered steps

## Notes
- bullets about why this is supportive for fibroids and low inflammation.
"""

    if OLLAMA_AVAILABLE:
        try:
            resp = ollama_client.generate(
                model="llama3",
                prompt=user_prompt,
            )
            text = resp.get("response", "") if isinstance(resp, dict) else ""
            if text.strip():
                # quick sanity check: if avoid items appear, fall back
                lowered = text.lower()
                if any(a.lower() in lowered for a in avoid_items if a):
                    return _build_fallback_recipe(
                        meal_type, servings, focus, include, avoid, time_limit, style
                    )
                return text
        except Exception:
            # fall through to deterministic builder
            pass

    return _build_fallback_recipe(
        meal_type, servings, focus, include, avoid, time_limit, style
    )


# =========================
# SIMPLE SEARCH HELPER
# =========================

def search_meals(query: str):
    """
    Simple search over MEALS by:
    - meal name
    - tags
    - ingredient item text
    """
    q = query.strip().lower()
    if not q:
        return []

    results = []
    for meal in MEALS:
        # name
        if q in meal.name.lower():
            results.append(meal)
            continue

        # tags
        if any(q in tag.lower() for tag in (meal.tags or [])):
            results.append(meal)
            continue

        # ingredients (defensive, ingredients may be None)
        if getattr(meal, "ingredients", None):
            for ing in meal.ingredients:
                item = (ing.get("item") or "").lower()
                if q in item:
                    results.append(meal)
                    break

    return results


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

    # Hero image “carousel”
    hero_len = len(HERO_IMAGES)
    hero_idx = st.session_state.get("hero_index", 0) % hero_len
    hero = HERO_IMAGES[hero_idx]

    st.markdown(
        f"""
        <div class="hero-image-card">
            <img src="{hero['url']}" alt="{hero['title']}" class="hero-image" />
            <div class="hero-image-meta">
                <div>
                    <div class="hero-image-title">{hero['title']}</div>
                    <div class="hero-image-sub">{hero['subtitle']}</div>
                </div>
                <div class="hero-image-tag">🌿 Anti-inflammatory focus</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    def go_prev():
        st.session_state["hero_index"] = (st.session_state["hero_index"] - 1) % hero_len

    def go_next():
        st.session_state["hero_index"] = (st.session_state["hero_index"] + 1) % hero_len

    c1, c2, c3 = st.columns([1, 3, 1])
    with c1:
        st.button("⟵", key="hero_prev", on_click=go_prev)
    with c3:
        st.button("⟶", key="hero_next", on_click=go_next)

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

    # Search bar – now functional
    search_query = st.text_input(
        "Search recipes",
        "",
        placeholder="Search a meal or ingredient…",
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

    # Search results
    if search_query.strip():
        results = search_meals(search_query)
        st.markdown("### 🔎 Search results")

        if not results:
            st.info("No meals found matching your search yet.")
        else:
            for meal in results:
                tags_display = ", ".join(meal.tags) if meal.tags else "no tags"
                st.markdown(
                    f"""
                    <div class="meal-card">
                        <div class="meal-header-line">
                            <div class="meal-name">{meal.name}</div>
                            <div class="meal-heart">👩‍🍳</div>
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


def render_ai() -> None:
    """AI-powered recipe studio using Ollama if available, with a strict fallback."""
    st.markdown('<div class="main-block">', unsafe_allow_html=True)

    st.markdown(
        """
        <div style="padding: 10px 0 4px 0; text-align:left;">
            <h2 style="margin: 0; font-size:24px; color:#263a2d;">AI recipe studio</h2>
            <div style="font-size:13px; color:#6c7a6e;">
                Co-create a fibroid-friendly, anti-inflammatory recipe that fits your cravings,
                ingredients and time.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not OLLAMA_AVAILABLE:
        st.info(
            "Ollama client is not available. Install `ollama` and run `ollama pull llama3` "
            "to use a local model. I’ll still generate recipes using an internal fallback."
        )

    with st.form("ai_recipe_form"):
        col1, col2 = st.columns(2)
        with col1:
            meal_type = st.selectbox(
                "Meal type",
                ["Breakfast", "Lunch", "Dinner", "Snack"],
                index=1,
            )
        with col2:
            servings = st.slider("Servings", 1, 6, 2)

        focus = st.multiselect(
            "What should this recipe support?",
            [
                "anti-inflammatory",
                "fibroid support",
                "hormone balance",
                "iron support",
                "gentle on digestion",
            ],
            default=["anti-inflammatory", "fibroid support"],
        )

        col3, col4 = st.columns(2)
        with col3:
            time_limit = st.selectbox(
                "Cooking time",
                ["Under 15 minutes", "Under 30 minutes", "Up to 45 minutes", "Slow / relaxed"],
                index=1,
            )
        with col4:
            style = st.selectbox(
                "Vibe",
                ["cosy bowl", "light salad", "hearty stew", "one-pan meal", "smoothie / drink"],
                index=4,
            )

        include = st.text_area(
            "Ingredients you’d like to include",
            placeholder="e.g. berries, spinach, kiwi, ginger…",
        )
        avoid = st.text_area(
            "Ingredients you’d like to avoid",
            placeholder="e.g. dairy, gluten, mushrooms, onion, broccoli…",
        )

        submitted = st.form_submit_button("✨ Generate recipe", use_container_width=True)

    if submitted:
        with st.spinner("Crafting your fibroid-friendly recipe…"):
            recipe_text = generate_ai_recipe_text(
                meal_type=meal_type,
                servings=servings,
                focus=focus,
                include=include,
                avoid=avoid,
                time_limit=time_limit,
                style=style,
            )
        st.session_state["ai_recipe"] = recipe_text

    if st.session_state.get("ai_recipe"):
        st.markdown("### Your AI-crafted recipe")
        st.markdown(st.session_state["ai_recipe"])

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
elif current_tab == "ai":
    render_ai()
else:
    render_home()


# =========================
# BOTTOM NAVIGATION
# =========================

home_class = "nav-item active" if current_tab == "home" else "nav-item"
plan_class = "nav-item active" if current_tab == "plan" else "nav-item"
recipes_class = "nav-item active" if current_tab == "recipes" else "nav-item"
ai_class = "nav-item active" if current_tab == "ai" else "nav-item"

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
        <a class="{ai_class}" href="?tab=ai">
            <span class="nav-icon">🤖</span>
            <span>AI Chef</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)







# import os
# from datetime import date
# import random
# from typing import List
#
# import streamlit as st
#
# from planner import FASTING_CONFIGS, generate_meal_plan
# from meals import MEALS
# from fermented import FERMENTED_RECIPES
#
#
# # =========================
# # OPTIONAL OLLAMA CLIENT
# # =========================
#
# OLLAMA_AVAILABLE = False
# try:
#     from ollama import Client  # type: ignore
#
#     # ollama_client = Client(host="http://localhost:11434")
#     ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
#     ollama_client = Client(host=ollama_host)
#
#     OLLAMA_AVAILABLE = True
# except Exception:
#     ollama_client = None
#     OLLAMA_AVAILABLE = False
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
# if "hero_index" not in st.session_state:
#     st.session_state["hero_index"] = 0
# if "ai_recipe" not in st.session_state:
#     st.session_state["ai_recipe"] = None
#
# # Determine current tab from query params (?tab=home|plan|recipes|ai)
# raw_tab = st.query_params.get("tab", "home")
# if isinstance(raw_tab, list):
#     current_tab = raw_tab[0] if raw_tab else "home"
# else:
#     current_tab = raw_tab or "home"
#
# if current_tab not in {"home", "plan", "recipes", "ai"}:
#     current_tab = "home"
#
#
# # =========================
# # HERO IMAGES (CAROUSEL)
# # =========================
#
# HERO_IMAGES = [
#     {
#         "title": "Healthy organic bowl",
#         "subtitle": "Leafy greens, good fats and fibre-rich veggies.",
#         "url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80",
#     },
#     {
#         "title": "Rainbow anti-inflammatory plate",
#         "subtitle": "Colourful plants to calm inflammation and support hormones.",
#         "url": "https://images.unsplash.com/photo-1543353071-873f17a7a088?auto=format&fit=crop&w=1200&q=80",
#     },
#     {
#         "title": "Nourishing veggie board",
#         "subtitle": "Cruciferous veg, healthy oils and real food ingredients.",
#         "url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=1200&q=80",
#     },
# ]
#
#
# # =========================
# # GLOBAL CSS
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
#     /* Hero image card (carousel) */
#     .hero-image-card {
#         background: #f6fbf8;
#         border-radius: 24px;
#         padding: 10px 10px 12px 10px;
#         margin: 4px 0 14px 0;
#         box-shadow: 0 4px 14px rgba(0,0,0,0.10);
#         border: 1px solid #d4e4d8;
#     }
#     .hero-image-card img.hero-image {
#         width: 100%;
#         border-radius: 20px;
#         object-fit: cover;
#         max-height: 260px;
#     }
#     .hero-image-meta {
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         margin-top: 8px;
#         gap: 10px;
#     }
#     .hero-image-title {
#         font-size: 18px;
#         font-weight: 700;
#         color: #294534;
#         margin-bottom: 2px;
#     }
#     .hero-image-sub {
#         font-size: 13px;
#         color: #6c7a6e;
#     }
#     .hero-image-tag {
#         font-size: 12px;
#         color: #314a38;
#         background: #e4efe6;
#         border-radius: 999px;
#         padding: 4px 10px;
#         white-space: nowrap;
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
#     /* Bottom navigation bar */
#     .bottom-nav {
#         position: fixed;
#         bottom: 0;
#         left: 0;
#         right: 0;
#         background: #314a38;  /* deep green */
#         border-top: 1px solid #1f3124;
#         display: flex;
#         justify-content: space-around;
#         padding: 6px 10px 10px 10px;
#         z-index: 9999;
#     }
#
#     .nav-item {
#         flex: 1;
#         background: transparent;
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#         justify-content: center;
#         font-size: 12px;
#         padding: 6px 0;
#         border-radius: 999px;
#         margin: 0 4px;
#         cursor: pointer;
#         text-decoration: none;
#     }
#
#     .nav-icon {
#         font-size: 18px;
#         margin-bottom: 1px;
#     }
#
#     a.nav-item,
#     a.nav-item:link,
#     a.nav-item:visited {
#         color: #d8e5db;
#         text-decoration: none;
#     }
#
#     a.nav-item.active,
#     a.nav-item.active:link,
#     a.nav-item.active:visited {
#         background: #e4efe6;     /* soft sage pill */
#         color: #314a38;
#         font-weight: 600;
#         text-decoration: none;
#     }
#
#     a.nav-item span {
#         color: inherit;
#         text-decoration: none;
#     }
#
#     /* Expander styling – match theme green */
#     [data-testid="stExpander"] > details > summary {
#         background-color: #314a38 !important;   /* same deep green as bottom nav */
#         color: #ffffff !important;
#         padding: 10px 14px;
#         border-radius: 8px;
#         cursor: pointer;
#         font-weight: 500;
#         list-style: none;
#     }
#
#     [data-testid="stExpander"] > details > summary::-webkit-details-marker {
#         display: none;
#     }
#
#     [data-testid="stExpander"] > details > summary svg {
#         stroke: #ffffff !important;
#     }
#
#     [data-testid="stExpander"] > details[open] {
#         border-left: 3px solid #314a38;
#         border-radius: 0 0 8px 8px;
#         margin-bottom: 10px;
#         background-color: #f6fbf8;
#         padding-bottom: 8px;
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
#     """,
#     unsafe_allow_html=True,
# )
#
#
# # =========================
# # AI GENERATION HELPER (OLLAMA + FALLBACK)
# # =========================
#
# AI_SYSTEM_INSTRUCTIONS = """
# You are a professional anti-inflammatory and fibroid-supportive nutritionist.
# You create recipes that:
# - lower inflammation,
# - support hormone balance and liver detox,
# - are gentle on digestion,
# - avoid ultra-processed foods and red/processed meat.
#
# You MUST obey:
# - ingredients to include (preferred),
# - ingredients to avoid (do not use them),
# - selected meal type & vibe.
#
# Output strictly in Markdown:
#
# # Title
# One or two sentence description.
#
# ## Ingredients
# - bullet list
#
# ## Method
# 1. numbered steps
#
# ## Notes
# - short bullets about fibre, hormones and anti-inflammatory focus.
# """
#
#
# def _parse_list(raw: str) -> List[str]:
#     return [x.strip() for x in raw.split(",") if x.strip()]
#
#
# def _build_fallback_recipe(
#     meal_type: str,
#     servings: int,
#     focus: List[str],
#     include: str,
#     avoid: str,
#     time_limit: str,
#     style: str,
# ) -> str:
#     """Deterministic recipe builder that actually respects include/avoid and smoothie/non-smoothie."""
#     include_items = _parse_list(include)
#     avoid_items = [a.lower() for a in _parse_list(avoid)]
#
#     def is_blocked(name: str) -> bool:
#         lname = name.lower()
#         return any(a in lname for a in avoid_items)
#
#     focus_str = ", ".join(focus) if focus else "fibroid support and low inflammation"
#
#     # Smoothie / drink template
#     if "smoothie" in style.lower() or "drink" in style.lower():
#         main_bits = [x for x in include_items if not is_blocked(x)]
#         if not main_bits:
#             main_bits = ["anti-inflammatory green"]
#         title_core = ", ".join(main_bits[:2]).title()
#         title = f"{title_core} smoothie"
#
#         per_serving = []
#         if not is_blocked("unsweetened almond milk"):
#             per_serving.append("200 ml unsweetened almond milk or filtered water")
#         if not is_blocked("spinach"):
#             per_serving.append("1 small handful fresh spinach or other mild leafy green")
#         if not is_blocked("berries"):
#             per_serving.append("1/2 cup mixed berries (fresh or frozen)")
#         if not is_blocked("ground flax"):
#             per_serving.append("1 tbsp ground flax or chia seeds")
#         if not is_blocked("fresh ginger"):
#             per_serving.append("a small slice of fresh ginger (optional)")
#         if not is_blocked("banana"):
#             per_serving.append("1/2 banana for creaminess (optional)")
#
#         for item in include_items:
#             if not is_blocked(item):
#                 pretty = item[0].upper() + item[1:]
#                 per_serving.append(f"Extra of your chosen ingredient: {pretty}")
#
#         ingredients_scaled = [f"- x{servings} {line}" for line in per_serving]
#
#         lines: List[str] = []
#         lines.append(f"# {title}")
#         lines.append("")
#         lines.append(
#             f"A creamy, fibroid-supportive smoothie tailored to your choices, focusing on {focus_str}."
#         )
#         lines.append("")
#         lines.append("## Ingredients")
#         lines.extend(ingredients_scaled)
#         lines.append("")
#         lines.append("## Method")
#         lines.append("1. Add all ingredients to a high-speed blender.")
#         lines.append("2. Blend until smooth and creamy, adding more liquid if needed.")
#         lines.append("3. Taste and adjust sweetness with a little extra fruit if desired.")
#         lines.append("4. Serve immediately, or chill in the fridge for up to 24 hours.")
#         lines.append("")
#         lines.append("## Notes")
#         lines.append("- Ground flax or chia adds fibre and gentle hormone support.")
#         lines.append("- Leafy greens support estrogen metabolism and liver detox.")
#         lines.append("- Keep it cold but not iced if your digestion is sensitive.")
#         if include_items:
#             lines.append(f"- You asked to include: {', '.join(include_items)}.")
#         if avoid_items:
#             lines.append(f"- Avoided: {', '.join(avoid_items)} as requested.")
#         return "\n".join(lines)
#
#     # Non-smoothie template (bowls / salads / stews)
#     if "salad" in style.lower():
#         base_name = "fibre-rich hormone support salad"
#     elif "stew" in style.lower():
#         base_name = "slow anti-inflammatory veggie stew"
#     elif "one-pan" in style.lower():
#         base_name = "one-pan anti-inflammatory veggie bowl"
#     else:
#         base_name = "cosy fibroid-friendly bowl"
#
#     title = base_name.title()
#
#     components: List[str] = []
#
#     if not is_blocked("quinoa"):
#         components.append("1 cup cooked quinoa or brown rice per person")
#     if not is_blocked("broccoli"):
#         components.append("1 cup chopped broccoli or other cruciferous veg per person")
#     if not is_blocked("spinach"):
#         components.append("1 big handful spinach / kale per person")
#     if not is_blocked("chickpeas"):
#         components.append("1/2 cup cooked chickpeas, lentils or beans per person")
#     if not is_blocked("olive oil"):
#         components.append("1–2 tbsp extra-virgin olive oil")
#     if not is_blocked("tahini"):
#         components.append("1–2 tbsp tahini or seed butter for the dressing")
#     if not is_blocked("garlic"):
#         components.append("1 small clove garlic, finely grated (optional)")
#     if not is_blocked("lemon"):
#         components.append("Juice of 1/2–1 lemon")
#     if not is_blocked("turmeric"):
#         components.append("1/2 tsp ground turmeric + pinch black pepper")
#
#     for item in include_items:
#         if not is_blocked(item):
#             pretty = item[0].upper() + item[1:]
#             components.append(
#                 f"Your chosen ingredient: {pretty}, chopped or prepared as you like"
#             )
#
#     ingredients_scaled = [f"- x{servings} {line}" for line in components]
#
#     lines = [
#         f"# {title}",
#         "",
#         f"A warm, fibroid-supportive bowl that focuses on {focus_str}, "
#         f"with a {style.lower()} feel and ready in {time_limit.lower()}.",
#         "",
#         "## Ingredients",
#     ]
#     lines.extend(ingredients_scaled)
#     lines.append("")
#     lines.append("## Method")
#     lines.append("1. Cook your grain (quinoa / rice) if not already prepared.")
#     lines.append(
#         "2. Lightly steam or sauté the vegetables in a splash of water or a little olive oil until just tender."
#     )
#     lines.append(
#         "3. Warm the chickpeas / lentils and add them to the pan, seasoning with salt, pepper and turmeric."
#     )
#     lines.append(
#         "4. In a small bowl, whisk olive oil, tahini, lemon juice and garlic (if using) into a creamy dressing."
#     )
#     lines.append(
#         "5. Assemble bowls with grains at the bottom, veggies and legumes on top, then drizzle generously with the dressing."
#     )
#     lines.append("6. Taste and adjust acidity, salt and heat to your liking.")
#     lines.append("")
#     lines.append("## Notes")
#     lines.append("- Cruciferous veg and leafy greens support estrogen metabolism.")
#     lines.append("- Beans and whole grains add fibre that helps with hormone balance.")
#     lines.append("- Healthy fats (olive oil, tahini) support nutrient absorption.")
#     if include_items:
#         lines.append(f"- You asked to include: {', '.join(include_items)}.")
#     if avoid_items:
#         lines.append(f"- Ingredients avoided: {', '.join(avoid_items)}.")
#     return "\n".join(lines)
#
#
# def generate_ai_recipe_text(
#     meal_type: str,
#     servings: int,
#     focus: List[str],
#     include: str,
#     avoid: str,
#     time_limit: str,
#     style: str,
# ) -> str:
#     """
#     Try to use Ollama (llama3) with strict instructions.
#     If not available or it fails, fall back to deterministic builder.
#     """
#     include_items = _parse_list(include)
#     avoid_items = _parse_list(avoid)
#     focus_str = ", ".join(focus) if focus else "fibroid support and low inflammation"
#
#     user_prompt = f"""
# SYSTEM:
# {AI_SYSTEM_INSTRUCTIONS}
#
# USER:
# Create a {meal_type} recipe for {servings} serving(s).
#
# Focus: {focus_str}.
# Style / vibe: {style}.
# Time limit: {time_limit}.
#
# Preferred ingredients (include if possible): {include or "none specified"}.
# Ingredients to AVOID (must not appear in ingredients list): {avoid or "none specified"}.
#
# The recipe must be:
# - anti-inflammatory,
# - fibroid-friendly (high fibre, cruciferous veg when appropriate, hormone supportive),
# - mostly plant-based (fish/eggs ok, no red or processed meat),
# - realistic to cook at home.
#
# Remember:
# - Absolutely do not use any of the avoid ingredients.
# - Strongly prefer using the included ingredients.
#
# Return only the recipe in Markdown with sections:
# # Title
# Short 1–2 sentence description.
#
# ## Ingredients
# - bullet list
#
# ## Method
# 1. numbered steps
#
# ## Notes
# - bullets about why this is supportive for fibroids and low inflammation.
# """
#
#     if OLLAMA_AVAILABLE:
#         try:
#             resp = ollama_client.generate(
#                 model="llama3",
#                 prompt=user_prompt,
#             )
#             text = resp.get("response", "") if isinstance(resp, dict) else ""
#             if text.strip():
#                 # quick sanity check: if avoid items appear, fall back
#                 lowered = text.lower()
#                 if any(a.lower() in lowered for a in avoid_items if a):
#                     return _build_fallback_recipe(
#                         meal_type, servings, focus, include, avoid, time_limit, style
#                     )
#                 return text
#         except Exception:
#             # fall through to deterministic builder
#             pass
#
#     return _build_fallback_recipe(
#         meal_type, servings, focus, include, avoid, time_limit, style
#     )
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
#     # Hero image “carousel”
#     hero_len = len(HERO_IMAGES)
#     hero_idx = st.session_state.get("hero_index", 0) % hero_len
#     hero = HERO_IMAGES[hero_idx]
#
#     st.markdown(
#         f"""
#         <div class="hero-image-card">
#             <img src="{hero['url']}" alt="{hero['title']}" class="hero-image" />
#             <div class="hero-image-meta">
#                 <div>
#                     <div class="hero-image-title">{hero['title']}</div>
#                     <div class="hero-image-sub">{hero['subtitle']}</div>
#                 </div>
#                 <div class="hero-image-tag">🌿 Anti-inflammatory focus</div>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#
#     def go_prev():
#         st.session_state["hero_index"] = (st.session_state["hero_index"] - 1) % hero_len
#
#     def go_next():
#         st.session_state["hero_index"] = (st.session_state["hero_index"] + 1) % hero_len
#
#     c1, c2, c3 = st.columns([1, 3, 1])
#     with c1:
#         st.button("⟵", key="hero_prev", on_click=go_prev)
#     with c3:
#         st.button("⟶", key="hero_next", on_click=go_next)
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
#     # Search bar (visual only)
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
#         fibroid_focus = st.checkbox(
#             "Support fibroids with fibre & cruciferous veggies", value=True
#         )
#         anemia_risk = st.checkbox(
#             "Support iron levels (for heavy periods / low iron)", value=True
#         )
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
#             <h2 style="margin: 0; font-size:24px; color:#263a2d;">Recipes</h2>
#             <div style="font-size:13px; color:#6c7a6e;">
#                 Browse anti-inflammatory meals or fermented add-ons to boost your gut and hormones.
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#
#     mode = st.radio(
#         "What would you like to explore?",
#         options=["Meals", "Fermented add-ons"],
#         horizontal=True,
#     )
#
#     if mode == "Meals":
#         col1, col2 = st.columns([2, 1])
#         meal_type_filter = col1.selectbox(
#             "Meal type",
#             ["All", "Breakfast", "Lunch", "Dinner", "Snack"],
#         )
#         tag_filter = col2.selectbox(
#             "Focus",
#             ["Any", "anti_inflammatory", "fibroid_friendly", "high_fiber", "iron_rich"],
#         )
#
#         for meal in MEALS:
#             if meal_type_filter != "All" and meal.meal_type.lower() != meal_type_filter.lower():
#                 continue
#             if tag_filter != "Any" and tag_filter not in meal.tags:
#                 continue
#
#             tags_display = ", ".join(meal.tags) if meal.tags else "no tags"
#
#             st.markdown(
#                 f"""
#                 <div class="meal-card">
#                     <div class="meal-header-line">
#                         <div class="meal-name">{meal.name}</div>
#                         <div class="meal-heart">👩‍🍳</div>
#                     </div>
#                     <div class="meal-meta">
#                         {meal.meal_type.title()} · 🌿 Anti-inflammatory: {meal.anti_inflammatory_score}/5
#                         · 💪 Iron: {meal.iron_support}/5
#                     </div>
#                     <div class="meal-tags">
#                         Tags: {tags_display}
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )
#
#             with st.expander("👩‍🍳 See full recipe"):
#                 if meal.ingredients:
#                     st.markdown("**Ingredients**")
#                     for ing in meal.ingredients:
#                         amount = ing.get("amount", "").strip()
#                         item = ing.get("item", "").strip()
#                         if amount:
#                             st.markdown(f"- {amount} {item}")
#                         else:
#                             st.markdown(f"- {item}")
#
#                 if meal.instructions:
#                     st.markdown("**Step-by-step**")
#                     for idx, step in enumerate(meal.instructions, start=1):
#                         st.markdown(f"{idx}. {step}")
#     else:
#         st.subheader("Fermented add-ons")
#         st.caption(
#             "These are small ferments you can prepare ahead and add to meals for extra fibre, "
#             "beneficial bacteria and flavour."
#         )
#
#         for fr in FERMENTED_RECIPES:
#             brine_text = (
#                 f" · {fr.brine_percent:.1f}% brine" if fr.brine_percent is not None else ""
#             )
#
#             st.markdown(
#                 f"""
#                 <div class="meal-card">
#                     <div class="meal-header-line">
#                         <div class="meal-name">{fr.name}</div>
#                         <div class="meal-heart">🧪</div>
#                     </div>
#                     <div class="meal-meta">
#                         Ferment · ⏱ At least {fr.min_days} days{brine_text}
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )
#
#             with st.expander("👩‍🍳 See full recipe"):
#                 if fr.notes:
#                     st.markdown(f"*{fr.notes}*")
#
#                 if fr.ingredients:
#                     st.markdown("**Ingredients**")
#                     for line in fr.ingredients:
#                         st.markdown(f"- {line}")
#
#                 if fr.steps:
#                     st.markdown("**How to make it**")
#                     for idx, step in enumerate(fr.steps, start=1):
#                         st.markdown(f"{idx}. {step}")
#
#                 st.markdown(f"**Fermentation time**: at least {fr.min_days} days.")
#
#     st.markdown("</div>", unsafe_allow_html=True)
#
#
# def render_ai() -> None:
#     """AI-powered recipe studio using Ollama if available, with a strict fallback."""
#     st.markdown('<div class="main-block">', unsafe_allow_html=True)
#
#     st.markdown(
#         """
#         <div style="padding: 10px 0 4px 0; text-align:left;">
#             <h2 style="margin: 0; font-size:24px; color:#263a2d;">AI recipe studio</h2>
#             <div style="font-size:13px; color:#6c7a6e;">
#                 Co-create a fibroid-friendly, anti-inflammatory recipe that fits your cravings,
#                 ingredients and time.
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
#
#     if not OLLAMA_AVAILABLE:
#         st.info(
#             "Ollama client is not available. Install `ollama` and run `ollama pull llama3` "
#             "to use a local model. I’ll still generate recipes using an internal fallback."
#         )
#
#     with st.form("ai_recipe_form"):
#         col1, col2 = st.columns(2)
#         with col1:
#             meal_type = st.selectbox(
#                 "Meal type",
#                 ["Breakfast", "Lunch", "Dinner", "Snack"],
#                 index=1,
#             )
#         with col2:
#             servings = st.slider("Servings", 1, 6, 2)
#
#         focus = st.multiselect(
#             "What should this recipe support?",
#             [
#                 "anti-inflammatory",
#                 "fibroid support",
#                 "hormone balance",
#                 "iron support",
#                 "gentle on digestion",
#             ],
#             default=["anti-inflammatory", "fibroid support"],
#         )
#
#         col3, col4 = st.columns(2)
#         with col3:
#             time_limit = st.selectbox(
#                 "Cooking time",
#                 ["Under 15 minutes", "Under 30 minutes", "Up to 45 minutes", "Slow / relaxed"],
#                 index=1,
#             )
#         with col4:
#             style = st.selectbox(
#                 "Vibe",
#                 ["cosy bowl", "light salad", "hearty stew", "one-pan meal", "smoothie / drink"],
#                 index=4,
#             )
#
#         include = st.text_area(
#             "Ingredients you’d like to include",
#             placeholder="e.g. berries, spinach, kiwi, ginger…",
#         )
#         avoid = st.text_area(
#             "Ingredients you’d like to avoid",
#             placeholder="e.g. dairy, gluten, mushrooms, onion, broccoli…",
#         )
#
#         submitted = st.form_submit_button("✨ Generate recipe", use_container_width=True)
#
#     if submitted:
#         with st.spinner("Crafting your fibroid-friendly recipe…"):
#             recipe_text = generate_ai_recipe_text(
#                 meal_type=meal_type,
#                 servings=servings,
#                 focus=focus,
#                 include=include,
#                 avoid=avoid,
#                 time_limit=time_limit,
#                 style=style,
#             )
#         st.session_state["ai_recipe"] = recipe_text
#
#     if st.session_state.get("ai_recipe"):
#         st.markdown("### Your AI-crafted recipe")
#         st.markdown(st.session_state["ai_recipe"])
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
# elif current_tab == "ai":
#     render_ai()
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
# ai_class = "nav-item active" if current_tab == "ai" else "nav-item"
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
#         <a class="{ai_class}" href="?tab=ai">
#             <span class="nav-icon">🤖</span>
#             <span>AI Chef</span>
#         </a>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )
#
