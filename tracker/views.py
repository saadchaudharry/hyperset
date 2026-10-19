import html
import json
import re
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from urllib.parse import quote

import markdown
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST

from . import ai, reports
from .forms import ExerciseForm, ProfileForm
from .models import (
    EQUIPMENT,
    MEALS,
    MUSCLE_GROUPS,
    BodyMeasurement,
    CoachMessage,
    Exercise,
    ExerciseLog,
    FoodEntry,
    Profile,
    SetEntry,
    TemplateExercise,
    WorkoutDay,
)

DEFAULT_EXTRA_SETS = 3
COACH_HISTORY_LENGTH = 20


def parse_day(value):
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise Http404("Invalid date")


def day_url(day, anchor=""):
    url = reverse("day", args=[day.isoformat()])
    return f"{url}#{anchor}" if anchor else url


LIST_ITEM = re.compile(r"^\s*([-*+]|\d+\.)\s")


def render_markdown(text):
    # Python-Markdown needs a blank line before a list; LLM replies often skip it.
    lines = []
    for line in html.escape(text).splitlines():
        if LIST_ITEM.match(line) and lines and lines[-1].strip() and not LIST_ITEM.match(lines[-1]):
            lines.append("")
        lines.append(line)
    return mark_safe(markdown.markdown("\n".join(lines), extensions=["sane_lists"]))


# ---------- Daily log ----------

@login_required
def home(request):
    return redirect("day", day=timezone.localdate().isoformat())


@login_required
def day_view(request, day):
    day = parse_day(day)
    plan_day = WorkoutDay.objects.filter(weekday=day.weekday()).prefetch_related("items__exercise").first()
    logs = {
        log.exercise_id: log
        for log in ExerciseLog.objects.filter(date=day).select_related("exercise").prefetch_related("sets")
    }

    cards = []
    planned_items = plan_day.items.all() if plan_day else []
    for item in planned_items:
        cards.append(build_card(item.exercise, item, logs.pop(item.exercise_id, None)))
    for log in logs.values():
        cards.append(build_card(log.exercise, None, log))

    foods = FoodEntry.objects.filter(date=day)
    meals = [(label, [f for f in foods if f.meal == key]) for key, label in MEALS]
    profile = Profile.load()
    total_calories = sum(f.calories for f in foods)
    total_protein = sum(f.protein_g for f in foods)

    context = {
        "day": day,
        "today": timezone.localdate(),
        "prev_day": day - timedelta(days=1),
        "next_day": day + timedelta(days=1),
        "week": week_strip(day),
        "plan_day": plan_day,
        "cards": cards,
        "done_count": sum(1 for c in cards if c["log"] and c["log"].completed),
        "set_count": sum(len(c["log"].sets.all()) for c in cards if c["log"]),
        "meals": meals,
        "has_food": bool(foods),
        "meal_choices": MEALS,
        "profile": profile,
        "total_calories": total_calories,
        "total_protein": total_protein,
        "calorie_pct": min(100, round(total_calories * 100 / profile.calorie_target)) if profile.calorie_target else 0,
        "protein_pct": min(100, round(total_protein * 100 / profile.protein_target_g)) if profile.protein_target_g else 0,
        "exercise_names": Exercise.objects.values_list("name", flat=True),
        "food_draft": request.GET.get("food", ""),
        "active": "day",
    }
    return render(request, "tracker/day.html", context)


def build_card(exercise, item, log):
    if log and log.sets.all():
        rows = [(s.reps, s.weight_kg) for s in log.sets.all()]
    else:
        rows = [("", "")] * (item.sets if item else DEFAULT_EXTRA_SETS)
    return {"exercise": exercise, "item": item, "log": log, "rows": rows}


def week_strip(day):
    monday = day - timedelta(days=day.weekday())
    sunday = monday + timedelta(days=6)
    titles = {d.weekday: d.short_title for d in WorkoutDay.objects.all()}
    done_dates = set(
        ExerciseLog.objects.filter(date__range=(monday, sunday), completed=True).values_list("date", flat=True)
    )
    strip = []
    for offset in range(7):
        d = monday + timedelta(days=offset)
        strip.append({"date": d, "title": titles.get(d.weekday(), "Rest"), "done": d in done_dates})
    return strip


@login_required
@require_POST
def save_exercise_log(request, day, exercise_id):
    day = parse_day(day)
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    log, _ = ExerciseLog.objects.get_or_create(date=day, exercise=exercise)
    log.completed = "completed" in request.POST
    log.save()

    log.sets.all().delete()
    set_number = 0
    for reps, weight in zip(request.POST.getlist("reps"), request.POST.getlist("weight")):
        if not reps.strip():
            continue
        try:
            reps_value = int(reps)
            weight_value = Decimal(weight or "0")
        except (ValueError, InvalidOperation):
            messages.error(request, f"{exercise.name}: reps and weight must be numbers.")
            continue
        set_number += 1
        SetEntry.objects.create(log=log, set_number=set_number, reps=reps_value, weight_kg=weight_value)

    messages.success(request, f"{exercise.name} saved" + (" and marked complete." if log.completed else "."))
    return redirect(day_url(day, f"ex-{exercise.id}"))


@login_required
@require_POST
def add_exercise_to_day(request, day):
    day = parse_day(day)
    exercise = Exercise.objects.filter(name__iexact=request.POST.get("name", "").strip()).first()
    if not exercise:
        messages.error(request, "Exercise not found. Pick one from the list or add it in Exercises first.")
        return redirect(day_url(day, "workout"))
    ExerciseLog.objects.get_or_create(date=day, exercise=exercise)
    return redirect(day_url(day, f"ex-{exercise.id}"))


@login_required
@require_POST
def remove_exercise_from_day(request, day, exercise_id):
    day = parse_day(day)
    log = get_object_or_404(ExerciseLog, date=day, exercise_id=exercise_id)
    log.delete()
    messages.success(request, f"{log.exercise.name} removed from this day.")
    return redirect(day_url(day, "workout"))


@login_required
@require_POST
def add_food(request, day):
    day = parse_day(day)
    description = request.POST.get("description", "").strip()
    meal = request.POST.get("meal", "snack")
    calories = request.POST.get("calories", "").strip()
    if not description:
        messages.error(request, "Describe what you ate.")
        return redirect(day_url(day, "food"))

    entry = FoodEntry(date=day, meal=meal, description=description)
    if calories:
        try:
            entry.calories = int(calories)
            entry.protein_g = Decimal(request.POST.get("protein") or "0")
        except (ValueError, InvalidOperation):
            messages.error(request, "Calories and protein must be numbers.")
            return redirect(day_url(day, "food"))
    else:
        try:
            estimate = ai.estimate_food(description)
        except ai.AIError as exc:
            messages.error(request, str(exc))
            return redirect(f"{day_url(day)}?food={quote(description)}#food")
        entry.calories = estimate["calories"]
        entry.protein_g = estimate["protein_g"]
        entry.carbs_g = estimate["carbs_g"]
        entry.fat_g = estimate["fat_g"]
        entry.ai_notes = estimate["notes"]
        entry.ai_estimated = True
    entry.save()
    messages.success(request, f"Added {entry.calories} kcal.")
    return redirect(day_url(day, "food"))


@login_required
@require_POST
def delete_food(request, pk):
    entry = get_object_or_404(FoodEntry, pk=pk)
    entry.delete()
    return redirect(day_url(entry.date, "food"))


# ---------- Weekly plan ----------

@login_required
def plan_view(request):
    days = WorkoutDay.objects.prefetch_related("items__exercise")
    return render(request, "tracker/plan.html", {
        "days": days,
        "exercise_names": Exercise.objects.values_list("name", flat=True),
        "today_weekday": timezone.localdate().weekday(),
        "active": "plan",
    })


@login_required
@require_POST
def update_plan_day(request, weekday):
    plan_day = get_object_or_404(WorkoutDay, weekday=weekday)
    plan_day.title = request.POST.get("title", "").strip() or "Rest"
    plan_day.focus = request.POST.get("focus", "").strip()
    plan_day.save()
    messages.success(request, f"{plan_day.get_weekday_display()} saved.")
    return redirect(f"{reverse('plan')}#day-{weekday}")


@login_required
@require_POST
def add_plan_item(request, weekday):
    plan_day = get_object_or_404(WorkoutDay, weekday=weekday)
    exercise = Exercise.objects.filter(name__iexact=request.POST.get("name", "").strip()).first()
    if not exercise:
        messages.error(request, "Exercise not found. Pick one from the list or add it in Exercises first.")
        return redirect(f"{reverse('plan')}#day-{weekday}")
    TemplateExercise.objects.create(
        day=plan_day,
        exercise=exercise,
        order=plan_day.items.count(),
        sets=int(request.POST.get("sets") or 3),
        reps=request.POST.get("reps", "").strip() or "8-12",
        rest=request.POST.get("rest", "").strip(),
    )
    return redirect(f"{reverse('plan')}#day-{weekday}")


@login_required
@require_POST
def update_plan_item(request, pk):
    item = get_object_or_404(TemplateExercise, pk=pk)
    weekday = item.day.weekday
    action = request.POST.get("action")

    if action == "delete":
        item.delete()
    elif action in ("up", "down"):
        items = list(item.day.items.all())
        index = items.index(item)
        swap = index - 1 if action == "up" else index + 1
        if 0 <= swap < len(items):
            items[index], items[swap] = items[swap], items[index]
        for order, each in enumerate(items):
            each.order = order
            each.save(update_fields=["order"])
    else:
        item.sets = int(request.POST.get("sets") or item.sets)
        item.reps = request.POST.get("reps", "").strip() or item.reps
        item.rest = request.POST.get("rest", "").strip()
        item.save()
    return redirect(f"{reverse('plan')}#day-{weekday}")


# ---------- Exercise library ----------

@login_required
def exercise_list(request):
    form = ExerciseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        exercise = form.save()
        messages.success(request, f"{exercise.name} added.")
        return redirect("exercise_detail", pk=exercise.pk)

    exercises = Exercise.objects.all()
    query = request.GET.get("q", "").strip()
    muscle = request.GET.get("muscle", "")
    equipment = request.GET.get("equipment", "")
    if query:
        exercises = exercises.filter(Q(name__icontains=query) | Q(instructions__icontains=query))
    if muscle:
        exercises = exercises.filter(muscle_group=muscle)
    if equipment:
        exercises = exercises.filter(equipment=equipment)

    return render(request, "tracker/exercises.html", {
        "exercises": exercises,
        "form": form,
        "query": query,
        "muscle": muscle,
        "equipment": equipment,
        "muscle_choices": MUSCLE_GROUPS,
        "equipment_choices": EQUIPMENT,
        "show_form": request.method == "POST",
        "active": "exercises",
    })


@login_required
def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    form = ExerciseForm(request.POST or None, instance=exercise)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Exercise saved.")
        return redirect("exercise_detail", pk=pk)

    return render(request, "tracker/exercise_detail.html", {
        "exercise": exercise,
        "form": form,
        "logs": exercise.logs.prefetch_related("sets")[:30],
        "plan_items": TemplateExercise.objects.filter(exercise=exercise).select_related("day"),
        "video_url": "https://www.youtube.com/results?search_query=" + quote(f"{exercise.name} proper form"),
        "active": "exercises",
    })


# ---------- Profile and reports ----------

@login_required
def profile_view(request):
    profile = Profile.load()
    today = timezone.localdate()
    todays_measurement = BodyMeasurement.objects.filter(date=today).first()
    form = ProfileForm(
        request.POST or None,
        instance=profile,
        initial={"waist_cm": todays_measurement.waist_cm if todays_measurement else None},
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        BodyMeasurement.objects.update_or_create(
            date=today,
            defaults={"weight_kg": profile.weight_kg, "waist_cm": form.cleaned_data["waist_cm"]},
        )
        messages.success(request, "Profile saved and today's weight logged.")
        return redirect("profile")

    days = int(request.GET.get("days", 30))
    if days not in reports.RANGES:
        days = 30
    report = reports.build_report(days)
    height_m = profile.height_cm / 100
    return render(request, "tracker/profile.html", {
        "profile": profile,
        "form": form,
        "bmi": round(float(profile.weight_kg) / (height_m * height_m), 1) if height_m else None,
        "has_measurements": BodyMeasurement.objects.exists(),
        "report": report,
        "ranges": reports.RANGES,
        "active": "profile",
    })


# ---------- AI coach ----------

@login_required
def coach_view(request):
    chat = [
        {"role": m.role, "html": render_markdown(m.content)}
        for m in CoachMessage.objects.all()
    ]
    return render(request, "tracker/coach.html", {"chat": chat, "active": "coach"})


@login_required
@require_POST
def coach_send(request):
    text = json.loads(request.body or "{}").get("message", "").strip()
    if not text:
        return JsonResponse({"error": "Type a question first."}, status=400)

    user_message = CoachMessage.objects.create(role="user", content=text)
    recent = CoachMessage.objects.order_by("-created_at", "-id")[:COACH_HISTORY_LENGTH]
    history = [{"role": m.role, "content": m.content} for m in reversed(recent)]
    try:
        reply = ai.coach_reply(history)
    except ai.AIError as exc:
        user_message.delete()
        return JsonResponse({"error": str(exc)}, status=502)

    CoachMessage.objects.create(role="assistant", content=reply)
    return JsonResponse({"user_html": render_markdown(text), "reply_html": render_markdown(reply)})


@login_required
@require_POST
def coach_clear(request):
    CoachMessage.objects.all().delete()
    return redirect("coach")
