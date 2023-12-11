from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_lecturer = models.BooleanField('lecturer_status', default=False)
    is_student = models.BooleanField('student_status', default=False)

class Course(models.Model):
    COURSE_TYPE_CHOICE = (
        ('Compulsory', 'Compulsory'),
        ('Required', 'Required'),
        ('Elective', 'Elective')
    )
    course_code = models.CharField(max_length=8, null=True)
    course_title = models.CharField(max_length=1000, null=True)
    unit = models.IntegerField(null=True)
    type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICE, null=True)

# class Lesson(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
#     title = models.CharField(max_length=1000, null=True)
#     content = models.TextField(null=True)
#     rich text for content, allow video content
#     date = models.DateTimeField(default=datetime.now, null=True)