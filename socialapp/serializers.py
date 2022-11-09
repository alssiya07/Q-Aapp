from rest_framework import serializers
from django.contrib.auth.models import User
from socialapp.models import Questions,Answers

# user serializer
class UserSerialiizer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=["email","username","password"]

# encryption of password
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# question serializer
class QuestionSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    created_by=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    class Meta:
        model=Questions
        fields=["id","title","description","image","created_by","created_date"]

# answer serializer
class AnswerSerializer(serializers.ModelSerializer):
    created_by=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    question=serializers.CharField(read_only=True)
    class Meta:
        model=Answers
        fields=["question","answer","created_by","created_date"]
    
# exracting question
    def create(self,validated_data):
        ques=self.context.get("question")
        usr=self.context.get("created_by")
        return ques.answers_set.create(created_by=usr,**validated_data)

class QuestionSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    created_by=serializers.CharField(read_only=True)
    question_answers=AnswerSerializer(read_only=True,many=True)

    class Meta:
        model=Questions
        fields=["id","title",
        "description","image",
        "created_by","created_date",
        "question_answers"]