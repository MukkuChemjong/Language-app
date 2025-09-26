# api/urls.py (your app URLs)
from django.urls import path
from backend import views

app_name = 'api'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('lesson/<slug:slug>/', views.lesson_detail, name='lesson_detail'),
    
    # API endpoints
    path('api/lessons/', views.lessons_api, name='lessons_api'),
    path('api/lesson/<slug:slug>/questions/', views.lesson_questions_api, name='lesson_questions_api'),
    path('api/submit-answer/', views.submit_answer, name='submit_answer'),
    path('api/complete-lesson/', views.complete_lesson, name='complete_lesson'),
]