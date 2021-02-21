from django import forms
from Apply.models import JobRequirements, EmployeeApplicants


class JobForm(forms.ModelForm):
    class Meta:
        model = JobRequirements
        exclude = ['job_id']


class ApplyForm(forms.ModelForm):
    class Meta:
        model = EmployeeApplicants
        exclude = ['userID', 'jobID', 'aptitude_score']

