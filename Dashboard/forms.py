from django import forms
from Apply.models import JobRequirements


class JobForm(forms.ModelForm):
    class Meta:
        model = JobRequirements
        exclude = ['job_id']