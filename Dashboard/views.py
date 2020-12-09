import os

from django.core.checks import messages
from django.template.defaulttags import register

from django.shortcuts import render, redirect
from Apply.models import EmployeeApplicants, Job, JobRequirements, Similarity
from Home.models import Big5result
from authentication.models import EmployeeInfo

from .training import train

from .forms import JobForm, ApplyForm


def dashboard(request):

    current_user = request.user
    job_list = Job.objects.filter(userID=current_user)

    return render(request, 'Dashboard/dashboard.html', {'job_list': job_list})


def dashboard1(request):
    job_list = []
    job_requirements = []
    current_user = request.user
    info = EmployeeInfo.objects.get(user=current_user)

    try:
        Big5resultlist = Big5result.objects.get(user_id=current_user)
    except Big5result.DoesNotExist:
        Big5resultlist = None

    employee_list = EmployeeApplicants.objects.filter(userID=current_user)
    for employee in employee_list:
        job_list.append(employee.jobID)

    for job in job_list:
        job_requirements.append(JobRequirements.objects.get(job_id=job.id))

    zipped_list = zip(job_requirements,employee_list)
    return render(request, 'Dashboard/dashboard1.html', {'info': info, 'results': Big5resultlist,
                                                         'zipped_list': zipped_list})


def applicants(request, job_id):

    applicants_list = EmployeeApplicants.objects.filter(jobID=job_id)

    resume_list = []

    personality = []

    job = JobRequirements.objects.get(job_id=job_id)
    ranking = Similarity.objects.filter(job_id=job_id)

    job_object = Job.objects.get(id=job_id)

    if not job.active:
        if not ranking:
            for applicant in applicants_list:
                resume_list.append(applicant.resume.url)

            resume_list.append(job.description.url)

            similarity_list = train(resume_list)

            for i in range(len(applicants_list)):
                employeeID = EmployeeApplicants.objects.get(id=applicants_list[i].id)
                similarity = Similarity.objects.create(job_id=job_object, employee_id=employeeID, cosine_similarity=similarity_list[i])
                similarity.save()

    ranking_list = Similarity.objects.filter(job_id=job_id).order_by('-cosine_similarity')

    for employee in ranking_list:
        user_id = employee.employee_id.userID.id
        result = Big5result.objects.get(user_id=user_id)
        personality.append(result)

    zipped_list = zip(ranking_list, personality)

    return render(request, 'Dashboard/applicants_list.html', {'applicants_list': applicants_list, 'zipped_list': zipped_list, 'job': job})


def update_job_form(request, job_id):
    job_detail = JobRequirements.objects.get(job_id=job_id)
    return render(request, 'Dashboard/update_job_form.html', {'job_detail': job_detail})


def update_job(request, job_id):
    job = JobRequirements.objects.get(job_id=job_id)
    form = JobForm(data=request.POST, files=request.FILES, instance=job)

    if form.is_valid():
        form.save()
        return redirect('/Dashboard/')


def delete_job(request, job_id):
    job = Job.objects.get(id=job_id)
    job.delete()
    return redirect('/Dashboard/')


def update_apply_form(request, applicant_id):
    apply_detail = EmployeeApplicants.objects.get(id=applicant_id)
    return render(request, 'Dashboard/update_apply_form.html', {'apply_detail': apply_detail})


def update_employee(request, employee_id):
    employee = EmployeeApplicants.objects.get(id=employee_id)
    form = ApplyForm(data=request.POST, files=request.FILES, instance=employee)

    if form.is_valid():
        form.save()
        return redirect('/Dashboard/Employee')


def delete_employee(request, applicant_id):
    employee = EmployeeApplicants.objects.get(id=applicant_id)
    employee.delete()
    return redirect('/Dashboard/Employee')

