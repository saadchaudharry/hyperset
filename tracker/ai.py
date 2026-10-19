"""AI features: food calorie estimates and the AI coach (with tools)."""

import json
from datetime import date, timedelta

import litellm
from django.utils import timezone

from .models import AISettings, BodyMeasurement, ExerciseLog, FoodEntry, Profile, WorkoutDay

MAX_TOOL_ROUNDS = 6
MAX_LOG_DAYS = 31


class AIError(Exception):
    pass


def _complete(**kwargs):
    settings = AISettings.load()
    if not settings.api_key:
        raise AIError("Add your Gemini API key in Admin → AI settings first.")
    try:
        response = litellm.completion(model=settings.model, api_key=settings.api_key, **kwargs)
    except Exception as exc:
        raise AIError(f"AI request failed: {exc}") from exc
    return response.choices[0].message


# ---------- Food calorie estimate ----------

FOOD_PROMPT = """You estimate nutrition for food a person ate.
Use typical portion sizes when the amount is not given, including Indian dishes and household
measures such as roti, katori, bowl or plate.
Reply with only a JSON object, no other text:
{"calories": int, "protein_g": number, "carbs_g": number, "fat_g": number,
 "notes": "one short line with the per-item breakdown and assumed portions"}"""


def estimate_food(description):
    message = _complete(
        messages=[
            {"role": "system", "content": FOOD_PROMPT},
            {"role": "user", "content": description},
        ],
        temperature=0.2,
    )
    text = message.content or ""
    try:
        data = json.loads(text[text.index("{"): text.rindex("}") + 1])
        return {
            "calories": round(float(data["calories"])),
            "protein_g": round(float(data.get("protein_g", 0)), 1),
            "carbs_g": round(float(data.get("carbs_g", 0)), 1),
            "fat_g": round(float(data.get("fat_g", 0)), 1),
            "notes": str(data.get("notes", "")),
        }
    except (ValueError, KeyError, TypeError) as exc:
        raise AIError("The AI reply could not be read. Try again or enter calories yourself.") from exc


# ---------- Data the coach can look up ----------

def day_data(day):
    template = WorkoutDay.objects.filter(weekday=day.weekday()).first()
    foods = FoodEntry.objects.filter(date=day)
    logs = ExerciseLog.objects.filter(date=day).select_related("exercise").prefetch_related("sets")
    return {
        "date": day.isoformat(),
        "weekday": day.strftime("%A"),
        "planned_workout": template.title if template else "Rest",
        "total_calories": sum(f.calories for f in foods),
        "total_protein_g": float(sum(f.protein_g for f in foods)),
        "food": [
            {
                "meal": f.meal,
                "description": f.description,
                "calories": f.calories,
                "protein_g": float(f.protein_g),
                "carbs_g": float(f.carbs_g),
                "fat_g": float(f.fat_g),
            }
            for f in foods
        ],
        "exercises": [
            {
                "name": log.exercise.name,
                "completed": log.completed,
                "sets": [{"reps": s.reps, "weight_kg": float(s.weight_kg)} for s in log.sets.all()],
            }
            for log in logs
        ],
    }


def get_profile_and_plan():
    profile = Profile.load()
    plan = []
    for day in WorkoutDay.objects.prefetch_related("items__exercise"):
        plan.append({
            "weekday": day.get_weekday_display(),
            "title": day.title,
            "focus": day.focus,
            "exercises": [
                {"name": item.exercise.name, "sets": item.sets, "reps": item.reps, "rest": item.rest}
                for item in day.items.all()
            ],
        })
    return {
        "weight_kg": float(profile.weight_kg),
        "height_cm": profile.height_cm,
        "age": profile.age,
        "goal": profile.goal,
        "daily_calorie_target": profile.calorie_target,
        "daily_protein_target_g": profile.protein_target_g,
        "weekly_plan": plan,
        "recent_body_measurements": [
            {"date": m.date.isoformat(), "weight_kg": float(m.weight_kg),
             "waist_cm": float(m.waist_cm) if m.waist_cm is not None else None}
            for m in BodyMeasurement.objects.order_by("-date")[:30]
        ],
    }


def get_logs(start_date, end_date):
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    if (end - start).days >= MAX_LOG_DAYS:
        start = end - timedelta(days=MAX_LOG_DAYS - 1)
    days = []
    day = start
    while day <= end:
        days.append(day_data(day))
        day += timedelta(days=1)
    return {"days": days}


def get_exercise_history(exercise_name, limit=10):
    logs = (
        ExerciseLog.objects.filter(exercise__name__iexact=exercise_name)
        .prefetch_related("sets")
        .order_by("-date")[: int(limit)]
    )
    return {
        "exercise": exercise_name,
        "sessions": [
            {
                "date": log.date.isoformat(),
                "completed": log.completed,
                "sets": [{"reps": s.reps, "weight_kg": float(s.weight_kg)} for s in log.sets.all()],
            }
            for log in logs
        ],
    }


TOOL_FUNCTIONS = {
    "get_profile_and_plan": get_profile_and_plan,
    "get_logs": get_logs,
    "get_exercise_history": get_exercise_history,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_profile_and_plan",
            "description": "The user's body stats, goal, daily calorie and protein targets, weekly workout plan "
            "and recent body weight / waist measurements.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_logs",
            "description": "Food eaten (calories and macros) and exercises done (sets, reps, weight) for each day "
            "in a date range. At most 31 days.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                    "end_date": {"type": "string", "description": "YYYY-MM-DD"},
                },
                "required": ["start_date", "end_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_exercise_history",
            "description": "Recent sessions of one exercise with sets, reps and weight, newest first. "
            "Use it to suggest the next weight.",
            "parameters": {
                "type": "object",
                "properties": {
                    "exercise_name": {"type": "string"},
                    "limit": {"type": "integer", "description": "Number of sessions, default 10"},
                },
                "required": ["exercise_name"],
            },
        },
    },
]


def run_tool(name, arguments):
    try:
        args = json.loads(arguments or "{}")
        return TOOL_FUNCTIONS[name](**args)
    except Exception as exc:
        return {"error": str(exc)}


# ---------- AI coach ----------

COACH_PROMPT = """You are a practical strength and nutrition coach inside the user's workout tracker.
Today is {today} ({weekday}). Today's planned workout: {planned}.

Always use the tools to look up the user's profile, plan, food and workout logs before giving advice.
Never guess numbers you can look up.

Give specific next steps, for example:
- what to eat for the rest of the day to reach the calorie and protein targets
- which weights and reps to aim for next session (if every set reached the top of the rep range, add 1-2.5 kg)
- missed workouts, weak points and recovery

Keep replies short and use bullet points. You are not a doctor: for pain or injury, suggest seeing a professional."""


def coach_reply(history):
    """history: list of {"role": "user" | "assistant", "content": str}, oldest first."""
    today = timezone.localdate()
    template = WorkoutDay.objects.filter(weekday=today.weekday()).first()
    system = COACH_PROMPT.format(
        today=today.isoformat(),
        weekday=today.strftime("%A"),
        planned=template.title if template else "Rest",
    )
    messages = [{"role": "system", "content": system}] + history

    for _ in range(MAX_TOOL_ROUNDS):
        message = _complete(messages=messages, tools=TOOLS)
        if not message.tool_calls:
            return message.content or ""
        messages.append(message)
        for call in message.tool_calls:
            result = run_tool(call.function.name, call.function.arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "name": call.function.name,
                "content": json.dumps(result),
            })
    raise AIError("The coach needed too many steps. Try a more specific question.")
