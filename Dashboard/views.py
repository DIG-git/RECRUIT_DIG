from django.shortcuts import render
from Apply.models import EmployeeApplicants, Job


def dashboard(request):

    current_user = request.user
    job_list = Job.objects.filter(userID=current_user)

    return render(request, 'Dashboard/dashboard.html', {'job_list': job_list})


def applicants(request, job_id):

    applicants_list = EmployeeApplicants.objects.filter(jobID=job_id)
    return render(request, 'Dashboard/applicants_list.html', {'applicants_list': applicants_list})