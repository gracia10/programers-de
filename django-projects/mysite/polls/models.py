from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='질문')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    owner = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE, null=True)

    @admin.display(boolean=True, description='최근생성(하루기준)')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'voter'], name='unique_voter_for_question')
        ]
