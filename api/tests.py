from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from io import BytesIO
from PIL import Image
from .models import Lessons  # Replace 'your_app' with your actual app name


class LessonsModelTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.lesson_data = {
            'name': 'Introduction to Python'
        }
    
    
    def test_create_lesson_without_image(self):

        lesson = Lessons.objects.create(**self.lesson_data)
        
        self.assertEqual(lesson.name, 'Introduction to Python')
        self.assertIsNone(lesson.image.name)
        self.assertTrue(lesson.image.name in ['', None])
    
    """
    def test_create_lesson_with_image(self):
        
        # Create a simple test image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
        
        lesson = Lessons.objects.create(
            name='Django Basics',
            image=test_image
        )
        
        self.assertEqual(lesson.name, 'Django Basics')
        self.assertTrue(lesson.image.name.startswith('lessons/images/'))
        self.assertTrue(lesson.image.name.endswith('.jpg'))
    
    def test_str_method(self):
        
        lesson = Lessons.objects.create(**self.lesson_data)
        self.assertEqual(str(lesson), 'Introduction to Python')
    
    def test_name_max_length(self):
        
        long_name = 'x' * 201  # Exceeds max_length of 200
        
        with self.assertRaises(DataError):
            Lessons.objects.create(name=long_name)
    
    def test_name_field_required(self):
        
        with self.assertRaises(ValidationError):
            lesson = Lessons(name='')
            lesson.full_clean()
    
    def test_image_field_optional(self):
        
        lesson = Lessons.objects.create(name='Test Lesson')
        self.assertIsNotNone(lesson)
        self.assertEqual(lesson.image.name, '')
    
    def test_image_upload_path(self):
        
        image = Image.new('RGB', (50, 50), color='blue')
        image_io = BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)
        
        test_image = SimpleUploadedFile(
            name='upload_test.png',
            content=image_io.getvalue(),
            content_type='image/png'
        )
        
        lesson = Lessons.objects.create(
            name='Upload Path Test',
            image=test_image
        )
        
        self.assertTrue(lesson.image.name.startswith('lessons/images/'))
    
    def test_model_fields_exist(self):
        
        lesson = Lessons()
        
        # Check that fields exist
        self.assertTrue(hasattr(lesson, 'name'))
        self.assertTrue(hasattr(lesson, 'image'))
    
    def test_multiple_lessons_creation(self):
        
        lessons_data = [
            {'name': 'Lesson 1'},
            {'name': 'Lesson 2'},
            {'name': 'Lesson 3'}
        ]
        
        for data in lessons_data:
            Lessons.objects.create(**data)
        
        self.assertEqual(Lessons.objects.count(), 3)
        
        # Test that all lessons were created correctly
        lesson_names = list(Lessons.objects.values_list('name', flat=True))
        expected_names = ['Lesson 1', 'Lesson 2', 'Lesson 3']
        self.assertEqual(sorted(lesson_names), sorted(expected_names))
    
    def test_lesson_update(self):
        
        lesson = Lessons.objects.create(name='Original Name')
        
        # Update the lesson
        lesson.name = 'Updated Name'
        lesson.save()
        
        # Refresh from database
        lesson.refresh_from_db()
        self.assertEqual(lesson.name, 'Updated Name')
    
    def test_lesson_deletion(self):
       
        lesson = Lessons.objects.create(name='To be deleted')
        lesson_id = lesson.id
        
        # Delete the lesson
        lesson.delete()
        
        # Verify it's deleted
        with self.assertRaises(Lessons.DoesNotExist):
            Lessons.objects.get(id=lesson_id)
    
    def tearDown(self):
        
        # Clean up any uploaded files
        for lesson in Lessons.objects.all():
            if lesson.image:
                lesson.image.delete()
        
        # Clear all lessons
        Lessons.objects.all().delete()
    """