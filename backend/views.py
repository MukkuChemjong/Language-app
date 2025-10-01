# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from api.models import Lessons, Question, QuestionOption, UserAnswer, LessonProgress
import json
import random
from django.utils import timezone

def index(request):
    """Main page showing all lessons"""
    return render(request, 'api/index.html')

def lessons_api(request):
    """API endpoint for React to fetch lessons data"""
    lessons = Lessons.objects.all().order_by('name')
    
    lessons_data = []
    for lesson in lessons:
        # Ensure slug exists, create one if missing
        if not lesson.slug:
            from django.utils.text import slugify
            lesson.slug = slugify(lesson.name)
            lesson.save()
        
        lessons_data.append({
            'id': lesson.id,
            'name': lesson.name,
            'name_limbu': lesson.name_limbu or '',
            'image': lesson.image.url if lesson.image else None,
            'slug': lesson.slug,
            'question_count': lesson.questions.count(),
        })
    
    return JsonResponse({
        'lessons': lessons_data
    })

def lesson_detail(request, slug):
    """Individual lesson page with questions"""
    lesson = get_object_or_404(Lessons, slug=slug)
    return render(request, 'api/lesson_detail.html', {'lesson': lesson})

def lesson_questions_api(request, slug):
    """API endpoint to get all questions for a lesson"""
    lesson = get_object_or_404(Lessons, slug=slug)
    questions = lesson.questions.all().order_by('order')
    
    questions_data = []
    for question in questions:
        options_data = []
        for option in question.options.all().order_by('order'):
            options_data.append({
                'id': option.id,
                'order': option.order,
                'text_english': option.option_text_english,
                'text_limbu': option.option_text_limbu,
                'is_correct': option.is_correct,
            })
        
        questions_data.append({
            'id': question.id,
            'order': question.order,
            'subject_image': question.subject_image.url if question.subject_image else None,
            'subject_name_english': question.subject_name_english,
            'points': question.points,
            'options': options_data,
        })
    
    return JsonResponse({
        'lesson': {
            'id': lesson.id,
            'name': lesson.name,
            'name_limbu': lesson.name_limbu,
            'slug': lesson.slug,
        },
        'questions': questions_data,
        'total_questions': len(questions_data),
    })

@csrf_exempt
@require_http_methods(["POST"])
def submit_answer(request):
    """API endpoint to submit an answer"""
    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        selected_option_id = data.get('selected_option_id')
        language_mode = data.get('language_mode', 'english')
        time_taken = data.get('time_taken')
        
        question = get_object_or_404(Question, id=question_id)
        selected_option = get_object_or_404(QuestionOption, id=selected_option_id)
        
        # Check if answer is correct
        is_correct = selected_option.is_correct
        
        # Save user answer (optional - for tracking)
        user_answer = UserAnswer.objects.create(
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
            language_mode=language_mode,
            time_taken=time_taken,
        )
        
        # Get the correct answer for feedback
        correct_option = question.options.filter(is_correct=True).first()
        
        return JsonResponse({
            'success': True,
            'is_correct': is_correct,
            'correct_answer': {
                'english': correct_option.option_text_english,
                'limbu': correct_option.option_text_limbu,
            } if correct_option else None,
            'points_earned': question.points if is_correct else 0,
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def complete_lesson(request):
    """API endpoint when user completes a lesson"""
    try:
        data = json.loads(request.body)
        lesson_id = data.get('lesson_id')
        total_questions = data.get('total_questions')
        correct_answers = data.get('correct_answers')
        
        lesson = get_object_or_404(Lessons, id=lesson_id)
        score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # Save lesson progress
        progress = LessonProgress.objects.create(
            lesson=lesson,
            total_questions=total_questions,
            correct_answers=correct_answers,
            score_percentage=score_percentage,
            completed_at=timezone.now(),
        )
        
        return JsonResponse({
            'success': True,
            'score_percentage': score_percentage,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'passed': score_percentage >= 70,  # 70% to pass
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)

        }, status=400)
