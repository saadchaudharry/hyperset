from django.db import models

WEEKDAYS = [
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday"),
]

MUSCLE_GROUPS = [
    ("chest", "Chest"),
    ("back", "Back"),
    ("traps", "Traps"),
    ("lower_back", "Lower back"),
    ("shoulders", "Shoulders"),
    ("biceps", "Biceps"),
    ("triceps", "Triceps"),
    ("forearms", "Forearms"),
    ("abs", "Abs"),
    ("obliques", "Obliques"),
    ("quads", "Quads"),
    ("hamstrings", "Hamstrings"),
    ("glutes", "Glutes"),
    ("adductors", "Adductors"),
    ("abductors", "Abductors"),
    ("calves", "Calves"),
    ("neck", "Neck"),
    ("full_body", "Full body"),
    ("cardio", "Cardio"),
    ("mobility", "Mobility"),
]

EQUIPMENT = [
    ("barbell", "Barbell"),
    ("dumbbell", "Dumbbell"),
    ("machine", "Machine"),
    ("cable", "Cable"),
    ("bodyweight", "Bodyweight"),
    ("kettlebell", "Kettlebell"),
    ("band", "Band"),
    ("smith", "Smith machine"),
    ("ez_bar", "EZ bar"),
    ("trap_bar", "Trap bar"),
    ("medicine_ball", "Medicine ball"),
    ("other", "Other"),
]

CATEGORIES = [
    ("compound", "Compound"),
    ("isolation", "Isolation"),
    ("cardio", "Cardio"),
    ("plyometric", "Plyometric"),
    ("stretch", "Stretch / mobility"),
]

MEALS = [
    ("breakfast", "Breakfast"),
    ("lunch", "Lunch"),
    ("dinner", "Dinner"),
    ("snack", "Snack"),
]


class Exercise(models.Model):
    name = models.CharField(max_length=120, unique=True)
    muscle_group = models.CharField(max_length=20, choices=MUSCLE_GROUPS)
    equipment = models.CharField(max_length=20, choices=EQUIPMENT)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    instructions = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class WorkoutDay(models.Model):
    """One day of the weekly template. A day with no exercises is a rest day."""

    weekday = models.IntegerField(choices=WEEKDAYS, unique=True)
    title = models.CharField(max_length=60, default="Rest")
    focus = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["weekday"]

    def __str__(self):
        return f"{self.get_weekday_display()} - {self.title}"

    @property
    def short_title(self):
        return self.title.split()[0] if self.title else "Rest"


class TemplateExercise(models.Model):
    day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name="items")
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    order = models.PositiveIntegerField(default=0)
    sets = models.PositiveIntegerField(default=3)
    reps = models.CharField(max_length=20, default="8-12")
    rest = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.exercise} {self.sets} x {self.reps}"


class ExerciseLog(models.Model):
    date = models.DateField()
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT, related_name="logs")
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date", "id"]
        unique_together = ["date", "exercise"]

    def __str__(self):
        return f"{self.date} {self.exercise}"


class SetEntry(models.Model):
    log = models.ForeignKey(ExerciseLog, on_delete=models.CASCADE, related_name="sets")
    set_number = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        ordering = ["set_number"]

    def __str__(self):
        return f"{self.reps} x {self.weight_kg} kg"


class FoodEntry(models.Model):
    date = models.DateField()
    meal = models.CharField(max_length=20, choices=MEALS, default="snack")
    description = models.CharField(max_length=300)
    calories = models.PositiveIntegerField(default=0)
    protein_g = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    carbs_g = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    fat_g = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    ai_estimated = models.BooleanField(default=False)
    ai_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "created_at"]
        verbose_name_plural = "food entries"

    def __str__(self):
        return f"{self.date} {self.description} ({self.calories} kcal)"


class BodyMeasurement(models.Model):
    date = models.DateField(unique=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1)
    waist_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.date} {self.weight_kg} kg"


class CoachMessage(models.Model):
    role = models.CharField(max_length=10, choices=[("user", "User"), ("assistant", "Assistant")])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"


class SingletonModel(models.Model):
    """A settings model with exactly one row (pk=1), edited in the admin."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Profile(SingletonModel):
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, default=63)
    height_cm = models.PositiveIntegerField(default=173)
    age = models.PositiveIntegerField(default=27)
    goal = models.TextField(
        default="Lean muscle gain: bigger chest, wider back, round shoulders, bigger arms and balanced legs. "
        "Gain 0.1-0.25 kg per week."
    )
    calorie_target = models.PositiveIntegerField(default=2300)
    protein_target_g = models.PositiveIntegerField(default=130)

    def __str__(self):
        return "Profile"


class AISettings(SingletonModel):
    api_key = models.CharField(max_length=200, blank=True, help_text="Your Gemini API key from Google AI Studio.")
    model = models.CharField(
        max_length=100,
        default="gemini/gemini-2.5-flash",
        help_text="AI model name, for example gemini/gemini-2.5-flash or gemini/gemini-2.5-pro.",
    )

    class Meta:
        verbose_name = "AI settings"
        verbose_name_plural = "AI settings"

    def __str__(self):
        return "AI settings"
