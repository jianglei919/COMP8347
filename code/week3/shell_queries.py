"""Shell queries demo for Week 3 Class Activity.

Run with:
    python manage.py shell < shell_queries.py
"""
from datetime import timedelta

from django.utils import timezone

from classroom.models import Student

# --- Seed a few students so the queries have something to chew on -----------
Student.objects.all().delete()

s1 = Student.objects.create(name="Alice Wong",   email="alice@uwindsor.ca",  phone_number="+1-519-111-1111")
s2 = Student.objects.create(name="Bob Singh",    email="bob@uwindsor.ca",    phone_number="+1-519-222-2222")
s3 = Student.objects.create(name="Carla Mendes", email="carla@uwindsor.ca",  phone_number="+1-519-333-3333")
s4 = Student.objects.create(name="Dan Patel",    email="dan@uwindsor.ca",    phone_number="+1-519-444-4444")

# join_date is auto_now_add=True, so backdate two of them to test the recent view.
old = timezone.now().date() - timedelta(days=20)
Student.objects.filter(pk__in=[s3.pk, s4.pk]).update(join_date=old)

print("\n--- All students after seeding ---")
for s in Student.objects.all():
    print(s.pk, s.name, s.email, s.phone_number, s.join_date)

# --- 1) FILTER: students whose name contains 'a' (case-insensitive) ---------
print("\n--- Query 1 (FILTER): name__icontains='a' ---")
qs_filter = Student.objects.filter(name__icontains="a")
for s in qs_filter:
    print(s.pk, s.name, s.email)

# --- 2) ORDER: all students newest first -----------------------------------
print("\n--- Query 2 (ORDER): order_by('-join_date') ---")
qs_order = Student.objects.order_by("-join_date")
for s in qs_order:
    print(s.pk, s.name, s.join_date)

# --- 3) DELETE: remove students who joined more than 7 days ago ------------
cutoff = timezone.now().date() - timedelta(days=7)
print(f"\n--- Query 3 (DELETE): join_date__lt={cutoff} ---")
deleted, info = Student.objects.filter(join_date__lt=cutoff).delete()
print("Deleted:", deleted, info)

print("\n--- Remaining students after delete ---")
for s in Student.objects.all():
    print(s.pk, s.name, s.join_date)
