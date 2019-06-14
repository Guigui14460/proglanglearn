from django.contrib.auth.models import User
from django.test import TestCase

from .models import Profile


class ProfileTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='Julia', email='julia@gmail.com', password='jules cesar')

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
