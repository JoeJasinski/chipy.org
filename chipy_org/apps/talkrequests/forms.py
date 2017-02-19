from django import forms
from . import models


class TalkRequestSubmissionForm(forms.ModelForm):
    class Meta:
        model = models.TalkRequest
        fields = ['title', 'text', 'category', ]
