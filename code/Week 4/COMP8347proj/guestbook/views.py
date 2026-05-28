from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Entry
from .forms import EntryForm

def entry_list(request):
    qs = Entry.objects.all().order_by("-created_at")
    # Read display_name from cookie (optional)
    saved_name = request.COOKIES.get("displayname", "")
    added_count = request.session.get("gb_added", 0)
    return render(request, "guestbook/entry_list.html", {
        "entries": qs,
        "saved_name": saved_name,
        "added_count": added_count,
    })

def add_entry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            # BUG 3: session counter not incrementing
            request.session["gb_added"] = request.session.get("gb_added", 0)
            # On success, redirect to list
            return redirect("gb-list")
    else:
        # Prefill display_name from cookie if present
        initial = {"display_name": request.COOKIES.get("displayname", "")}
        # BUG 4: initial won't work because form doesn't include display_name
        form = EntryForm(initial=initial)

    return render(request, "guestbook/add_entry.html", {"form": form})

def set_name_cookie(request):
    # Sets a cookie so future forms can prefill display_name
    name = request.GET.get("name", "").strip()
    resp = HttpResponse("Name saved. You can go back.")
    # BUG 5: cookie name mismatch used elsewhere ("displayname" vs "display_name")
    resp.set_cookie("display_name", name, max_age=3600)
    return resp

def clear_name_cookie(request):
    resp = HttpResponse("Name cleared.")
    # BUG 6: clearing wrong cookie key; leave stale cookie in browser
    resp.delete_cookie("display_namex")
    return resp

