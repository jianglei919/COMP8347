from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("students/", views.student_list, name="student-list"),
    path("students/add/", views.add_student, name="add-student"),
]
urlpatterns += [
    path("articles/", views.article_list, name="article_list"),
    path("articles/<int:pk>/", views.article_detail, name="article_detail"),
]
