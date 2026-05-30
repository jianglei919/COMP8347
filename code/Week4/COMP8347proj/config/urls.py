"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hello.views import hello_world
from hello.views import greet
from classroom.views import student_list
from classroom.views import add_student
from classroom.views import visit_counter
from classroom.views import set_fav_color
from guestbook.views import entry_list, add_entry, set_name_cookie, clear_name_cookie

urlpatterns = [
    path('admin/', admin.site.urls),
    path("hello/", hello_world, name="hello"),
]
urlpatterns += [path("greet/", greet, name="greet")]
urlpatterns += [path("students/", student_list, name="student-list")]
urlpatterns += [path("students/add/", add_student, name="add-student")]
urlpatterns += [path("visit-counter/", visit_counter, name="visit-counter")]
urlpatterns += [path("set-color/", set_fav_color, name="set-fav-color")]
urlpatterns += [
    path("guestbook/", entry_list, name="gb-list"),
    path("guestbook/add/", add_entry, name="gb-add"),
    path("guestbook/name/set/", set_name_cookie, name="gb-set-name"),
    path("guestbook/name/clear/", clear_name_cookie, name="gb-clear-name"),
]