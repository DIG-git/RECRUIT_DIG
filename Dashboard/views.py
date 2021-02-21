import os

from django.core.checks import messages
from django.template.defaulttags import register

from django.shortcuts import render, redirect
from Apply.models import EmployeeApplicants, Job, JobRequirements, Similarity, Aptitude, Compatible
from Home.models import Big5result
from authentication.models import EmployeeInfo, CompanyInfo

from .training import train, train_desc
from .forms import JobForm, ApplyForm
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse


def dashboard(request):
    current_user = request.user
    job_list = Job.objects.filter(userID=current_user)
    info = CompanyInfo.objects.get(user=current_user)

    return render(request, 'Dashboard/dashboard.html', {'job_list': job_list, 'info': info})


def dashboard1(request):
    job_list = []
    job_requirements = []
    final = []
    compatible = []
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

    zipped_list = zip(job_requirements, employee_list)

    if Compatible.objects.filter(userID=current_user.id):
        compatible_list = Compatible.objects.get(userID=current_user.id)

        final.append(compatible_list.desc1)
        final.append(compatible_list.desc2)
        final.append(compatible_list.desc3)

        for f in final:
            compatible.append(JobRequirements.objects.get(job_id=f))

    return render(request, 'Dashboard/dashboard1.html', {'info': info, 'results': Big5resultlist,
                                                         'zipped_list': zipped_list, 'compatible': compatible})


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
                similarity = Similarity.objects.create(job_id=job_object, employee_id=employeeID,
                                                       cosine_similarity=similarity_list[i])
                similarity.save()

    ranking_list = Similarity.objects.filter(job_id=job_id).order_by('-cosine_similarity')

    for employee in ranking_list:
        print(employee.cosine_similarity)
        user_id = employee.employee_id.userID.id
        result = Big5result.objects.get(user_id=user_id)
        personality.append(result)

    zipped_list = zip(ranking_list, personality)

    return render(request, 'Dashboard/applicants_list.html', {'applicants_list': applicants_list,
                                                              'zipped_list': zipped_list, 'job': job})


def description_list(request):
    current_user = request.user
    emp = EmployeeApplicants.objects.filter(userID=current_user).first()
    jobs = JobRequirements.objects.all()
    ranking = Compatible.objects.filter(userID=current_user.id)
    job_list = []
    desc_list = []
    final = []

    for job in jobs:
        if job.active:
            desc_list.append(job.description.url)
            job_list.append(job.job_id.id)

    desc_list.append(emp.resume.url)

    similarity_list = train_desc(desc_list)

    for i in range(len(job_list)):
        info = {
            "similarity": similarity_list[i],
            "jobID": job_list[i]
        }
        final.append(info)

    final = sorted(final, key=lambda i: i['similarity'], reverse=True)

    if not ranking:
        compatibility = Compatible.objects.create(userID=current_user.id, desc1=final[0]['jobID'],
                                                  desc2=final[1]['jobID'],
                                                  desc3=final[2]['jobID'])
        compatibility.save()
    else:
        Compatible.objects.filter(userID=current_user.id).update(desc1=final[0]['jobID'], desc2=final[1]['jobID'],
                                                  desc3=final[2]['jobID'])

    # compatible_list = Compatible.objects.get(userID=current_user.id)

    return HttpResponseRedirect('Employee')


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
    aptitude = Aptitude.objects.filter(job_id=job_id)
    job.delete()
    aptitude.delete()
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
