from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('lessons/', views.lessons, name='lessons'),
    path('lessons/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('kanji/<str:level>/', views.kanji, name='kanji'),
    path('kanji/', views.kanji, name='kanji_default'),
    path('talkmate/<str:level>/', views.talkmate, name='talkmate'),
    path('talkmate/', views.talkmate, name='talkmate_default'),
    path('listening/<str:level>/', views.listening, name='listening'),
    path('listening/', views.listening, name='listening_default'),
    path('reading/<str:level>/', views.reading, name='reading'),
    path('reading/', views.reading, name='reading_default'),
    path('jlpt/<str:level>/test/', views.jlpt_test, name='jlpt_test'),
    path('jlpt/test/', views.jlpt_test, name='jlpt_test_default'),
]
