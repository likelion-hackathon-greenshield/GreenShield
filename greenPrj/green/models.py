from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    order = models.PositiveIntegerField() # 설문 문항 순서 (필요하다면)
    question = models.CharField(max_length=100, null=True) # 설문 문항
    to_do = models.CharField(max_length=100, null=True) # 해야 할 일
    tip = models.CharField(max_length=100, null=True) # 팁

    def __str__(self):
        return f'{self.question}'

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField() # 1~5의 점수
    timestamp = models.DateTimeField(auto_now_add=True)  # 설문 응답 시간
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.score}'
    
class CheckList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    date = models.DateField(auto_created=True)

    def __str__(self):
        return f'{self.complete}'