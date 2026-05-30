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
            entry = form.save()
            # FIX 3: increment the per-session counter on a successful post
            request.session["gb_added"] = request.session.get("gb_added", 0) + 1
            # Remember the name in a cookie so future forms can prefill it
            resp = redirect("gb-list")
            if entry.display_name:
                resp.set_cookie("displayname", entry.display_name, max_age=7 * 24 * 3600)
            return resp
    else:
        # FIX 4: prefill display_name from cookie (form now includes the field)
        initial = {"display_name": request.COOKIES.get("displayname", "")}
        form = EntryForm(initial=initial)

    return render(request, "guestbook/add_entry.html", {"form": form})

def set_name_cookie(request):
    # Sets a cookie so future forms can prefill display_name
    name = request.GET.get("name", "").strip()
    resp = HttpResponse("Name saved. You can go back.")
    # FIX 5: use the same cookie key ("displayname") that is read elsewhere
    resp.set_cookie("displayname", name, max_age=7 * 24 * 3600)
    return resp

def clear_name_cookie(request):
    resp = HttpResponse("Name cleared.")
    # FIX 6: delete the correct cookie key
    resp.delete_cookie("displayname")
    return resp

