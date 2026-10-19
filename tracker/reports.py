"""Numbers behind the profile page: body trend, nutrition, training and strength over a date range."""

from collections import defaultdict
from datetime import timedelta

from django.utils import timezone

from .models import BodyMeasurement, ExerciseLog, FoodEntry, Profile, WorkoutDay

RANGES = [7, 30, 90]
GAIN_PER_WEEK_MIN = 0.1
GAIN_PER_WEEK_MAX = 0.25
STALL_SESSIONS = 3


def build_report(days):
    today = timezone.localdate()
    start = today - timedelta(days=days - 1)
    dates = [start + timedelta(days=i) for i in range(days)]
    profile = Profile.load()

    nutrition = nutrition_summary(start, today, profile)
    training = training_summary(start, today, dates)
    body = body_summary(start, today)

    return {
        "days": days,
        "start": start,
        "end": today,
        "nutrition": nutrition,
        "training": training,
        "body": body,
        "insights": build_insights(profile, nutrition, training, body, days),
        "charts": {
            "calories": {
                "labels": [d.strftime("%d %b") for d in dates],
                "values": [nutrition["calories_by_date"].get(d) for d in dates],
                "target": profile.calorie_target,
                "unit": "kcal",
            },
            "protein": {
                "labels": [d.strftime("%d %b") for d in dates],
                "values": [nutrition["protein_by_date"].get(d) for d in dates],
                "target": profile.protein_target_g,
                "unit": "g",
            },
            "weight": {
                "labels": [m.date.strftime("%d %b") for m in body["entries"]],
                "values": [float(m.weight_kg) for m in body["entries"]],
                "unit": "kg",
            },
            "volume": {
                "labels": [f"Wk {w.strftime('%d %b')}" for w, _ in training["volume_by_week"]],
                "values": [round(v) for _, v in training["volume_by_week"]],
                "unit": "kg",
            },
        },
    }


def nutrition_summary(start, end, profile):
    calories_by_date = defaultdict(int)
    protein_by_date = defaultdict(float)
    for entry in FoodEntry.objects.filter(date__range=(start, end)):
        calories_by_date[entry.date] += entry.calories
        protein_by_date[entry.date] += float(entry.protein_g)

    logged_days = len(calories_by_date)
    avg_calories = round(sum(calories_by_date.values()) / logged_days) if logged_days else None
    avg_protein = round(sum(protein_by_date.values()) / logged_days) if logged_days else None
    protein_days_hit = sum(1 for p in protein_by_date.values() if p >= profile.protein_target_g)
    return {
        "calories_by_date": dict(calories_by_date),
        "protein_by_date": {d: round(p) for d, p in protein_by_date.items()},
        "logged_days": logged_days,
        "avg_calories": avg_calories,
        "avg_protein": avg_protein,
        "protein_days_hit": protein_days_hit,
        "calorie_target": profile.calorie_target,
        "protein_target": profile.protein_target_g,
    }


def training_summary(start, end, dates):
    plan = {d.weekday: d for d in WorkoutDay.objects.prefetch_related("items")}
    logs = ExerciseLog.objects.filter(date__range=(start, end)).select_related("exercise").prefetch_related("sets")

    trained_dates = set()
    sets_by_muscle = defaultdict(int)
    volume_by_week = defaultdict(float)
    total_sets = 0
    best_by_exercise = defaultdict(list)
    for log in logs:
        sets = list(log.sets.all())
        if log.completed:
            trained_dates.add(log.date)
        total_sets += len(sets)
        sets_by_muscle[log.exercise.get_muscle_group_display()] += len(sets)
        week_start = log.date - timedelta(days=log.date.weekday())
        volume_by_week[week_start] += sum(s.reps * float(s.weight_kg) for s in sets)
        if sets:
            best = max(sets, key=lambda s: (s.weight_kg, s.reps))
            best_by_exercise[log.exercise.name].append((log.date, float(best.weight_kg), best.reps))

    # Today only counts once it is trained, so an unfinished day isn't a miss.
    planned_dates = [
        d for d in dates
        if plan.get(d.weekday()) and plan[d.weekday()].items.all() and (d < end or d in trained_dates)
    ]
    missed = defaultdict(int)
    for d in planned_dates:
        if d not in trained_dates:
            missed[plan[d.weekday()].title] += 1
    planned_done = sum(1 for d in planned_dates if d in trained_dates)

    weeks = max(1, len(dates) / 7)
    muscle_rows = sorted(sets_by_muscle.items(), key=lambda row: -row[1])
    max_sets = muscle_rows[0][1] if muscle_rows else 0

    return {
        "workout_days": len(trained_dates),
        "planned_days": len(planned_dates),
        "planned_done": planned_done,
        "consistency": round(planned_done * 100 / len(planned_dates)) if planned_dates else None,
        "missed": sorted(missed.items(), key=lambda row: -row[1]),
        "total_sets": total_sets,
        "total_volume": round(sum(volume_by_week.values())),
        "volume_by_week": sorted(volume_by_week.items()),
        "muscle_sets": [
            {
                "name": name,
                "sets": count,
                "per_week": round(count / weeks, 1),
                "pct": round(count * 100 / max_sets) if max_sets else 0,
            }
            for name, count in muscle_rows
        ],
        "strength": strength_progress(best_by_exercise),
    }


def strength_progress(best_by_exercise):
    rows = []
    for name, sessions in best_by_exercise.items():
        sessions.sort()
        first_date, first_weight, first_reps = sessions[0]
        last_date, last_weight, last_reps = sessions[-1]
        recent = [weight for _, weight, _ in sessions[-STALL_SESSIONS:]]
        rows.append({
            "name": name,
            "sessions": len(sessions),
            "first": f"{first_reps} × {first_weight:g} kg",
            "last": f"{last_reps} × {last_weight:g} kg",
            "change": round(last_weight - first_weight, 2),
            "change_label": f"{last_weight - first_weight:+g} kg" if last_weight != first_weight else "0 kg",
            "stalled": len(sessions) >= STALL_SESSIONS and max(recent) <= recent[0],
        })
    rows.sort(key=lambda row: (-row["change"], -row["sessions"]))
    return rows


def body_summary(start, end):
    entries = list(BodyMeasurement.objects.filter(date__range=(start, end)))
    latest = BodyMeasurement.objects.order_by("-date").first()
    rate = None
    weight_change = None
    waist_change = None
    if len(entries) >= 2:
        first, last = entries[0], entries[-1]
        weight_change = round(float(last.weight_kg - first.weight_kg), 1)
        span_days = (last.date - first.date).days
        if span_days >= 7:
            rate = round(weight_change / (span_days / 7), 2)
        waists = [e for e in entries if e.waist_cm is not None]
        if len(waists) >= 2:
            waist_change = round(float(waists[-1].waist_cm - waists[0].waist_cm), 1)
    return {
        "entries": entries,
        "latest": latest,
        "weight_change": weight_change,
        "rate_per_week": rate,
        "waist_change": waist_change,
    }


def build_insights(profile, nutrition, training, body, days):
    """Plain-language findings. Each is (status, title, detail) with status good / warn / info."""
    insights = []

    rate = body["rate_per_week"]
    if rate is None:
        insights.append(("info", "Weight trend not available yet",
                         "Log your weight at least twice, a week apart, to see how fast you are gaining."))
    elif rate < GAIN_PER_WEEK_MIN:
        insights.append(("warn", f"Gaining {rate:+.2f} kg a week",
                         "That is below the 0.1-0.25 kg target. Add about 150 kcal a day and recheck in 2 weeks."))
    elif rate > GAIN_PER_WEEK_MAX:
        insights.append(("warn", f"Gaining {rate:+.2f} kg a week",
                         "That is faster than the 0.1-0.25 kg target, so some of it is likely fat. "
                         "Trim about 150 kcal a day."))
    else:
        insights.append(("good", f"Gaining {rate:+.2f} kg a week", "Right in the lean-gain range. Keep calories where they are."))

    if body["waist_change"] is not None and body["waist_change"] > 1:
        insights.append(("warn", f"Waist up {body['waist_change']:g} cm",
                         "Waist is growing faster than expected for a lean gain. Hold calories steady for a week."))

    if nutrition["logged_days"]:
        avg, target = nutrition["avg_calories"], nutrition["calorie_target"]
        diff = avg - target
        if abs(diff) <= target * 0.1:
            insights.append(("good", f"Calories on target ({avg} kcal avg)", f"Within 10% of your {target} kcal goal."))
        else:
            word = "below" if diff < 0 else "above"
            insights.append(("warn", f"Calories {abs(diff)} kcal {word} target",
                             f"You averaged {avg} kcal against a {target} kcal goal on days you logged food."))

        hit, logged = nutrition["protein_days_hit"], nutrition["logged_days"]
        status = "good" if hit >= logged * 0.8 else "warn"
        insights.append((status, f"Protein target hit on {hit} of {logged} days",
                         f"Average {nutrition['avg_protein']} g a day against {nutrition['protein_target']} g. "
                         "Spread protein over 3-5 meals."))
        if logged < days * 0.7:
            insights.append(("info", f"Food logged on {logged} of {days} days",
                             "Log every day so calorie and protein numbers are reliable."))
    else:
        insights.append(("info", "No food logged in this period", "Add meals on the Today page to see nutrition insights."))

    if training["planned_days"]:
        consistency = training["consistency"]
        status = "good" if consistency >= 80 else "warn"
        detail = f"{training['planned_done']} of {training['planned_days']} planned workouts completed."
        if training["missed"]:
            missed = ", ".join(f"{title} ×{count}" for title, count in training["missed"][:3])
            detail += f" Missed: {missed}."
        insights.append((status, f"{consistency}% workout consistency", detail))

    improving = [row for row in training["strength"] if row["change"] > 0]
    if improving:
        top = improving[0]
        insights.append(("good", f"{top['name']} up {top['change']:g} kg",
                         f"From {top['first']} to {top['last']} over {top['sessions']} sessions."))
    for row in training["strength"]:
        if row["stalled"]:
            insights.append(("warn", f"{row['name']} has stalled",
                             f"No weight increase in the last {STALL_SESSIONS} sessions. "
                             "Aim for one more rep per set before adding weight, and check sleep and food."))
            break

    return insights
