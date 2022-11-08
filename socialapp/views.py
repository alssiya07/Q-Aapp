from django.shortcuts import render

# Create your views here.

from socialapp.serializers import UserSerialiizer,QuestionSerializer,AnswerSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from socialapp.models import Questions,Answers
from rest_framework import authentication,permissions
from rest_framework.decorators import action

# localhost:8000/users/
class UsersView(ModelViewSet):
    serializer_class=UserSerialiizer
    queryset=User.objects.all()
#----------------------------------------------------------------------------------
# localhost:8000/questions/     post
# localhost:8000/questions/     get
class QuestionView(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# localhost:8000/questions/my_questions/

    @action(methods=['GET'],detail=False)
    def my_questions(self,request,*args,**kwargs):
        qs=request.user.questions_set.all()
        serializer=QuestionSerializer(qs,many=True)
        return Response(data=serializer.data)

        # qs=Questions.objects.filter(created_by=request.user)
#--------------------------------------------------------------------------------
# localhost:8000/question/1/add_answers/
    def add_answer(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        ques=Questions.objects.get(id=id)
        ans=request.user
        serializer=AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

# example
    def create(self,request,*args,**kwargs):
        serializer=AnswerSerializer(data=request.data)
        if serializer.is_valid():
            Answers.objects.create(**serializer.validated_data,context={"created_by":request.user})  # (user=request.user) for normal case
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)