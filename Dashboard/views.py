import os

from django.shortcuts import render
from Apply.models import EmployeeApplicants, Job, JobRequirements

from .training import train


def dashboard(request):

    current_user = request.user
    job_list = Job.objects.filter(userID=current_user)

    return render(request, 'Dashboard/dashboard.html', {'job_list': job_list})


def applicants(request, job_id):

    applicants_list = EmployeeApplicants.objects.filter(jobID=job_id)

    resume_list = []

    similarity_list = []

    job = JobRequirements.objects.get(job_id=job_id)

    for applicant in applicants_list:
        resume_list.append(applicant.resume.url)

    resume_list.append(job.description.url)

    similarity_list = train(resume_list)

    return render(request, 'Dashboard/applicants_list.html', {'applicants_list': applicants_list, 'resume_list': similarity_list})


