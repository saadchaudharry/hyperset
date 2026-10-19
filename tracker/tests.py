import json
from datetime import date, timedelta
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from .models import AISettings, BodyMeasurement, CoachMessage, Exercise, ExerciseLog, FoodEntry, TemplateExercise, WorkoutDay

MONDAY = "2026-10-19"


def fake_response(content=None, tool_calls=None):
    message = SimpleNamespace(content=content, tool_calls=tool_calls)
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


class TrackerTests(TestCase):
    def setUp(self):
        user = User.objects.create_superuser("me", "me@example.com", "pass")
        self.client.force_login(user)
        AISettings.objects.create(api_key="test-key", model="gemini/gemini-2.5-flash")

    def test_seed_data(self):
        self.assertGreater(Exercise.objects.count(), 300)
        self.assertEqual(WorkoutDay.objects.count(), 7)
        self.assertEqual(WorkoutDay.objects.get(weekday=0).items.count(), 7)

    def test_day_page_shows_template(self):
        response = self.client.get(f"/day/{MONDAY}/")
        self.assertContains(response, "Incline Dumbbell Press")
        self.assertContains(response, "Push")

    def test_save_sets_and_complete(self):
        exercise = Exercise.objects.get(name="Incline Dumbbell Press")
        self.client.post(
            f"/day/{MONDAY}/log/{exercise.id}/",
            {"reps": ["10", "9", ""], "weight": ["20", "20", ""], "completed": "on"},
        )
        log = ExerciseLog.objects.get(date=MONDAY, exercise=exercise)
        self.assertTrue(log.completed)
        self.assertEqual([s.reps for s in log.sets.all()], [10, 9])

    def test_add_extra_exercise_to_day(self):
        self.client.post(f"/day/{MONDAY}/add-exercise/", {"name": "push-up"})
        self.assertTrue(ExerciseLog.objects.filter(date=MONDAY, exercise__name="Push-Up").exists())

    def test_remove_extra_exercise_from_day(self):
        self.client.post(f"/day/{MONDAY}/add-exercise/", {"name": "Push-Up"})
        exercise = Exercise.objects.get(name="Push-Up")
        self.client.post(f"/day/{MONDAY}/remove/{exercise.id}/")
        self.assertFalse(ExerciseLog.objects.filter(date=MONDAY, exercise=exercise).exists())

    def test_add_food_manual_calories(self):
        self.client.post(f"/day/{MONDAY}/food/", {"meal": "lunch", "description": "Rice", "calories": "300"})
        entry = FoodEntry.objects.get()
        self.assertEqual(entry.calories, 300)
        self.assertFalse(entry.ai_estimated)

    @patch("tracker.ai.litellm.completion")
    def test_add_food_ai_estimate(self, completion):
        completion.return_value = fake_response(
            '```json\n{"calories": 520, "protein_g": 24, "carbs_g": 60, "fat_g": 18, "notes": "3 rotis + dal"}\n```'
        )
        self.client.post(f"/day/{MONDAY}/food/", {"meal": "lunch", "description": "3 rotis and dal"})
        entry = FoodEntry.objects.get()
        self.assertEqual(entry.calories, 520)
        self.assertTrue(entry.ai_estimated)
        self.assertEqual(completion.call_args.kwargs["api_key"], "test-key")

    def test_add_food_without_api_key_shows_error(self):
        AISettings.objects.update(api_key="")
        response = self.client.post(f"/day/{MONDAY}/food/", {"description": "Banana"}, follow=True)
        self.assertContains(response, "Gemini API key")
        self.assertEqual(FoodEntry.objects.count(), 0)

    @patch("tracker.ai.litellm.completion")
    def test_coach_uses_tools(self, completion):
        FoodEntry.objects.create(date=date.today(), description="Eggs", calories=300, protein_g=20)
        tool_call = SimpleNamespace(
            id="call_1",
            function=SimpleNamespace(
                name="get_logs",
                arguments=json.dumps({"start_date": date.today().isoformat(), "end_date": date.today().isoformat()}),
            ),
        )
        completion.side_effect = [fake_response(tool_calls=[tool_call]), fake_response("- Eat 100 g more protein")]

        response = self.client.post("/coach/send/", json.dumps({"message": "What next?"}), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("100 g more protein", response.json()["reply_html"])
        tool_message = completion.call_args_list[1].kwargs["messages"][-1]
        self.assertEqual(tool_message["role"], "tool")
        self.assertIn("Eggs", tool_message["content"])
        self.assertEqual(CoachMessage.objects.count(), 2)

    def test_plan_add_move_delete(self):
        self.client.post("/plan/3/add/", {"name": "Plank", "sets": "3", "reps": "45 s", "rest": "60 s"})
        self.client.post("/plan/3/add/", {"name": "Crunch", "sets": "3", "reps": "15", "rest": ""})
        thursday = WorkoutDay.objects.get(weekday=3)
        crunch = TemplateExercise.objects.get(day=thursday, exercise__name="Crunch")
        self.client.post(f"/plan/item/{crunch.id}/", {"action": "up"})
        self.assertEqual([i.exercise.name for i in thursday.items.all()], ["Crunch", "Plank"])
        self.client.post(f"/plan/item/{crunch.id}/", {"action": "delete"})
        self.assertEqual(thursday.items.count(), 1)

    def test_profile_save_logs_weight(self):
        response = self.client.post("/profile/", {
            "weight_kg": "64.2", "waist_cm": "78", "height_cm": "173", "age": "27",
            "calorie_target": "2400", "protein_target_g": "135", "goal": "Lean gain",
        })
        self.assertEqual(response.status_code, 302)
        entry = BodyMeasurement.objects.get()
        self.assertEqual(float(entry.weight_kg), 64.2)
        self.assertEqual(float(entry.waist_cm), 78)

    def test_report_insights(self):
        today = date.today()
        BodyMeasurement.objects.create(date=today - timedelta(days=14), weight_kg=63)
        BodyMeasurement.objects.create(date=today, weight_kg=63.8)
        FoodEntry.objects.create(date=today, description="Food", calories=1500, protein_g=80)
        exercise = Exercise.objects.get(name="Hip Thrust")
        for offset, weight in [(14, 40), (7, 45)]:
            log = ExerciseLog.objects.create(date=today - timedelta(days=offset), exercise=exercise, completed=True)
            log.sets.create(set_number=1, reps=10, weight_kg=weight)

        response = self.client.get("/profile/?days=30")

        self.assertContains(response, "Gaining +0.40 kg a week")
        self.assertContains(response, "Calories 800 kcal below target")
        self.assertContains(response, "Hip Thrust up 5 kg")
        self.assertContains(response, 'id="chart-data"')

    def test_pages_load(self):
        for url in ["/plan/", "/profile/", "/profile/?days=7", "/profile/?days=90", "/exercises/", "/exercises/?q=curl&muscle=biceps", "/coach/", "/admin/tracker/aisettings/"]:
            self.assertEqual(self.client.get(url).status_code, 200, url)
        exercise = Exercise.objects.first()
        self.assertEqual(self.client.get(f"/exercises/{exercise.id}/").status_code, 200)


class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("saad", "saad@example.com", "old-pass-123")

    def test_pages_need_login(self):
        response = self.client.get("/plan/")
        self.assertRedirects(response, "/login/?next=/plan/")

    def test_login_and_logout(self):
        response = self.client.post("/login/", {"username": "saad", "password": "old-pass-123"})
        self.assertRedirects(response, "/", fetch_redirect_response=False)
        response = self.client.post("/logout/")
        self.assertRedirects(response, "/login/")
        self.assertEqual(self.client.get("/plan/").status_code, 302)

    def test_wrong_password_shows_error(self):
        response = self.client.post("/login/", {"username": "saad", "password": "nope"})
        self.assertContains(response, "Wrong username or password")

    def test_password_reset_flow(self):
        from django.core import mail

        self.client.post("/password-reset/", {"email": "saad@example.com"})
        self.assertEqual(len(mail.outbox), 1)
        link = next(line for line in mail.outbox[0].body.splitlines() if "/reset/" in line).strip()
        path = link.split("testserver")[1]
        response = self.client.get(path, follow=True)
        self.assertContains(response, "Set a new password")
        set_url = response.redirect_chain[-1][0]
        self.client.post(set_url, {"new_password1": "new-pass-456!", "new_password2": "new-pass-456!"})
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new-pass-456!"))
