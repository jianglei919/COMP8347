from django.db import models

class Entry(models.Model):
    display_name = models.CharField(max_length=40, blank=True, default="")
    message = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # show first 24 chars for admin list
        who = self.display_name or "Anonymous"
        return f"{who}: {self.message[:24]}..."

