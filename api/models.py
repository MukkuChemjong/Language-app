# models.py
from django.db import models

class Lessons(models.Model):
    name = models.CharField(max_length=200)
    name_limbu = models.CharField(max_length=200, help_text="Lesson name in Limbu", blank=True, null=True)
    image = models.ImageField(upload_to='lessons/')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Lessons"

class Question(models.Model):
    """Each question shows an image with the Limbu word and 10 multiple choice options"""
    lesson = models.ForeignKey(
        Lessons, 
        on_delete=models.CASCADE, 
        related_name='questions'
    )
    
    # The subject being taught (e.g., "apple", "house", "water")
    subject_image = models.ImageField(
        upload_to='questions/images/', 
        help_text="Image of the subject being taught"
    )
    
    # The correct answer/subject name
    subject_name_english = models.CharField(
        max_length=100, 
        help_text="What the image shows in English"
    )
    
    # Question order in the lesson
    order = models.PositiveIntegerField(default=0, help_text="Question order in the lesson")
    
    # Points and metadata
    points = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['lesson', 'order']
        unique_together = ['lesson', 'order']
    
    def __str__(self):
        return f"{self.lesson.name} - Q{self.order}: {self.subject_name_english}"

class QuestionOption(models.Model):
    """10 multiple choice options for each question"""
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='options'
    )
    
    # The option text in both languages
    option_text_english = models.CharField(max_length=200, help_text="Option in English")
    option_text_limbu = models.CharField(max_length=200, help_text="Option in Limbu")
    
    # Whether this is the correct answer
    is_correct = models.BooleanField(default=False)
    
    # Order of the option (1-10)
    order = models.PositiveIntegerField(help_text="Option order (1-10)")
    
    class Meta:
        ordering = ['question', 'order']
        unique_together = ['question', 'order']
    
    def __str__(self):
        status = "✓" if self.is_correct else "✗"
        return f"{status} {self.option_text_english} / {self.option_text_limbu}"

# Optional: Vocabulary bank for generating random options
class Vocabulary(models.Model):
    """Bank of words to generate random incorrect options"""
    lesson = models.ForeignKey(
        Lessons, 
        on_delete=models.CASCADE, 
        related_name='vocabulary',
        null=True, 
        blank=True
    )
    word_english = models.CharField(max_length=200)
    word_limbu = models.CharField(max_length=200)
    category = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="e.g., 'animals', 'food', 'colors'"
    )
    
    class Meta:
        ordering = ['word_english']
        unique_together = ['word_english', 'word_limbu']
    
    def __str__(self):
        return f"{self.word_english} / {self.word_limbu}"

# Optional: Track user progress
class UserAnswer(models.Model):
    """Track user responses and progress"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(
        QuestionOption, 
        on_delete=models.CASCADE,
        help_text="Which option the user selected"
    )
    is_correct = models.BooleanField()
    language_mode = models.CharField(
        max_length=10,
        choices=[('english', 'English'), ('limbu', 'Limbu')],
        default='english',
        help_text="Language mode when answered"
    )
    time_taken = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text="Time taken to answer in seconds"
    )
    answered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Answer: {self.question.subject_name_english} - {'Correct' if self.is_correct else 'Wrong'}"

# Optional: User progress tracking
class LessonProgress(models.Model):
    """Track overall progress in a lesson"""
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    score_percentage = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.lesson.name} - {self.score_percentage}%"