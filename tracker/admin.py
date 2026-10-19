from django.contrib import admin

from .models import (
    AISettings,
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


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AISettings)
class AISettingsAdmin(SingletonAdmin):
    fields = ["api_key", "model"]


@admin.register(Profile)
class ProfileAdmin(SingletonAdmin):
    pass


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["name", "muscle_group", "equipment", "category"]
    list_filter = ["muscle_group", "equipment", "category"]
    search_fields = ["name"]


class TemplateExerciseInline(admin.TabularInline):
    model = TemplateExercise
    autocomplete_fields = ["exercise"]
    extra = 0


@admin.register(WorkoutDay)
class WorkoutDayAdmin(admin.ModelAdmin):
    list_display = ["weekday", "title", "focus"]
    inlines = [TemplateExerciseInline]


class SetEntryInline(admin.TabularInline):
    model = SetEntry
    extra = 0


@admin.register(ExerciseLog)
class ExerciseLogAdmin(admin.ModelAdmin):
    list_display = ["date", "exercise", "completed"]
    list_filter = ["date", "completed"]
    inlines = [SetEntryInline]


@admin.register(FoodEntry)
class FoodEntryAdmin(admin.ModelAdmin):
    list_display = ["date", "meal", "description", "calories", "protein_g", "ai_estimated"]
    list_filter = ["date", "meal"]


@admin.register(CoachMessage)
class CoachMessageAdmin(admin.ModelAdmin):
    list_display = ["created_at", "role", "content"]


@admin.register(BodyMeasurement)
class BodyMeasurementAdmin(admin.ModelAdmin):
    list_display = ["date", "weight_kg", "waist_cm"]
