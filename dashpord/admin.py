from django.contrib import admin
from .models import *
model=[StudyGroup,System,Lecture,Book,BookCall,LectureCall]
for i in model:
    admin.site.register(i)
    
    



