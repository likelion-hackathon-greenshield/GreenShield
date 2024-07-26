from django.contrib import admin
from .models import Category, Product, Post, Comment, Expert, Question, Answer, CheckList

# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__id')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'company', 'price', 'url')
    list_filter = ('category',)

admin.site.register(Category)

admin.site.register(Product, ProductAdmin)

admin.site.register(Post)

admin.site.register(Comment)

admin.site.register(Expert)

admin.site.register(Question)

admin.site.register(Answer)

admin.site.register(CheckList)
