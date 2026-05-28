from django.shortcuts import render, redirect
from .models import  Student
from django.utils import timezone
from django.db.models import Count
from .forms import StudentForm
from django.http import HttpResponse

# Create your views here.
def student_list(request):
    qs = Student.objects.all()
    return render(request, "classroom/student_list.html", {
        "students": qs,
        "count": qs.count(),
        "is_empty" : not qs.exists(),
    })

def dashboard(request):
    today = timezone.now().date()
    stats = {
        "total": Student.objects.count(),
        "joined_today": Student.objects.filter(join_date=today).count(),
        "by_day": Student.objects.extra({'day': "date(join_date)"}).values('day').annotate(c=Count('id')),
    }
    return render(request, "classroom/dashboard.html", {"stats": stats})

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            # track in session (see later)
            request.session['added_count'] = request.session.get('added_count', 0) + 1
            return redirect("student-list")
    else:
        form = StudentForm()
    return render(request, "classroom/add_student.html", {"form": form})

def visit_counter(request):
    visits = request.session.get("visits", 0) + 1
    request.session["visits"] = visits
    return render(request, "classroom/visit_counter.html", {"visits": visits})

def set_fav_color(request):
    resp = HttpResponse("Favourite color set!")
    resp.set_cookie("fav_color", "blue", max_age=3600)
    return resp