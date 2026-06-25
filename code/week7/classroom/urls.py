from django.urls import path
from . import views
from graphene_django.views import GraphQLView

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("students/", views.student_list, name="student-list"),
    path("students/add/", views.add_student, name="add-student"),
]
urlpatterns += [
    path("articles/", views.article_list, name="article_list"),
    path("articles/<int:pk>/", views.article_detail, name="article_detail"),
]
urlpatterns += [
    path('api/students/', views.student_list, name='student-list'),
    path('api/students/<int:pk>/', views.student_detail),
    path('api/students/create/', views.student_create, name='student_create'),
    path('api/students/<int:pk>/update/', views.student_update, name='student_update'),
    path('api/students/<int:pk>/delete/', views.student_delete, name='student_delete'),

]

urlpatterns += [
    path("graphql/", GraphQLView.as_view(graphiql=True)),
]