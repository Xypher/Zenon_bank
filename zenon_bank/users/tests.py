from django.test import TestCase

from django.contrib.auth.models import User

from .models import Student


class StudentTestCase(TestCase):

    def setUp(self):
        
        user = User(username="testuser")
        user.save()
        Student.objects.create(
            user=user,
            department=Student.Computer_Engineer,
            gender=Student.Male,
            phone_number="0777777777",
            biography="lorem impsum"
        )
    
    def test_exists(self):

        test_Student= Student.objects.get(phone_number="0777777777")
        self.assertEqual(test_Student.user.username, "testuser")
        self.assertEqual(test_Student.biography, "lorem impsum")
        
