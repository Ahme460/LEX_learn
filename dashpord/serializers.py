from rest_framework import serializers
from .models import *
from rest_framework.exceptions import NotFound


class Grou_study(serializers.ModelSerializer):
    class Meta:
        model= StudyGroup
        fields="__all__"
        
        
class System_study(serializers.ModelSerializer):
    class Meta:
        model= System
        fields="__all__"
        
        
class Books_System_selizer(serializers.ModelSerializer):
    class Meta:
        model= Book
        fields=["id","System","title","image","author","university","release_date"]
        
    
class Order_Book_selizer(serializers.ModelSerializer):
    class Meta:
        model=BookCall
        fields=["book"]
    def validate(self, attrs):
        book = attrs.get("book")
        book_id = book.id
        
        if not isinstance(book_id, int): 
            raise serializers.ValidationError(
                {"book": "Book must be an ID (integer)."}
                )
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise NotFound(detail={"error": "Book not found."})

        return attrs

    def create(self, validated_data):
       user=self.context['request'].user
       validated_data['user'] = user
       return  super().create(validated_data)


class Lecture_Sleizer(serializers.ModelSerializer):
    class Meta:
        model=Lecture
        exclude=('video_url',)
               
    
class Order_Lecture_selizer(serializers.ModelSerializer):
    class Meta:
        model=LectureCall
        fields=["lecture"]
        
        
    def validate(self, attrs):
        lecture = attrs.get("lecture")
        if not lecture:
            raise NotFound(
                detail="not id lecture"
            )
        lecture_id = getattr(lecture,"id",None)
        if not isinstance(lecture_id, int): 
            raise serializers.ValidationError(
            {
            "lecture":"lecture must be an ID (integer)."
            })
        try:
            lecture = Lecture.objects.get(id=lecture_id)
        except Lecture.DoesNotExist:
            raise NotFound(
                detail={"error": "lecture not found."}
                )
        return attrs

    def create(self, validated_data):
       user=self.context['request'].user
       validated_data['user'] = user
       return  super().create(validated_data)