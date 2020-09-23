from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from .models import EmployeeApplicants, JobRequirements, Job


def apply(request, job_id):
    job_info = Job.objects.get(id=job_id)
    return render(request, 'Forms/apply.html', {'job_info': job_info})


def add_apply(request, job_id):
    fname = request.POST['fname']
    mname = request.POST['mname']
    lname = request.POST['lname']
    contact = request.POST['contact']
    address = request.POST['address']
    email = request.POST['email']
    gender = request.POST['gender']
    dob = request.POST['dob']
    resume = request.FILES['resume']

    current_user = request.user

    job = Job.objects.get(id=job_id)

    employee_applicants = EmployeeApplicants.objects.create(userID=current_user, jobID=job, fname=fname, mname=mname, lname=lname,
                                                            contact=contact, address=address, email=email,
                                                            gender=gender, dob=dob,
                                                            resume=resume)
    employee_applicants.save()

    apply_info = EmployeeApplicants.objects.all()

    return render(request, 'Forms/info_view.html', {'apply': apply_info})


def add_jobs(request):
    return render(request, 'Forms/require.html')


def post_jobs(request):
    comp_name = request.POST['comp_name']
    post = request.POST['post']
    salary = request.POST['salary']
    address = request.POST['address']
    openings = request.POST['openings']
    experience = request.POST['experience']
    hours = request.POST['hours']
    gender = request.POST['gender']
    job_category = request.POST['job_category']
    fromdate = request.POST['fromdate']
    todate = request.POST['todate']
    description = request.FILES['description']

    current_user = request.user

    job = Job.objects.create(userID=current_user, comp_name=comp_name, job_category=job_category)
    job.save()

    job_requirements = JobRequirements.objects.create(job_id=job, post=post, salary=salary, address=address,
                                                      openings=openings,
                                                      experience=experience, hours=hours, gender=gender,
                                                      fromdate=fromdate, todate=todate, description=description)
    job_requirements.save()

    return render(request, 'Home/job_detail.html', {'job_requirements': job_requirements})
