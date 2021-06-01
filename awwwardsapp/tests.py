from django import urls
from awwwardsapp.views import profile, project
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

  def test_search_projects(self):
    self.project.save_project()
    projects=Projects.search_project('project')
    self.assertTrue(len(projects),1)
  
  def test_get_all_projects(self):
    self.project.save_project()
    projects=Projects.get_all_projects()
    self.assertEqual(len(projects),1)
  
  def test_get_project(self):
    project=Projects.objects.create(id=1,name='portfolio',description='lol',project_image='image.png',urls='www.lol.com',profile=self.user)
    self.project.save_project()
    project=Projects.get_project(id=self.project.id)
    self.assertTrue(len(project),1)
  
  def test_user_projects(self):
    projects=Projects.user_projects(self.profile.id)
    self.assertEqual(projects[0].name,'portfolio')
    self.assertEqual(len(projects),1)

class RatingsTestClass(TestCase):
  def setUp(self):
    self.user = User.objects.create(username='burens')
    self.project=Projects.objects.create(id=1,name='portfolio',description='lol',project_image='image.png',urls='www.lol.com',profile=self.user)
    self.rating = Ratings.objects.create(id=1, design=9, usability=10, content=10, profile=self.user, prjects=self.project)

  def tearDown(self):
    User.objects.all().delete()
    Projects.objects.all().delete()
    Ratings.objects.all().delete()

  def test_instance(self):
    self.assertTrue(isinstance(self.rating,Ratings))
  
  def test_save_rating(self):
    self.rating = Ratings.objects.create(id=1, design=9, usability=10, content=10, profile=self.user, prjects=self.project)
    self.rating.save_rating()
    ratings=Ratings.objects.all()
    self.assertEqual(len(ratings),1)
  
  def test_delete_rating(self):
    self.rating = Ratings.objects.create(id=1, design=9, usability=10, content=10, profile=self.user, prjects=self.project)
    self.rating.save_rating()
    ratings = Ratings.objects.all()
    self.assertEqual(len(ratings), 1)
    self.rating.delete_rating()
    rate=Ratings.objects.all()
    self.assertEqual(len(rate),0)

  def test_project_votes(self):
    self.project=Projects.objects.create(id=1,name='portfolio',description='lol',project_image='image.png',urls='www.lol.com',profile=self.user)
    self.rating = Ratings.objects.create(id=1, design=9, usability=10, content=10, profile=self.user, prjects=self.project)
    self.rating.save_rating()
    ratings=Ratings.project_votes(project=self.project)
    self.assertEqual(ratings[0].name, 'portfolio')
    self.assertTrue(len(ratings),1)

  def test_project_voters(self):
    self.profile=Profile(user=self.user,url='www.lol.com',profile_pic='lol.png',bio='awesome',location='kenya',email='mail@gmail.com')
    self.profile.save_profile()
    voters=Ratings.project_votes(self.profile)
    self.assertTrue(len(voters),1)
    self.assertEqual(voters[0].rater.user.username, 'burens')