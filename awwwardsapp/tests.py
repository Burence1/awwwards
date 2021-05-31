from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile,Projects,Ratings

# Create your tests here.
class ProjectsClass(TestCase):
  def setUp(self):
    self.burens = User(username='burens',email='burensdev@gmail.com',password='lol')