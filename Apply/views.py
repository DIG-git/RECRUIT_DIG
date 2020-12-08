from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .models import EmployeeApplicants, JobRequirements, Job
from Home.models import Big5result


def apply(request, job_id):
    job_info = Job.objects.get(id=job_id)

    questions_key = get_ques()

    current_user = request.user
    try:
        Big5resultlist = Big5result.objects.get(user_id=current_user)
    except Big5result.DoesNotExist:
        Big5resultlist = None

    if not Big5resultlist:
        return render(request, 'PersonalityTest/Big5Form.html', {"questions": questions_key, "error": "Take personality test before applying!!"})
    else:
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

    return redirect('/Dashboard/Employee')


def add_jobs(request):
    return render(request, 'Forms/job_form.html')


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


def get_ques():
    questions_key = [
        'I am the life of the party.',
        "I don't talk a lot.",
        'I feel comfortable around people.',
        'I keep in the background.',
        'I start conversations.',
        'I have little to say.',
        'I talk to a lot of different people at parties.',
        "I don't like to draw attention to myself.",
        "I don't mind being the center of attention.",
        'I am quiet around strangers.',
        'I get stressed out easily.',
        'I am relaxed most of the time.',
        'I worry about things.',
        'I seldom feel blue.',
        'I am easily disturbed.',
        'I get upset easily.',
        'I change my mood a lot.',
        'I have frequent mood swings.',
        'I get irritated easily.',
        'I often feel blue.',
        'I feel little concern for others.',
        'I am interested in people.',
        'I insult people.',
        "I sympathize with others' feelings.",
        "I am not interested in other people's problems.",
        'I have a soft heart.',
        'I am not really interested in others.',
        'I take time out for others.',
        "I feel others' emotions.",
        'I make people feel at ease.',
        'I am always prepared.',
        'I leave my belongings around.',
        'I pay attention to details.',
        'I make a mess of things.',
        'I get chores done right away.',
        'I often forget to put things back in their proper place.',
        'I like order.',
        'I shirk my duties.',
        'I follow a schedule.',
        'I am exacting in my work.',
        'I have a rich vocabulary.',
        'I have difficulty understanding abstract ideas.',
        'I have a vivid imagination.',
        'I am not interested in abstract ideas.',
        'I have excellent ideas.',
        'I do not have a good imagination.',
        'I am quick to understand things.',
        'I use difficult words.',
        'I spend time reflecting on things.',
        'I am full of ideas.'
    ]

    return questions_key