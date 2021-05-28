from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.forms.fields import EmailField
from .models import Ratings,Profile,Projects
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
  email=forms.EmailField(max_length=254)
  class Meta:
    model = User
    fields=['username','email','password1','password2']

class AddProjectForm(ModelForm):
  class Meta:
    model = Projects
    fields = ['name','description','project_image','urls','']