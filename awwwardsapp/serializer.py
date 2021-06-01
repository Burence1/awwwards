from django.db import models
from django.db.models import fields
from .models import Profile,Projects
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('id','user','profile_pic','bio','email','url','location')

class ProjectsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Projects
    fields=('id','name','description','project_image','urls','pub_date')