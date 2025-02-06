from rest_framework import serializers
from .models import *


class Grou_study(serializers.ModelSerializer):
    class Meta:
        model= StudyGroup
        fields="__all__"
        
        
class Subject_study(serializers.ModelSerializer):
    class Meta:
        model= Subject
        fields="__all__"
        