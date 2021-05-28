from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
  profile_pic=CloudinaryField('photo')
  bio=models.TextField()
  location=models.CharField(max_length=50)
  email=models.EmailField()
  url=models.URLField()

  def __str__(self):
    return self.user.username

  def save_profile(self):
    self.save()
  
  def delete_profile(self):
    self.delete()

class Projects(models.Model):
  name=models.CharField(max_length=50)
  description=models.TextField()
  project_image=CloudinaryField('project_images')
  urls=models.URLField()
  pub_date=models.DateTimeField(auto_now_add=True)
  profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
  voters = models.IntegerField(default=0)


  def __str__(self):
    return self.name

  def save_project(self):
    self.save()
  
  def delete_project(self):
    self.delete()

  def voters_num(self):
    return self.voters.count()

  @classmethod
  def get_all_projects(cls):
    return cls.objects.all()

  @classmethod
  def get_project(cls,id):
    return Projects.objects.get(id=id)

  @classmethod
  def search_project(cls,name):
    return cls.objects.filter(name__icontains=name)

  @classmethod
  def user_projects(cls,profile):
    return cls.objects.filter(profile=profile)  

class Meta:
  ordering=['-pub_date']

class Ratings(models.Model):
  design = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))))
  usability = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))))
  content = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))))
  rater = models.ForeignKey(Profile,on_delete=models.CASCADE)
  projects=models.ForeignKey(Projects,on_delete=models.CASCADE)
  pub_date=models.DateTimeField(auto_now_add=True)
  design_average=models.FloatField(default=0)
  usability_average=models.FloatField(default=0)
  content_average=models.FloatField(default=0)
  average_rating=models.FloatField(default=0)
  
  def __str__(self):
    return self.projects

  def save_rating(self):
    self.save()
  
  def delete_rating(self):
    self.delete()

  @classmethod
  def project_votes(cls,project):
    return cls.objects.filter(project=project)

  @classmethod
  def project_voters(cls,rater):
    return cls.objects.filter(rater=rater)

  class Meta:
    ordering=['-pub_date']