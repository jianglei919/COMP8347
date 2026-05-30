from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        # FIX 1: include display_name so it renders and saves
        fields = ["display_name", "message"]
        # No HTML maxlength: let users type past the limit so server-side
        # validation can reject overly long input with a clear error message.
        widgets = {
            "display_name": forms.TextInput(attrs={"placeholder": "Your name (max 40 chars)"}),
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Your message (max 280 chars)"}),
        }

    # FIX 2: reject empty/whitespace-only messages and enforce length limit
    def clean_message(self):
        msg = self.cleaned_data.get("message", "").strip()
        if not msg:
            raise forms.ValidationError("Message cannot be empty.")
        if len(msg) > 280:
            raise forms.ValidationError("Message is too long (max 280 characters).")
        return msg

    def clean_display_name(self):
        name = self.cleaned_data.get("display_name", "").strip()
        if len(name) > 40:
            raise forms.ValidationError("Name is too long (max 40 characters).")
        return name
