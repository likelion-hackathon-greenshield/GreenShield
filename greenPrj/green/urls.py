from django.urls import path
from . import views

app_name = 'green'

urlpatterns = [
    path('main/', views.main_view, name='main'),
    path('community/', views.community, name='community'),
    path('mypage/', views.mypage, name='mypage'),
    path('list/', views.list_view, name='list'),
    path('expert/', views.expert, name='expert'),
    path('market/', views.market, name='market'),
    path('test/', views.test_view, name='test'),
    path('result/', views.result_view, name='result'),
]