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

class ProjectTest(TestCase):
  def setUp(self):
    self.user=User.objects.create(username='burens')
    self.user.save()
    self.project=Projects.objects.create(id=1,name='portfolio',description='lol',project_image='image.png',urls='www.lol.com',profile=self.user)

  def tearDown(self):
      Projects.objects.all().delete()
      User.objects.all().delete()

  def test_instance(self):
    self.assertTrue(isinstance(self.project, Projects))

  def test_save_project(self):
    self.project.save_project()
    total_proj=Projects.objects.all()
    self.assertEqual(len(total_proj),1)

  def test_delete_project(self):
    self.project.save_project()
    projects=Projects.objects.all()
    self.assertEqual(len(projects),1)
    self.project.delete_project()
    total_proj=Projects.objects.all()
    self.assertTrue(len(total_proj)==0)