from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

AUTH = "tracker/auth/"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name=AUTH + "login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name=AUTH + "password_reset_form.html",
            email_template_name=AUTH + "password_reset_email.txt",
            subject_template_name=AUTH + "password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path("password-reset/sent/", auth_views.PasswordResetDoneView.as_view(template_name=AUTH + "password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name=AUTH + "password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name=AUTH + "password_reset_complete.html"), name="password_reset_complete"),
    path("", views.home, name="home"),
    path("day/<str:day>/", views.day_view, name="day"),
    path("day/<str:day>/log/<int:exercise_id>/", views.save_exercise_log, name="save_exercise_log"),
    path("day/<str:day>/add-exercise/", views.add_exercise_to_day, name="add_exercise_to_day"),
    path("day/<str:day>/remove/<int:exercise_id>/", views.remove_exercise_from_day, name="remove_exercise_from_day"),
    path("day/<str:day>/food/", views.add_food, name="add_food"),
    path("food/<int:pk>/delete/", views.delete_food, name="delete_food"),
    path("plan/", views.plan_view, name="plan"),
    path("plan/<int:weekday>/", views.update_plan_day, name="update_plan_day"),
    path("plan/<int:weekday>/add/", views.add_plan_item, name="add_plan_item"),
    path("plan/item/<int:pk>/", views.update_plan_item, name="update_plan_item"),
    path("exercises/", views.exercise_list, name="exercises"),
    path("exercises/<int:pk>/", views.exercise_detail, name="exercise_detail"),
    path("profile/", views.profile_view, name="profile"),
    path("coach/", views.coach_view, name="coach"),
    path("coach/send/", views.coach_send, name="coach_send"),
    path("coach/clear/", views.coach_clear, name="coach_clear"),
]
