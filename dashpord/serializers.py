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
        fields=["id","System","title","image","author"]
        
    
class Order_Book_selizer(serializers.ModelSerializer):
    class Meta:
        model=BookCall
        fields=["System","book"]
    def validate(self, attrs):
        system_id = attrs.get("System").id
        book_id = attrs.get("book").id
        print(system_id)
        

        if not isinstance(system_id, int):  
            raise serializers.ValidationError({"System": "System must be an ID (integer)."})

        if not isinstance(book_id, int): 
            raise serializers.ValidationError({"book": "Book must be an ID (integer)."})

        try:
            system = System.objects.get(id=system_id)
        except System.DoesNotExist:
            raise NotFound(detail={"error": "System not found."})

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise NotFound(detail={"error": "Book not found."})

        return attrs

    def create(self, validated_data):
       user=self.context['request'].user
       validated_data['user'] = user
       return  super().create(validated_data)
    
        
        

