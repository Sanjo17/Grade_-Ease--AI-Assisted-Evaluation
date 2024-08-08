from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL
from exam.utils.grading import Grading
from .models import Student
from papergrading.utils.preprocessing import preprocess
from papergrading.utils.keyword import *
from papergrading.utils.mark_rubics import *
from papergrading.utils.bert import check_similarity
from huggingface_hub import from_pretrained_keras



#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    student = Student.objects.get(user=request.user)
    
    dict={
    'student':student,
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.QuestionAnswer.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_exam.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.QuestionAnswer.objects.all().filter(course=course).count()
    questions=QMODEL.QuestionAnswer.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.QuestionAnswer.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    # time = course.duration
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    model =  from_pretrained_keras("keras-io/bert-semantic-similarity")
    labels = ["Contradiction", "Perfect", "Neutral"]
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.QuestionAnswer.objects.all().filter(course=course)
        
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].correct_answer 

            #keyword
            key_keywords = extract_keywords(questions[i].correct_answer,top_n=10)
            print("\n key_kewords : ",key_keywords)
            try:
                studans_keywords = extract_keywords(selected_ans,top_n=10)
            except Exception as e:
                studans_keywords = ['nul']
                
            print("\n ans_kewords : ",studans_keywords)
            keyword_score = calculate_keyword_similarity(student_keywords=studans_keywords,key_keywords=key_keywords)
            print("keyword_Score",keyword_score)
            # keyword_score = calculate_keyword_similarity(student_keywords=studans_keywords,key_keywords=key_keywords)


            #preprocessing
            student_ans_pre = preprocess(selected_ans)
            key_ans_pre = preprocess(actual_answer)

            #count
            k_wordcount_score = Grading.count_words(questions[i].correct_answer)
            stdans_wordcount_score = Grading.count_words(selected_ans)
            print("key count" , k_wordcount_score)
            print("std count" , stdans_wordcount_score)

            data = {
            "inputs": {
            "source_sentence": key_ans_pre,
            "sentences":[student_ans_pre]
            }
            }
            print("actual "+actual_answer)
            print(selected_ans)
            # if selected_ans == actual_answer:
            #     total_marks = total_marks + questions[i].marks
            bert_score = check_similarity(sentence1=key_ans_pre,sentence2=student_ans_pre,model=model,labels=labels)
            perfect = bert_score['Perfect']
            neutral = bert_score['Neutral']
            contradiction = bert_score['Contradiction']
            print("contraidction",contradiction)
            if selected_ans == None:
                mark = [0]
            else:
                try:
                    markr = Grading.marking(data)
                except Exception as e:
                    print("error")
                    mark = [perfect]
            
            if contradiction>mark[0]:
                student_mark = (contradiction-1)*10
            else:
                student_mark = mark[0]
            
            print(mark[0])
            # student_mark = mark[0]
            # student_mark = 
            if student_mark< 0.2 :
                student_mark = 0
            question_mark = questions[i].marks
            t_marks = calculate_total_marks(semantic_similarity=mark[0]*10,keyword_similarity=keyword_score/10,total_marks=question_mark,word_count_key=k_wordcount_score,word_count_student=stdans_wordcount_score)
            print("real mark" ,t_marks)
            # total_marks = total_marks+ student_mark*question_mark
            total_marks = total_marks+ t_marks

        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()

        return HttpResponseRedirect('view-result')



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    question_mark=QMODEL.QuestionAnswer.objects.all().filter(course=course)
    total_marks=0
    for q in question_mark:
        total_marks=total_marks + q.marks
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results,'total_marks':total_marks})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})
  