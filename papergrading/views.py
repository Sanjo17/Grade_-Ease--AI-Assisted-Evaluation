from django.shortcuts import render,redirect,reverse
from . import models, forms
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam.utils.grading import Grading
from exam.utils.handwritten import GeminiHandler
import os
from student.models import Student
from exam.models import Course
from .utils.text_file_extraction import TextExtractor, extract_answers_key
from exam.utils.grading import Grading
from .utils.preprocessing import preprocess 
from .utils.text_structure import TextStruct,answer_struct_fn
from .models import StudentPaper as Qpaper
from .models import MarkSheet
from django.core.serializers import serialize
import json
from .utils.pdf_to_image import pdf_to_img
from .utils.keyword import *
from .utils.mark_rubics import *
from .utils.bert import check_similarity
from .utils.reportcard import *
from huggingface_hub import from_pretrained_keras

# answer key page
def papergradingclick_view(request):
    answer_key = forms.KeyUploadForm()
    if request.method=='POST':
        answer_key=forms.KeyUploadForm(request.POST,request.FILES)  
        if answer_key.is_valid():        
            answer_key.save()
            answer_key_file = request.FILES['key_file']           
            course_id = int(request.POST['course'])
            course_name = Course.objects.get(pk=course_id)
            filepath = f'{settings.MEDIA_ROOT}/answer_keys/{answer_key_file}'
            txt_ex = extract_answers_key(file_path=filepath) #extracting the txt from answer key
            # txt_ex = TextExtractor(filepath)
            # key_ques,key_ans = txt_ex.extract()
            # request.session['key_ans'] = key_ans
            key_answers_only=[]
            answers_list = list(txt_ex.values())
            print("answer list == ",answers_list)
            # key_ques = request.session.get('key_ques')
            for i in range(0,len(answers_list)):
                answer_k, marks_k = answers_list[i]
                print("\n answer_k : ",answer_k)
                print("\n marks_k: ",marks_k)
                key_ans_pre = preprocess(answer_k) #proproces
                print('\n key_ans_pre : ',key_ans_pre)
        
                key_answers_only.append(key_ans_pre)     
            # request.session.pop('key_ans', None)
            # request.session.pop('key_ques', None)
            print("\n anserkey : ",key_answers_only)
            request.session['key_ans'] = key_answers_only #saving the text to session
            request.session['answers_list'] = answers_list #saving the text to session
            # request.session['key_ques'] = key_ques           
            return HttpResponseRedirect('papergrade')
        else:
            print("form is invalid")
    return render(request,'papergrading/paperkey_upload.html',{'answer_key': answer_key})
    # return render(request,'papergrading/result.html')
    
# student answer upload
def papergrade(request):
    student_answer = forms.StudentAnswerFileUploadForm()
    if request.method=='POST':
        student_answer = forms.StudentAnswerFileUploadForm(request.POST,request.FILES)
        if student_answer.is_valid():
            student_paper = student_answer.save(commit=False)
            student_paper.save()
            # student_answer_file = request.FILES['answer_file']
            # print(student_answer_file)
            student_id = int(request.POST['student'])
            course_id = int(request.POST['course'])
            student = Student.objects.get(pk=student_id)
            coursee = Course.objects.get(pk=course_id)
            # course_data = serialize('json', [coursee])
            student_name = student.__str__()
            request.session["student_name"] = student_name
            request.session["course_name"] = coursee.course_name
            filename = student_paper.answer_file.name
            hand = GeminiHandler()
            text_list = ['']
            image_paths = pdf_to_img(f"media/{filename}",f"media/temp")
            for path in image_paths:
                r = hand.gemini_output(path) 
                print(r) 
                text_list[0] = text_list[0] + f'\n {r}'
            print("\n text_list:  ",text_list)
            # joined_list = ''.join(text_list)
            # print(joined_list)
            text_struct = TextStruct(text_list[0])
            
            print("\n text struct : ",text_struct) 
            # struct_ques = []
            # struct_ans = []
            struct_ques,struct_ans = text_struct.extract()
            print("truct_answ :: ",struct_ans)
            request.session['struct_ans'] = struct_ans
            # filename = student_name
            # filepath = os.path.join(settings.MEDIA_ROOT, student_answer_file)
            # print("filepath=",filepath)
            # with open(filepath, 'wb') as f:
            #     for chunk in student_answer_file.chunks():
            #         f.write(chunk)
            
            # print("file",filepath)
            return redirect('paperresult', paper_id=student_paper.pk)#pasing the student answer id
            # return HttpResponseRedirect('paperresult',filename=filename)
        else:
            print("form invalid")
    return render(request, 'papergrading/papergrade.html',{'student_answer': student_answer}) 

# result
def paperresult(request,paper_id):
    model =  from_pretrained_keras("keras-io/bert-semantic-similarity")
    labels = ["Contradiction", "Perfect", "Neutral"]
    # print(filename)
    student_paper = Qpaper.objects.get(pk = paper_id)
    # print("student paper",student_paper.answer_file)
    filename = student_paper.answer_file.name
    # print("file name",filename)    
    key_answers_only = request.session.get('key_ans')
    answers_list = request.session.get('answers_list')
    text_struct = request.session.get('text_struct')
    struct_ans = request.session.get('struct_ans')
    
    
    # key_answers_only=[]
    # answers_list = list(key_ans.values())
    # print("answer list == ",answers_list)
    # # key_ques = request.session.get('key_ques')
    # for i in range(0,len(answers_list)):
    #     answer_k, marks_k = answers_list[i]
    #     print("\n answer_k : ",answer_k)
    #     print("\n marks_k: ",marks_k)
    #     key_ans_pre = preprocess(answer_k) #proproces
    #     print('\n key_ans_pre : ',key_ans_pre)
        
    #     key_answers_only.append(key_ans_pre)     
    # # request.session.pop('key_ans', None)
    # # request.session.pop('key_ques', None)
    # print("\n anserkey : ",key_answers_only)
    # print(key_ans,key_ques)
    # hand = GeminiHandler()
    # text_list = []
    # image_paths = pdf_to_img(f"media/{filename}",f"media/temp")
    # for path in image_paths:
    #     r = hand.gemini_output(path)  
    #     text_list.append(r)
    # print("\n text_list:  ",text_list[0])
    # joined_list = [' '.join(text_list)]
    # print("joined list:  ",joined_list)
    # text_struct = []
    # result = hand.gemini_output(f"media/{filename}")   
    # text_struct = TextStruct(text_list[0])   
    # text_struct = answer_struct_fn(text_list)  
    # print("\n text struct : ",text_struct) 
    # struct_ques = []
    # struct_ans = []
    # struct_ques,struct_ans = text_struct.extract() #structed data retrval 
    print("\n struct_ans : ",struct_ans)
    print("\n length struct_ans : ",len(struct_ans))
    print("andkeyonly : ",key_answers_only)
    print("length andkeyonly : ",len(key_answers_only))
    total_ans = len(answers_list)
    total_student_ans = len(struct_ans)
    # total_student_ans = len(text_struct)
    diff = total_ans-total_student_ans
    if diff>0 :                         
        for i in range(0,diff):
            struct_ans.append('null')
    elif diff<0 :
        for i in range(diff,0):
            key_answers_only.append('null')
    # if diff>0 :                         
    #     for i in range(0,diff):
    #         text_struct.append(['',''])
    # elif diff<0 :
    #     for i in range(diff,0):
    #         key_answers_only.append('') #if diff appending ""
    print("\n satha answer key : ",key_answers_only)
    # key_answers_only.reverse()
    # print("reverse answer key",key_answers_only)
    total_marks = 0.0
    marksheetform = forms.MarksheetForm()
    total_marks_ff = 0 
    print("ket_answers_only lenght : ",len(key_answers_only))
    print("answer list lenght : ",len(answers_list))
    for i in range(0,len(key_answers_only)):
        question = i+1
        _, maxmark = answers_list[i]
        total_marks_ff += maxmark
        # print("maxmark=",maxmark)
        print("\n key first answer : ",key_answers_only[i])
        # print("\n struct first ans : ",text_struct[i][1])
        print("\n struct first ans : ",struct_ans[i])
        ans_pre = preprocess(struct_ans[i])
        # ans_pre = preprocess(text_struct[i][1])
        key_keywords = extract_keywords(key_answers_only[i],top_n=10)
        print("\n key_kewords : ",key_keywords)
        # studans_keywords = extract_keywords(text_struct[i][1],top_n=10)
        studans_keywords = extract_keywords(struct_ans[i],top_n=10)
        print("\n ans_kewords : ",studans_keywords)
        data ={
            "inputs": {
            "source_sentence": key_answers_only[i],
            "sentences":[ans_pre]
            }}
        #bert
        bert_score = check_similarity(sentence1=key_answers_only[i],sentence2=ans_pre,model=model,labels=labels)
        perfect = bert_score['Perfect']
        neutral = bert_score['Neutral']
        contradiction = bert_score['Contradiction']
        try:
            semantic_score = Grading.marking(data)
            temp_similarity_score = semantic_score[0]

        except Exception as e:
            print("error")
            semantic_score = perfect
            temp_similarity_score = semantic_score
        # print(perfect,neutral,contradiction)
        # semantic_score = Grading.marking(data)
        keyword_score = calculate_keyword_similarity(student_keywords=studans_keywords,key_keywords=key_keywords)
        k_wordcount_score = count_words(answer=key_answers_only[i])
        stdans_wordcount_score = count_words(answer=ans_pre)
        # print(semantic_score)
        # print("key result",keyword_score/10)
        # temp_similarity_score = semantic_score[0]
        # print(temp_similarity_score)
        # if contradiction>semantic_score[0]:
        if contradiction>temp_similarity_score:

            temp_similarity_score = (contradiction-1)*10
        t_marks = calculate_total_marks(semantic_similarity=temp_similarity_score*10,keyword_similarity=keyword_score/10,total_marks=maxmark,word_count_key=k_wordcount_score,word_count_student=stdans_wordcount_score)
        # print("t_Total marks",t_marks)
        # mark = semantic_score[0]*10
        # total_marks_ff += maxmark
        mark = t_marks
        if mark<0.4 :
            pass
        total_marks += int(mark)
        obtained_marks = int(mark)

        mark_sheet = MarkSheet(
            question=question,
            maximum_marks=maxmark,
            obtained_marks= int(obtained_marks)
        )
        mark_sheet.save()
    marksheet = MarkSheet.objects.all()
    result = int(total_marks)
    student_name = request.session.get('student_name')
    course_name= request.session.get('course_name')
    request.session.pop('student_name', None)
    request.session.pop('course_name', None)
    request.session['data_displayed'] = True
    context = {
        'student_paper':student_paper,'result':result,
        'student_name':student_name,'marksheet':marksheet,
        'course_name':course_name,"filename":filename,
        'total_mark':total_marks_ff,
        }
    # print(marksheet['question']) 
    # return render(request, 'papergrading/paperresult.html',{'student_paper':student_paper,'result':result,'student_name':student_name,'marksheet':marksheet})
    return render(request, 'papergrading/result.html',context=context)

# report card
def generate_report_card(request):
    name = request.COOKIES.get('name')
    mark = request.COOKIES.get('mark')
    course = request.COOKIES.get('course') 
    print(name) # Assuming 'name' is an array of names
    # name = request.POST.getlist('name')  # Assuming 'name' is an array of names
    # Call the reportcard function
    image_paths = []
    out_path = reportcard(name=name, mark=mark, course=course)
    if os.path.exists(out_path):
        with open(out_path, 'rb') as file:
            response = HttpResponse(FileWrapper(file), content_type='image/jpg')
            response['Content-Disposition'] = f'attachment; filename="report_card_{name}.jpg"'
            return response
    else:
        return HttpResponse("File not found", status=404)
    
    
    # Return JSON response with paths to generated images
    





