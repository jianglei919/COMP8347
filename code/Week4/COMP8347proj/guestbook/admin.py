from django.contrib import admin
from .models import Entry

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("display_name", "short_message", "created_at")
    search_fields = ("display_name", "message")
    ordering = ("-created_at",)

    def short_message(self, obj):
        return (obj.message[:40] + "…") if len(obj.message) > 40 else obj.message

