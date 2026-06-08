from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("students/", views.student_list, name="student-list"),
    path("students/add/", views.add_student, name="add-student"),
]
