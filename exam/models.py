from django.db import models
import datetime 
from student.models import Student

# course table
class Course(models.Model):
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   duration = models.DurationField(default=datetime.timedelta(minutes=60))

   def __str__(self):
        return self.course_name

# class Question(models.Model):
#     course=models.ForeignKey(Course,on_delete=models.CASCADE)
#     marks=models.PositiveIntegerField()
#     question=models.CharField(max_length=600)
#     option1=models.CharField(max_length=200)
#     option2=models.CharField(max_length=200)
#     option3=models.CharField(max_length=200)
#     option4=models.CharField(max_length=200)
#     cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
#     answer=models.CharField(max_length=200,choices=cat)


# queston table
class QuestionAnswer(models.Model):
    course=models.ForeignKey(Course, on_delete = models.CASCADE)
    marks = models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    correct_answer=models.CharField(max_length=200)

    def __str__(self):
        return self.text

# result table
class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

# student answer table
class StudentResponse(models.Model):
    course=models.ForeignKey(Course, on_delete = models.CASCADE)
    question = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)
    student_answer = models.TextField(default=" ")

    def __str__(self):
        return f"{self.course.name} - {self.question.text}"


