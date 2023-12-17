from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from .forms import *
from datetime import datetime, timezone

# Create your views here.
def index(request):
    user = request.user
    try:
        courses = Course.objects.all().order_by('course_code')
        assignments = Assignment.objects.all().order_by('-date')
        if user.is_student:
            submissions = Submission.objects.filter(user=user)
            ctx = {
                'courses': courses,
                'assignments': assignments,
                'submissions': submissions
            }
            return render(request, 'lms/student.html', ctx)
        if user.is_lecturer:
            submissions = Submission.objects.all().order_by('-id')
            ctx = {
                'courses': courses,
                'assignments': assignments,
                'submissions': submissions
            }
            return render(request, 'lms/lecturer.html', ctx)
    except AttributeError:
        return render(request, 'lms/index.html')
    return render(request, 'lms/index.html')

@login_required
def courses(request):
    user = request.user
    try:
        if user:
            courses = Course.objects.all().order_by('course_code')
            ctx = {
                'courses': courses
            }
            return render(request, 'lms/courses.html', ctx)
    except AttributeError:
        return render(request, 'lms/index.html')
    return render(request, 'lms/index.html')

@login_required
def assignments(request):
    user = request.user
    try:
        if user:
            assignments = Assignment.objects.all().order_by('-date')
            ctx = {
                'assignments': assignments
            }
            return render(request, 'lms/assignments.html', ctx)
    except AttributeError:
        return render(request, 'lms/index.html')
    return render(request, 'lms/index.html')

@login_required
def assignment(request, id):
    user = request.user
    try:
        if user.is_student:
            assignment = Assignment.objects.get(id=id)
            submitted = assignment.submissions.filter(user=user).exists()
            current_time = datetime.now(timezone.utc)
            
            ctx = {
                'assignment': assignment,
                'submitted': submitted,
                'due': assignment.due_date and current_time > assignment.due_date
            }
            if submitted:
                e = assignment.submissions.get(user=user)
                if e.grade:
                    ctx['grade'] = e.grade

            return render(request, 'lms/assignment.html', ctx)
        elif user.is_lecturer:
            assignment = Assignment.objects.get(id=id)
            ctx = {
                'assignment': assignment,
                'submissions': assignment.submissions.all()
            }
            return render(request, 'lms/assignment.html', ctx)
    except AttributeError:
        return render(request, 'lms/index.html')
    return render(request, 'lms/index.html')

@login_required
def course(request, id):
    user = request.user
    if user:
        course = Course.objects.get(id=id)
        ctx = {
            'course': course,
            'lessons': Lesson.objects.filter(course=id)
        }
        return render(request, 'lms/course.html', ctx)
    return redirect(courses)

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
def addlesson(request, id):
    user = request.user
    if user.is_lecturer:
        if request.POST:
            form_data = LessonForm(request.POST)
            if form_data.is_valid():
                instance = form_data.save(commit=False)
                instance.course = Course.objects.get(id=id)
                instance.save()
                return redirect(course, id=id) 
        ctx = {'form': LessonForm}
        return render(request, 'lms/addlesson.html', ctx)
    return redirect(index)


@login_required
def addassignment(request, id):
    user = request.user
    if user.is_lecturer:
        if request.POST:
            form_data = AssignmentForm(request.POST)
            if form_data.is_valid():
                instance = form_data.save(commit=False)
                instance.course = Course.objects.get(id=id)
                instance.save()
                return redirect(course, id=id) 
        ctx = {'form': AssignmentForm}
        return render(request, 'lms/addassignment.html', ctx)
    return redirect(index)

@login_required
def submit(request, id):
    user = request.user
    assignment = Assignment.objects.get(id=id)
    if user.is_student:
        if request.POST:
            form_data = SubmissionForm(request.POST)
            if form_data.is_valid():
                instance = form_data.save(commit=False)
                instance.assignment = assignment
                instance.user = user
                instance.save()
                return redirect(index) 
        ctx = {'form': SubmissionForm, 'assignment': assignment}
        return render(request, 'lms/submit.html', ctx)
    return redirect(index)

@login_required
def lesson(request, id):
    ctx = {'lesson': Lesson.objects.get(id=id)}
    return render(request, 'lms/lesson.html', ctx)
    
@login_required
def grade(request, id):
    user = request.user
    if user.is_lecturer:
        submission = Submission.objects.get(id=id)
        if request.POST:
            grade = request.POST.get('grade')
            submission.grade = grade
            submission.save()
        ctx = {'submission': submission}
        return render(request, 'lms/grade.html', ctx)
    return redirect(index)



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
