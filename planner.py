from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict, List, Tuple, Optional

from meals import Meal, MEALS


# ===== Core data structures =====

@dataclass
class MealSlot:
    time_str: str           # "HH:MM"
    meal_type: str          # "breakfast" | "lunch" | "dinner" | "snack"
    meal: Meal


@dataclass
class DayPlan:
    day: date
    meals: List[MealSlot]


@dataclass
class FastingConfig:
    """
    Defines a fasting pattern as a list of offsets (in hours)
    from the eating-window start.
    Example: offsets = [(0, "lunch"), (4, "dinner")]
    """
    id: str
    label: str
    description: str
    offsets: List[Tuple[int, str]]  # (offset_hours_from_start, meal_type)


# ===== Fasting patterns =====

FASTING_CONFIGS: Dict[str, FastingConfig] = {
    "none_3meals": FastingConfig(
        id="none_3meals",
        label="No fasting · 3 meals",
        description="Breakfast, lunch and dinner spread through the day.",
        offsets=[
            (0, "breakfast"),   # eat_window_start_hour
            (5, "lunch"),
            (10, "dinner"),
        ],
    ),
    "16_8": FastingConfig(
        id="16_8",
        label="16:8 · 2 meals",
        description="16 hours fasting with 2 solid meals in an 8 hour window.",
        offsets=[
            (0, "lunch"),   # first meal at start of eating window
            (4, "dinner"),  # second meal ~4 hours later
        ],
    ),
    "14_10": FastingConfig(
        id="14_10",
        label="14:10 · 3 meals (gentler)",
        description="14 hours fasting, 3 smaller meals in a 10 hour window.",
        offsets=[
            (0, "breakfast"),
            (4, "lunch"),
            (9, "dinner"),
        ],
    ),
    "18_6_2meals": FastingConfig(
        id="18_6_2meals",
        label="18:6 · 2 meals",
        description="Two solid meals in a 6 hour window.",
        offsets=[
            (0, "lunch"),
            (3, "dinner"),
        ],
    ),
    "omad": FastingConfig(
        id="omad",
        label="OMAD · One main meal",
        description="One main meal per day. Only advisable if medically safe.",
        offsets=[
            (0, "dinner"),
        ],
    ),
}


# ===== Time slot generation =====

def get_slots_for_day(
    fasting_pattern_id: str,
    eat_window_start_hour: int,
) -> List[Tuple[str, str]]:
    """
    Build time slots for a given day:
    returns list of (time_str 'HH:MM', meal_type)

    We also enforce a latest meal time (20:00) to avoid very late dinners.
    """
    config = FASTING_CONFIGS[fasting_pattern_id]
    slots: List[Tuple[str, str]] = []

    latest_meal_hour = 20  # latest allowed meal time = 20:00

    for offset_hours, meal_type in config.offsets:
        raw_hour = eat_window_start_hour + offset_hours
        # wrap within 0–23
        wrapped = raw_hour % 24
        # clamp to latest_meal_hour
        hour = min(wrapped, latest_meal_hour)
        time_str = f"{hour:02d}:00"
        slots.append((time_str, meal_type))

    return slots


# ===== Meal filtering & selection =====

def filter_meals_for_type(
    meals_source: List[Meal],
    meal_type: str,
    fibroid_focus: bool,
) -> List[Meal]:
    """
    Filter meals by type and inflammation / fibroid focus.
    """
    filtered: List[Meal] = []
    for meal in meals_source:
        if meal.meal_type != meal_type:
            continue

        # must be explicitly anti-inflammatory
        if "anti_inflammatory" not in meal.tags:
            continue

        # tighten selection if fibroid_focus is on
        if fibroid_focus:
            if not any(
                tag in meal.tags
                for tag in ("fibroid_friendly", "high_fiber", "liver_support")
            ):
                continue

        # basic quality filter: exclude very inflammatory foods
        if meal.anti_inflammatory_score > 3:
            continue

        filtered.append(meal)

    return filtered


def choose_meal(
    candidates: List[Meal],
    anemia_risk: bool,
    repeat_counter: Dict[str, int],
) -> Optional[Meal]:
    """
    Choose a meal from candidates, preferring iron-rich/fibre-rich ones
    if anemia_risk is True, and respecting max_repeats_per_30.
    """
    valid_candidates: List[Meal] = []
    for meal in candidates:
        used = repeat_counter.get(meal.id, 0)
        if used >= meal.max_repeats_per_30:
            continue
        valid_candidates.append(meal)

    if not valid_candidates:
        return None

    scored: List[Tuple[int, Meal]] = []
    for meal in valid_candidates:
        score = 10

        # better anti-inflammatory score (lower) → higher score
        score += max(0, 5 - meal.anti_inflammatory_score)

        # iron support if anemia_risk
        if anemia_risk:
            score += meal.iron_support

        # fibre is always a win
        score += meal.fiber_score

        scored.append((score, meal))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


# ===== Plan generation =====

def generate_meal_plan(
    days: int,
    fasting_pattern_id: str,
    eat_window_start_hour: int,
    fibroid_focus: bool,
    anemia_risk: bool,
    meals_source: Optional[List[Meal]] = None,
    start_day: Optional[date] = None,
) -> List[DayPlan]:
    """
    Main entry: create a rotating plan for N days.

    - uses fasting pattern + eating window
    - only anti-inflammatory meals
    - fibroid_focus: prioritise fibroid-friendly & hormone-support meals
    - anemia_risk: prefer iron-rich meals more often
    """
    if meals_source is None:
        meals_source = MEALS

    if start_day is None:
        start_day = date.today()

    plans: List[DayPlan] = []
    repeat_counter: Dict[str, int] = {}

    for i in range(days):
        current_day = start_day + timedelta(days=i)
        slots = get_slots_for_day(fasting_pattern_id, eat_window_start_hour)
        day_meals: List[MealSlot] = []

        for time_str, meal_type in slots:
            candidates = filter_meals_for_type(
                meals_source=meals_source,
                meal_type=meal_type,
                fibroid_focus=fibroid_focus,
            )

            chosen = choose_meal(
                candidates=candidates,
                anemia_risk=anemia_risk,
                repeat_counter=repeat_counter,
            )

            # fallback: if fibroid focus is too strict and we get nothing, relax it once
            if chosen is None and fibroid_focus:
                relaxed_candidates = filter_meals_for_type(
                    meals_source=meals_source,
                    meal_type=meal_type,
                    fibroid_focus=False,
                )
                chosen = choose_meal(
                    candidates=relaxed_candidates,
                    anemia_risk=anemia_risk,
                    repeat_counter=repeat_counter,
                )

            if chosen is None:
                # nothing suitable for this slot
                continue

            day_meals.append(
                MealSlot(
                    time_str=time_str,
                    meal_type=meal_type,
                    meal=chosen,
                )
            )
            repeat_counter[chosen.id] = repeat_counter.get(chosen.id, 0) + 1

        plans.append(DayPlan(day=current_day, meals=day_meals))

    return plans


# ===== CLI test =====

if __name__ == "__main__":
    demo_plan = generate_meal_plan(
        days=7,
        fasting_pattern_id="16_8",
        eat_window_start_hour=12,
        fibroid_focus=True,
        anemia_risk=True,
    )

    for day_plan in demo_plan:
        print(f"\n=== {day_plan.day.isoformat()} ===")
        for slot in day_plan.meals:
            print(f"{slot.time_str} | {slot.meal_type.title():8} | {slot.meal.name}")
