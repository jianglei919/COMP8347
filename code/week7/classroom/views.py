from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .forms import StudentForm
from .models import Student
from .models import Article
from .serializers import StudentSerializer

# Create your views here.
@login_required
def profile(request):
    return render(request, "classroom/profile.html",
{"user": request.user
    })


def student_list(request):
    qs = Student.objects.all()
    return render(request, 'classroom/student_list.html', {
        "students": qs,
        "count" : qs.count(),
        "is_empty" : not qs.exists(),
    })

def dashboard(request):
    today = timezone.now().date()
    stats = {
        "total" : Student.objects.count(),
        "joined_today" : Student.objects.filter(join_date=today).count(),
        "by_day" : Student.objects.extra({'day': "date(join_date"}).values('day').annotate(c=Count('id')),
    }
    return render(request, 'classroom/dashboard.html', {"stats" : stats})

@login_required
@permission_required('classroom.add_student',raise_exception=True)
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            #track in session
            request.session['added_count'] = request.session.get('added_count', 0) + 1
            return redirect("student-list")
    else:
        form = StudentForm()
    return render(request, 'classroom/add_student.html', {'form': form})

@login_required
def dashboard(request):
    student_count = Student.objects.count()
    user = request.user
    context = {
        "student_count": student_count,
        "user": user,
    }
    return render(request, "classroom/dashboard.html", context)

def visit_counter(request):
    visits = request.session.get("visits", 0) + 1
    request.session["visits"] = visits

    return render(request, "classroom/visit_counter.html", {"visits" : visits})

def set_fave_color(request):
    resp = HttpResponse("Your favorite color set!")
    resp.set_cookie("fav_color", "blue", max_age=3600)
    return resp

def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, "classroom/article_list.html", {"articles": articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, "classroom/article_detail.html", {"article": article})

@api_view(['GET'])
@permission_classes([AllowAny])
def student_list(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def student_detail(request, pk):
    student = Student.objects.get(pk=pk)
    serializer = StudentSerializer(student)
    return Response(serializer.data)

@api_view(['POST'])
def student_create(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['PUT'])
def student_update(request, pk):
    student = Student.objects.get(pk=pk)
    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
def student_delete(request, pk):
    student = Student.objects.get(pk=pk)
    student.delete()
    return Response({'message': 'Student deleted successfully'})





