from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
  user=models.OneToOneField(User,on_delete=CASCADE, related_name='profile')
  profile_pic=CloudinaryField('photo')
  bio=models.TextField()
  location=models.CharField(max_length=50)
  email=models.EmailField()
  url=models.URLField()

  def __str__(self):
    return self.user.username