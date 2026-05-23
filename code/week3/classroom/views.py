from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

from .models import Student

# Create your views here.
def student_list(request):
    qs = Student.objects.all()
    return render(request, "classroom/student_list.html", {
        "students": qs,
        "count": qs.count(),
        "is_empty" : not qs.exists(),
    })


def recent_students(request):
    days = 7
    cutoff = timezone.now().date() - timedelta(days=days)
    qs = Student.objects.filter(join_date__gte=cutoff).order_by("-join_date")
    return render(request, "classroom/recent_students.html", {
        "students": qs,
        "days": days,
        "count": qs.count(),
        "is_empty": not qs.exists(),
    })