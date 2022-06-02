from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Profile

User = get_user_model()


class ProfileTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='Julia', email='julia@gmail.com', password='julia cesar')

    def test_create_profile(self):
        julia = Profile.objects.get(user__username='Julia')
        self.assertIsNotNone(julia)
        self.assertEqual(julia.level, 1)
        julia.level = 50
        julia.save()
        self.assertEqual(julia.level, 50)

    def test_set_favorite_articles(self):
        julia = Profile.objects.get(user__username='Julia')
        julia.favorite_articles = ['1', '2']
        julia.save()
        self.assertEqual(julia.favorite_articles, ['1', '2'])


# import os
# import unittest

# from yourpackage.forms import MyForm

# class TestCase(unittest.TestCase):
#     def setUp(self):
#         os.environ['RECAPTCHA_DISABLE'] = 'True'

#     def test_myform(self):
#         form = MyForm({
#             'field1': 'field1_value'
#         })
#         self.assertTrue(form.is_valid())

#     def tearDown(self):
#         del os.environ['RECAPTCHA_DISABLE']
