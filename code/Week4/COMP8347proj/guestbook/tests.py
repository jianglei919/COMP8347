from django.test import TestCase
from .models import Entry


class GuestbookTests(TestCase):
    def test_add_increments_counter_and_sets_cookie(self):
        r = self.client.post("/guestbook/add/", {"display_name": "Alice", "message": "Hello world"})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(self.client.session.get("gb_added"), 1)
        self.assertEqual(self.client.cookies.get("displayname").value, "Alice")
        self.client.post("/guestbook/add/", {"display_name": "Alice", "message": "Second"})
        self.assertEqual(self.client.session.get("gb_added"), 2)

    def test_list_shows_author_and_message_newest_first(self):
        self.client.post("/guestbook/add/", {"display_name": "Alice", "message": "First msg"})
        self.client.post("/guestbook/add/", {"display_name": "Bob", "message": "Second msg"})
        r = self.client.get("/guestbook/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Alice")
        self.assertContains(r, "First msg")
        names = list(Entry.objects.order_by("-created_at").values_list("display_name", flat=True))
        self.assertEqual(names, ["Bob", "Alice"])

    def test_cookie_prefills_name_on_add_form(self):
        self.client.cookies["displayname"] = "Alice"
        r = self.client.get("/guestbook/add/")
        self.assertContains(r, 'value="Alice"')

    def test_empty_message_rejected(self):
        r = self.client.post("/guestbook/add/", {"display_name": "Bob", "message": "   "})
        self.assertEqual(r.status_code, 200)  # re-renders form, no redirect
        self.assertContains(r, "error")       # an error message is shown
        self.assertEqual(Entry.objects.count(), 0)

    def test_overly_long_message_rejected(self):
        r = self.client.post("/guestbook/add/", {"display_name": "Bob", "message": "x" * 281})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Entry.objects.count(), 0)
