from django.shortcuts import render
from Apply.models import Job, JobRequirements


def index(request):
    jobs = JobRequirements.objects.all()
    return render(request, 'Home/index.html', {'jobs': jobs})


def jobs(request):
    return render(request, 'Jobs/jobs.html')


def category(request):
    return render(request, 'JobCategory/category.html')


def dashboard(request):
    return render(request, 'Dashboard/dashboard.html')


def job_detail(request, pk):
    job_requirements = JobRequirements.objects.get(job_id=pk)
    return render(request, 'Home/job_detail.html', {'job_requirements': job_requirements})