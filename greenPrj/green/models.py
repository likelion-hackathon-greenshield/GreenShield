from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    CATEGORY_CHOICES = (
        ('health', '건강 게시판'),
        ('free', '자유 게시판'),
    )
    
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f'{self.category} 게시판 - {self.id}'
    
    def get_likes_count(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author.username}'
    
class Expert(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='experts/')

    def __str__(self):
        return self.name
    
class Reservation(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_file = models.ImageField(upload_to='payment/', null=True, blank=True)