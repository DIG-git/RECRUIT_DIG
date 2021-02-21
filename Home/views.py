from django.shortcuts import render, get_object_or_404

from Apply.models import JobRequirements, Job, EmployeeApplicants
from Home.Big5 import Big5
from .models import Big5result, Category


def index(request):
    categories = Category.objects.first()
    print(categories)
    jobs = JobRequirements.objects.order_by('-fromdate')[:15]
    return render(request, 'Home/index.html', {'jobs': jobs, 'categories': categories})


def jobs(request):
    categories = Category.objects.first()
    return render(request, 'Jobs/jobs.html', {'categories': categories})


def job_category(request, id=None):
    category = None
    count = 0
    job_requirements = []
    categories = Category.objects.all()
    if id:
        category = Category.objects.get(slug=id)
        print(category.slug)
        jobs = Job.objects.filter(job_category=category.slug)
        print(jobs)
        for job in jobs:
            print(JobRequirements.objects.get(job_id=job))
            job_requirements.append(JobRequirements.objects.get(job_id=job))
        print(job_requirements)
        for job in job_requirements:
            if job.active:
                count = count + 1
    return render(request, 'JobCategory/category.html', {'categories': categories, 'jobs': job_requirements, 'category': category.name, 'active': count})


def category(request):
    categories = Category.objects.all()
    jobs = JobRequirements.objects.all()
    print(categories)
    return render(request, 'JobCategory/category1.html', {'jobs': jobs, 'categories': categories})


def personality_test(request):
    current_user = request.user
    if current_user.is_authenticated:

        try:
            Big5resultlist = Big5result.objects.get(user_id=current_user)
        except Big5result.DoesNotExist:
            Big5resultlist = None

        questions_key = get_ques()

        if not Big5resultlist:
            return render(request, 'PersonalityTest/Big5Form.html', {"questions": questions_key})
        else:
            return render(request, 'PersonalityTest/Big5Results.html', {'results': Big5resultlist})

    else:
        return render(request, 'authentication/login.html', {'error': 'Login to take personality test!!'})


def personality_score(request):
    answers = {}

    current_user = request.user

    try:
        Big5resultlist = Big5result.objects.get(user_id=current_user)
    except Big5result.DoesNotExist:
        Big5resultlist = None

    for ques in get_ques():
        chk = request.POST[ques]
        answers[ques] = int(chk)

    print(answers)

    if not Big5resultlist:
        big5 = Big5()
        results = big5.handle_personality_test(answers)
        print(results)

        for key, score in results.items():
            if 'O_score' in key:
                openness = score
            if 'C_score' in key:
                conscientiousness = score
            if 'E_score' in key:
                extraversion = score
            if 'A_score' in key:
                agreeableness = score
            if 'N_score' in key:
                neuroticism = score

        big5_result = Big5result.objects.create(user_id=current_user, openness=openness,
                                                conscientiousness=conscientiousness, extraversion=extraversion,
                                                agreeableness=agreeableness, neuroticism=neuroticism)
        big5_result.save()

    test_results = Big5result.objects.get(user_id=current_user)

    return render(request, 'PersonalityTest/Big5Results.html', {'results': test_results})


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


def job_detail(request, pk):
    job_requirements = JobRequirements.objects.get(job_id=pk)
    current_user = request.user
    apply = EmployeeApplicants.objects.filter(userID=current_user, jobID=pk)
    return render(request, 'Home/job_detail.html', {'job_requirements': job_requirements, 'applied': apply})


def search(request):
    searched_job = []
    search = request.POST['search']
    job_list = JobRequirements.objects.filter(post__icontains=search)
    for job in job_list:
        if job.active:
            searched_job.append(job)
    return render(request, 'Home/search_result.html', {'jobs': searched_job, 'search': search})


def about(request):
    return render(request, 'Home/about.html')