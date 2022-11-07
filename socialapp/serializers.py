from rest_framework import serializers
from django.contrib.auth.models import User
from socialapp.models import Questions 
# ,Answers

class UserSerialiizer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=["email","username","password"]

# encryption of password
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# question serializer
class QuestionSerializer(serializers.ModelSerializer):
    created_by=serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model=Questions
        fields=["title","description","image","created_by"]

# answer serializer
# class AnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Answers
#         fields=["question","answer","created_by"]
