from django import forms

from .models import Exercise, Profile


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "muscle_group", "equipment", "category", "instructions"]
        widgets = {"instructions": forms.Textarea(attrs={"rows": 8})}


class ProfileForm(forms.ModelForm):
    waist_cm = forms.DecimalField(label="Waist (cm)", max_digits=5, decimal_places=1, required=False)

    class Meta:
        model = Profile
        fields = ["weight_kg", "waist_cm", "height_cm", "age", "calorie_target", "protein_target_g", "goal"]
        labels = {
            "weight_kg": "Weight today (kg)",
            "height_cm": "Height (cm)",
            "calorie_target": "Daily calories (kcal)",
            "protein_target_g": "Daily protein (g)",
        }
        widgets = {"goal": forms.Textarea(attrs={"rows": 3})}
