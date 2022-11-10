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
# ----------------------------------------------------------------------------------
# localhost:8000/questions/     post
# localhost:8000/questions/     get

class QuestionView(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
# ---------------------------------------------------------------------------------
# localhost:8000/questions/my_questions/

    @action(methods=['GET'],detail=False)
    def my_questions(self,request,*args,**kwargs):
        qs=request.user.questions_set.all()
        serializer=QuestionSerializer(qs,many=True)
        return Response(data=serializer.data)

        # qs=Questions.objects.filter(created_by=request.user)
# --------------------------------------------------------------------------------
# localhost:8000/questions/1/add_answer/

    @action(methods=["POST"],detail=True)
    def add_answer(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        ques=Questions.objects.get(id=id)
        usr=request.user
        serializer=AnswerSerializer(data=request.data,context={"created_by":usr,"question":ques})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

# ----------------------------------------------------------------------------------
# localhost:8000/questions/1/list_answers/

    @action(methods=["GET"],detail=True)
    def list_answers(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        ques=Questions.objects.get(id=id)
        qs=ques.answers_set.all()
        serializer=AnswerSerializer(qs,many=True)
        return Response(data=serializer.data)

# ----------------------------------------------------------------------------------
# localhost:8000/answers/1/up_vote/

class AnswersView(ModelViewSet):
    serializer_class=AnswerSerializer
    queryset=Answers.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    @action(methods=["get"],detail=True)
    def up_vote(self,request,*args,**kwargs):
        ans=self.get_object()       # answer object
        usr=request.user
        ans.upvote.add(usr)
        return Response(data="created")

        


