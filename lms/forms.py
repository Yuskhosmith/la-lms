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
                }
            ),
            "course_title": forms.TextInput(attrs={
                "placeholder":"Course Title",
            }),
            'unit': forms.NumberInput(
                attrs={"placeholder": "Course Unit", 'required': True}
            ),
            'type': forms.Select()
        }
