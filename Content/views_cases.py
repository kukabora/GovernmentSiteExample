from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from .models import Citizen, Project, ProjectPhoto

def log_off(request):
    """Simple logging-in method."""
    logout(request)
    return redirect("start")

def auth(request, context):
    """Authentication method, which consists of login and authenticate methods."""
    email=request.POST['email']
    password=request.POST['password']
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        return redirect("main")
    else:
        context['errors'] = "Invalid login or password!"
        return render(request, 'Content/login.html', context)


def login_check(request):
    """Method that checks whether user is logged in or not. Returns also a Citizen object if user is logged in."""
    context = {
        'user':None,
        'cit':None
    }
    if request.user.is_authenticated:
        context = {
            'user':request.user,
            'cit':Citizen.objects.get(id=request.user.id)
        }
    return context

def handle_uploaded_file(file, request):
    """Function that handles uploaded file and writes it chunk by chunk in 'media/avatars/..."""
    with open(f'media/avatars/{request.user.email}.jpg', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def handle_image(request, context):
    """Function that takes  image out of request.FILES and cuts off it's prefix and common name."""
    postfix = request.FILES['avatar'].name[request.FILES['avatar'].name.rfind("."):]
    request.FILES['avatar'].name = request.user.email+postfix
    handle_uploaded_file(request.FILES['avatar'], request)
    context['cit'].avatar = request.FILES['avatar']
    context['cit'].save()

def user_creating(request, context):
    """Registration method, which considers user's job and status, and saves models."""
    deps = {
            '01':'Presidential branch',
            '02':'Healthcare Sphere',
            '03':'Educational Sphere',
            '04':'Military Sphere',
            '05':'Official'
        }
    ranks = {
            '01':'Ordinary worker',
            '02':'Manager',
            '03':'Secretary',
            '04':'Cleaner',
            '05':'Overseer',
            '06':'Main'
        }
    date_source = request.POST['birth_day']
    date = date_source[-4:] + "-" + date_source[-7:-5] + "-" + date_source[-10:-8]
    User.objects.create_user(
        username = request.POST['email'],
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = request.POST['password'],
    )
    new = Citizen(
        user = User.objects.get(username = request.POST['email']),
        department = deps.get(request.POST['res_code'][:2], "Other"),
        rank = ranks.get(request.POST['res_code'][2:4], "Citizen"),
        birth_day = date,
        gender = request.POST['gender'],
    )
    new.save()
    return redirect("login")

def project_creating(request):
    """
    New project creationg functions. Creates project model,
    updates Citizen model, saves uploaded files to media.
    """
    citizen_id = request.user.id
    citizen = Citizen.objects.get(id=citizen_id)
    project = Project(
        title = request.POST['title'],
        description = request.POST['desc'],
        votes = 0,
        creator = citizen,
        sphere = request.POST['sphere']
    )
    sphere_dict = {
        'ed':citizen.ed_proj,
        'health':citizen.health_proj,
        'military':citizen.military_proj,
        'social':citizen.social_proj,
        'cult':citizen.cult_proj
    }
    sphere_dict[request.POST['sphere']] += 1
    citizen.save()
    project.save()
    for file in request.FILES['images']:
        pass
    