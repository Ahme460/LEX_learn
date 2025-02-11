from django.shortcuts import render
from rest_framework.generics import ListAPIView ,CreateAPIView ,ListCreateAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
import mimetypes
from django.http import FileResponse


class All_Group_staude(ListAPIView):
    permission_classes=[IsAuthenticated]
    queryset=StudyGroup.objects.all()
    serializer_class= Grou_study
    

class All_System_in_grade(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id):
        try:
            grop=get_object_or_404(StudyGroup,id=id)
            subject=grop.subject.all()
            print(subject)
            serializer=System_study(subject,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)            
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)


class Books_System(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class= Books_System_selizer
    def get_queryset(self):
        id=self.kwargs.get('id')
        books=Book.objects.filter(System__id=id)
        booked_books = BookCall.objects.filter(user=self.request.user).values_list("book_id", flat=True)
        books = books.exclude(id__in=booked_books)
        return books
        


class Create_Order_Book(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=Order_Book_selizer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request)
    
 
        
class BookFileView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        
        book_call=BookCall.objects.filter(user=request.user,is_approved=True)
        if not book_call.exists():
            raise NotFound(detail={"error": "No book calls found for this user."})
        else:
            books = list(book_call.values(
                "book__id", "book__title", "book__System__name", "book__author",
                "book__image", "book__pdf_file", "book__release_date", "book__university"
            ))
            for book in books:
                book["book__image"] = request.build_absolute_uri('/media/' + book["book__image"]) if book["book__image"] else None
                book["book__pdf_file"] = request.build_absolute_uri('/media/' + book["book__pdf_file"]) if book["book__pdf_file"] else None

            return Response({"books": books}, status=status.HTTP_200_OK)

class Lecture_Viewset(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=Lecture_Sleizer
    def get_queryset(slef):
        id_system=slef.kwargs.get('id')
        Lectures=Lecture.objects.filter(System__id=id_system)
        Lecture_order=LectureCall.objects.values_list("lecture__id",flat=True)
        Lectures=Lectures.exclude(id__in=Lecture_order)
        return Lectures


class Create_Order_Lecture(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=Order_Lecture_selizer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request)
    
 
 
class Lecture_data_view(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        
        lectures_call=LectureCall.objects.filter(user=request.user,is_approved=True)
        if not lectures_call.exists():
            raise NotFound(detail={"error": "No lectures calls found for this user."})
        else:
            lectures=list(lectures_call.values("lecture__id", "lecture__title", 
                                        "lecture__img_lecture","lecture__teacher",
                                        "lecture__video_url","lecture__created_at"))
            for lecture in lectures:
                lecture['lecture__img_lecture']=request.build_absolute_uri('/media/'+lecture['lecture__img_lecture'])if lecture['lecture__img_lecture'] else None

            return Response({"lectures":lectures},status=status.HTTP_200_OK)
        
        
        
class Delete_user(APIView):
    def delete(self,request):
        try:
            user=request.user
            user=Account.objects.get(id=user.id)
            user.delete()
            return Response({"delete_account":" done"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"eroor":str(e)},status=status.HTTP_400_BAD_REQUEST)
            