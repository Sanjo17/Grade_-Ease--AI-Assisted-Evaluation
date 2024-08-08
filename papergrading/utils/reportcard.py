import cv2
import os
from django.http import HttpResponse
from wsgiref.util import FileWrapper

# report card generation
def reportcard(name,mark,course):
    
    template_path = 'C:/code base/Main pro/gradeeaseeee/media/reportcardtemp/repo_temp.png'
    
    if not os.path.exists(template_path):
        print(f"Error: Template image '{template_path}' does not exist.")
        
    
    template = cv2.imread(template_path)
    
    if template is None:
        print(f"Error: Unable to read template image '{template_path}'.")
        
    
    cv2.putText(template, str(name), (532, 562), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(template, str(course), (538, 955), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(template, str(mark), (818, 960), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
    
    out_path = f'C:/code base/Main pro/gradeeaseeee/media/temp/{name}.jpg'
    cv2.imwrite(out_path, template)
    
    if not os.path.exists(out_path):
        print(f"Error: Unable to save image to '{out_path}'.")
    return out_path
        
    
    # print(f'Processed {index+1}/{len(list_names)}')
