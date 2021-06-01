from django import urls
from awwwardsapp.views import profile
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile,Projects,Ratings
from .models import *

# Create your tests here.
class ProfileClass(TestCase):
  def setUp(self):
    self.user = User(username='burens')
    self.user.save()
    self.profile=Profile(user=self.user,url='www.lol.com',profile_pic='lol.png',bio='awesome',location='kenya',email='mail@gmail.com')
    
  def tearDown(self):
    Profile.objects.all().delete()
    User.objects.all().delete()
  
  def test_instance(self):
    self.assertTrue(isinstance(self.profile, Profile))

  def test_save_profile(self):
    self.new_profile=Profile(user=self.kanosa,url='www.lol.com',profile_pic='lol.png',bio='awesome',location='kenya',email='mail@gmail.com')
    self.new_profile.save_profile()
    profiles=Profile.objects.all()
    self.assertEqual(len(profiles),1)