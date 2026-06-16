from django.contrib import admin
from .models import Student
from .models import Article

# Register your models here.
admin.site.register(Student)
admin.site.register(Article)