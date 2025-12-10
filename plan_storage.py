# plan_storage.py
import json
from datetime import date
from types import SimpleNamespace
from typing import List, Any

from meals import MEALS
from db import save_plan as db_save_plan, load_latest_plan as db_load_latest_plan


def plan_to_json(plan: List[Any]) -> str:
    """
    Convert a list of day_plan objects into JSON.
    Each day_plan has: day (date), meals (list of slots)
    Each slot has: time_str, meal (with .name)
    """
    serialised = []
    for day_plan in plan:
        day_entry = {
            "day": day_plan.day.isoformat(),
            "meals": [],
        }
        for slot in day_plan.meals:
            day_entry["meals"].append(
                {
                    "time_str": slot.time_str,
                    "meal_name": slot.meal.name,
                }
            )
        serialised.append(day_entry)
    return json.dumps(serialised)


def plan_from_json(plan_json: str) -> List[Any]:
    """
    Convert stored JSON back into lightweight objects that look like your
    original plan objects (day.day, day.meals[*].time_str, .meal).
    """
    raw = json.loads(plan_json)
    result: List[Any] = []

    for day_data in raw:
        day_date = date.fromisoformat(day_data["day"])
        slots = []

        for slot_data in day_data.get("meals", []):
            meal_name = slot_data["meal_name"]
            time_str = slot_data["time_str"]

            # find matching meal object from MEALS by name
            meal = next((m for m in MEALS if m.name == meal_name), None)
            if not meal:
                # silently skip if meal list changed
                continue

            slot = SimpleNamespace(time_str=time_str, meal=meal)
            slots.append(slot)

        day_obj = SimpleNamespace(day=day_date, meals=slots)
        result.append(day_obj)

    return result


def save_user_plan(user_id: int, plan: List[Any]) -> None:
    json_str = plan_to_json(plan)
    db_save_plan(user_id, json_str)


def load_user_plan(user_id: int) -> List[Any]:
    plan_json = db_load_latest_plan(user_id)
    if not plan_json:
        return []
    return plan_from_json(plan_json)
