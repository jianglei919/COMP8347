from django.shortcuts import render
from .models import  Student

# Create your views here.
def student_list(request):
    qs = Student.objects.all()
    return render(request, "classroom/student_list.html", {
        "students": qs,
        "count": qs.count(),
        "is_empty" : not qs.exists(),
    })