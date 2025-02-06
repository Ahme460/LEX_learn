from django.shortcuts import render
from rest_framework.generics import ListAPIView ,CreateAPIView ,ListCreateAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *

class All_Group_staude(ListAPIView):
    permission_classes=[IsAuthenticated]
    queryset=StudyGroup.objects.all()
    serializer_class= Grou_study
    
    


class All_Group_staude(APIView):
    permission_classes=[IsAuthenticated]
    def get (self,request,id):
        try:
            grop=StudyGroup.objects.get(id=id)
            subject=grop.subject.all()
            serializer=Subject_study(subject)
            if serializer.is_valid():
                return Response(serializer.data,status=status.HTTP_200_OK)            
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        





