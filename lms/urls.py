from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses', views.courses, name='courses'),
    path('assignment/<int:id>', views.assignment, name='assignment'),
    path('assignments', views.assignments, name='assignments'),
    path('addcourse', views.addcourse, name='addcourse'),
    path('course/<int:id>', views.course, name='course'),
    path('lesson/<int:id>', views.lesson, name='lesson'),
    path('addlesson/<int:id>', views.addlesson, name='addlesson'),
    path('addassignment/<int:id>', views.addassignment, name='addassignment'),
    path('submit/<int:id>', views.submit, name='submit'),



    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
