from django.db import models
from exam.models import Course
from student.models import Student

# answer key
class AnswerKey(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    key_file = models.FileField(upload_to='answer_keys/',null=True,blank=True)

# student annswer paper 
class StudentPaper(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    answer_file = models.FileField(upload_to='student_answers/',null=True,blank=True)

# marks
class MarkSheet(models.Model):
    question = models.CharField(max_length=100)
    maximum_marks = models.IntegerField()
    obtained_marks = models.FloatField()
    
    def __str__(self):
        return f"{self.question}: {self.obtained_marks}/{self.maximum_marks}"






