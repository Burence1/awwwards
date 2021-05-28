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


class Projects(models.Model):
  name=models.CharField(max_length=50)
  description=models.TextField()
  project_image=CloudinaryField('project_images')
  urls=models.URLField()
  pub_date=models.DateTimeField(auto_now_add=True)
  profile=models.ForeignKey(Profile,on_delete=models.CASCADE)

def __str__(self):
  return self.name

class Meta:
  ordering=['-pub_date']

class Ratings(models.Model):
  design = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))),default=0)
  usability = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))),default=0)
  content = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))),default=0)
  rater = models.ForeignKey(Profile,on_delete=models.CASCADE)
  projects=models.ForeignKey(Projects,on_delete=models.CASCADE)
  pub_date=models.DateTimeField(auto_now_add=True)
  design_average=models.FloatField(default=0)
  usability_average=models.FloatField(default=0)
  content_average=models.FloatField(default=0)
  average_rating=models.FloatField(default=0)

  def __str__(self):
    return self.projects

  class Meta:
    ordering=['-pub_date']