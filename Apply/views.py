from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from .models import EmployeeApplicants, JobRequirements, Job, Aptitude
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

    ques = Aptitude.objects.filter(job_id=job_id)

    if ques.exists():
        return render(request, 'Forms/aptitude_answerSheet.html', {'questions': ques, 'job_id': job_id})
    else:
        jobs = JobRequirements.objects.order_by('-fromdate')[:9]
        return render(request, 'Home/index.html', {'jobs': jobs})


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

    return render(request, 'Forms/aptitude_form.html', {'job_id':job.id})


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


def aptitude_form(request, job_id):
    question = request.POST['ques']
    opta = request.POST['opta']
    optb = request.POST['optb']
    optc = request.POST['optc']
    optd = request.POST['optd']
    ans = request.POST['answer']

    if ans == 'Option A':
        answer = opta
    elif ans == 'Option B':
        answer = optb
    elif ans == 'Option C':
        answer = optc
    else:
        answer = optd

    aptitude = Aptitude.objects.create(job_id=job_id, question=question, opta=opta, optb=optb, optc=optc,
                                       optd=optd, answer=answer)

    aptitude.save()

    return render(request, 'Forms/aptitude_form.html', {'job_id':job_id})


def aptitude_result(request, job_id):
    current_user = request.user

    score = 0
    questions = Aptitude.objects.values_list('question', flat=True).filter(job_id=job_id)
    for ques in questions:
        chk = request.POST[ques]
        answers = Aptitude.objects.values_list('answer', flat=True).filter(question=ques)
        if chk == answers[0]:
            score = score + 1

    employee = EmployeeApplicants.objects.filter(userID=current_user, jobID=job_id).order_by('-id').first()
    employee.aptitude_score = score
    employee.save()

    jobs = JobRequirements.objects.order_by('-fromdate')[:9]
    return render(request, 'Home/index.html', {'jobs': jobs})

