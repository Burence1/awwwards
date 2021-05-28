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
