from django.shortcuts import render

# Create your views here.

from socialapp.serializers import UserSerialiizer,QuestionSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from socialapp.models import Questions,Answers
from rest_framework import authentication,permissions

class UsersView(ModelViewSet):
    serializer_class=UserSerialiizer
    queryset=User.objects.all()

class QuestionView(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# class AnswerView(ModelViewSet):
#     serializer_class=AnswerSerializer
#     queryset=Answers.objects.all()
