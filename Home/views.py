from django.shortcuts import render


def index(request):
    return render(request, 'Home/index.html')


def jobs(request):
    return render(request, 'Jobs/jobs.html')


def category(request):
    return render(request, 'JobCategory/category.html')


def dashboard(request):
    return render(request, 'Dashboard/dashboard.html')
