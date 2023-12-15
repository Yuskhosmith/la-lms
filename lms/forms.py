from django import forms
from tinymce.widgets import TinyMCE
from .models import Course, Lesson, Assignment, Submission

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                   "placeholder": "Lesson Title",
                   "class": "biginput",
                }
            ),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ['grade', 'assignment', 'user']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                   "placeholder": "Lesson Title",
                   "class": "biginput",
                }
            ),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'course_title', 'unit', 'type']
        labels = {
            'course_code': "",
            'course_title': "",
            'unit': "",
            'type': ""
        }
        widgets = {
            'course_code': forms.TextInput(attrs={
                   "placeholder": "Course Code",
                   "class": "input",
                }
            ),
            "course_title": forms.TextInput(attrs={
                "placeholder":"Course Title",
                "class": "input",
            }),
            'unit': forms.NumberInput(
                attrs={"placeholder": "Course Unit", 'required': True, "class": "input",}
            ),
            'type': forms.Select(attrs={"class": "input", "required": True,})
        }
