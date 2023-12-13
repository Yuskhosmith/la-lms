from django import forms
from .models import Course




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
