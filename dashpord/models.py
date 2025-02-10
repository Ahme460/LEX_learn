from django.db import models
from user.models import Account

class StudyGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class System(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE,related_name="subject")

    def __str__(self):
        return self.name

class Lecture(models.Model):
    System = models.ForeignKey(System, on_delete=models.CASCADE,related_name='lecture')
    title = models.CharField(max_length=255)
    img_lecture=models.FileField(upload_to="img_lecture/")
    teacher = models.CharField(max_length=100)
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    requires_approval = models.BooleanField(default=True)
    
    def __str__(self):
        return f"lecture {self.title}"
    


class Book(models.Model):
    System=models.ForeignKey(System,on_delete=models.CASCADE,related_name='books')
    title = models.CharField(max_length=255)
    image=models.FileField(upload_to='img_books')
    author = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='books/')
    requires_approval = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title


class BookCall(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - Book Access - {self.book.title} - Approved: {self.is_approved}"


    
class LectureCall(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    lecture=models.ForeignKey(Lecture,on_delete=models.CASCADE,null=True)
    is_approved = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - Lecture Access - {self.lecture.title} - Approved: {self.is_approved}"





# class QuestionCall(models.Model):
#     user = models.ForeignKey(Account, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # المادة
#     is_approved = models.BooleanField(default=False)  # هل تمت الموافقة؟
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user} - Question Access - {self.subject} - Approved: {self.is_approved}"
# class Test(models.Model):
#     subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name="test")
#     name=models.CharField(max_length=400)
#     detal=models.TextField(null=True)
    
#     @property
#     def totle_question(self):
#         all_question=QuestionBank.objects.filter(id=self.id).count()
#         return all_question

# class QuestionBank(models.Model):
#     packed_question=models.ForeignKey(Test,on_delete=models.CASCADE)
#     question_text = models.TextField()
#     correct_answer = models.TextField()
#     choses=models.TextField()
        
#     requires_approval = models.BooleanField(default=True)

