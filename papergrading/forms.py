from django import forms
from django.contrib.auth.models import User
from . import models

# answer key form
class KeyUploadForm(forms.ModelForm):

    class Meta:
        model = models.AnswerKey
        fields = ['course','key_file']
        
# student answer file upload
class StudentAnswerFileUploadForm(forms.ModelForm):

    class Meta:
        model = models.StudentPaper
        fields = ['course','answer_file','student']

# marks
class MarksheetForm(forms.ModelForm):

    class Meta:
        model = models.MarkSheet
        fields = ['question','maximum_marks','obtained_marks']
        

