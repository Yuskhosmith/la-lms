from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from .forms import *

# Create your views here.
def index(request):
    user = request.user
    try:
        if user.is_student:
            return render(request, 'lms/student.html')
        if user.is_lecturer:
            courses = Course.objects.all().order_by('course_code')
            ctx = {
                'courses': courses
            }
            return render(request, 'lms/lecturer.html', ctx)
    except AttributeError:
        return render(request, 'lms/index.html')
    return render(request, 'lms/index.html')

@login_required
def courses(request):
    user = request.user
    try:
        if user.is_student:
            return render(request, 'lms/courses.html')
        if user.is_lecturer:
            courses = Course.objects.all().order_by('course_code')
            ctx = {
                'courses': courses
            }
            return render(request, 'lms/courses.html', ctx)
    except AttributeError:
        return render(request, 'lms/index.html')
    return render(request, 'lms/index.html')

@login_required
def addcourse(request):
    user = request.user
    if user.is_lecturer:
        if request.POST:
            form_data = CourseForm(request.POST)
            if form_data.is_valid():
                x = form_data.save()
                return redirect(course, id=x.id) 
        ctx = {'form': CourseForm}
        return render(request, 'lms/addcourse.html', ctx)
    return redirect(index)

@login_required
def course(request, id):
    user = request.user
    if user.is_lecturer:
        ctx = {
            'course': Course.objects.get(id=id)
        }
        return render(request, 'lms/course.html', ctx)
    return redirect(courses)


def login_view(request):   

    if request.method == "POST":
        next = request.POST['next']
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            
            if next == "":
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(next)
        else:
            return render(request, "lms/login.html", {
                "message": "Invalid username and/or password."
            })

    return render(request, "lms/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        user_type = request.POST["type"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "lms/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            if user_type == 'student':
                user.is_student = True
            elif user_type == 'lecturer':
                user.is_lecturer = True
            user.save()
        except IntegrityError:
            return render(request, "lms/register.html", {
                "message": "ID/Email already registered."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "lms/register.html")
