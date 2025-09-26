# admin.py
from django.contrib import admin
from .models import Lessons, Question, QuestionOption, Vocabulary, UserAnswer, LessonProgress

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 10  # Show 10 option fields by default
    max_num = 10  # Maximum 10 options
    fields = ['order', 'option_text_limbu', 'is_correct']

@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_limbu', 'created_at']
    search_fields = ['name', 'name_limbu']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'order', 'subject_name_english', 'points']
    list_filter = ['lesson', 'created_at']
    search_fields = ['subject_name_english']
    inlines = [QuestionOptionInline]
    ordering = ['lesson', 'order']

@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'option_text_english', 'option_text_limbu', 'is_correct']
    list_filter = ['is_correct', 'question__lesson']
    search_fields = ['option_text_english', 'option_text_limbu']

@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ['word_english', 'word_limbu', 'category', 'lesson']
    list_filter = ['category', 'lesson']
    search_fields = ['word_english', 'word_limbu', 'category']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'selected_option', 'is_correct', 'language_mode', 'answered_at']
    list_filter = ['is_correct', 'language_mode', 'answered_at']
    readonly_fields = ['answered_at']

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'correct_answers', 'total_questions', 'score_percentage', 'completed_at']
    list_filter = ['completed_at', 'lesson']