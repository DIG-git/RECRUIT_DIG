import os

from django.shortcuts import render
from Apply.models import EmployeeApplicants, Job, JobRequirements, Similarity

from .training import train


def dashboard(request):

    current_user = request.user
    job_list = Job.objects.filter(userID=current_user)

    return render(request, 'Dashboard/dashboard.html', {'job_list': job_list})


def applicants(request, job_id):

    applicants_list = EmployeeApplicants.objects.filter(jobID=job_id)

    resume_list = []

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
                similarity = Similarity.objects.create(job_id=job_object, employee_id=EmployeeApplicants.objects.get(id=applicants_list[i].id), cosine_similarity=similarity_list[i])
                similarity.save()

    ranking_list = Similarity.objects.filter(job_id=job_id).order_by('-cosine_similarity')

    return render(request, 'Dashboard/applicants_list.html', {'applicants_list': applicants_list, 'resume_list': ranking_list})


