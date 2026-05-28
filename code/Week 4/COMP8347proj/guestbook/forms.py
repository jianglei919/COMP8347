from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        # BUG 1: display_name missing, so it never renders/saves
        fields = ["message"]   # should also include "display_name"

    # BUG 2: weak validation: allow empty message accidentally
    def clean_message(self):
        msg = self.cleaned_data.get("message", "")
        # broken: returns message even if empty/whitespace
        return msg
