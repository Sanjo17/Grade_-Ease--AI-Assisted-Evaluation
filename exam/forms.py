from django import forms
from django.contrib.auth.models import User
from . import models

# contact form
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

# teacher salary form
class TeacherSalaryForm(forms.Form):
    salary=forms.IntegerField()

# course form
class CourseForm(forms.ModelForm):
    class Meta:
        model=models.Course
        fields=['course_name','question_number','total_marks','duration']

# class QuestionForm(forms.ModelForm):
    
#     #this will show dropdown __str__ method course model is shown on html so override it
#     #to_field_name this will fetch corresponding value  user_id present in course model and return it
#     courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
#     class Meta:
#         model=models.Question
#         fields=['marks','question','option1','option2','option3','option4','answer']
#         widgets = {
#             'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
#         }

# question answer form for adding question to course
class QuestionanswerForm(forms.ModelForm):
    courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model = models.QuestionAnswer
        fields = ['marks','question','correct_answer',]
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }
        
# studentresponse form of the student answer from test
class StudentResponseForm(forms.ModelForm):
    courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model = models.StudentResponse()
        fields = ['course','question','student_answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }