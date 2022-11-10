from django.db.models import Count
from django.db import models
from django.contrib.auth.models import User


# FOR QUESTIONS

class Questions(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=500)
    image=models.ImageField(upload_to="images",null=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)

    # to written/return answers along with questions
    # by using property we can access objects as an attribute
    # taken one question as object

    @property
    def question_answers(self):
        qs=self.answers_set.all().annotate(u_count=Count('upvote')).order_by('-u_count')   
        return qs

    def __str__(self):
        return self.title

# FOR ANSWERS

class Answers(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    answer=models.CharField(max_length=500)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    upvote=models.ManyToManyField(User,related_name="up_vote")

    @property
    def votecount(self):
        return self.upvote.all().count()

    def __str__(self):
        return self.answer
        