from django.contrib.auth.models import User
from django.db.models import fields
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
    fields = ['name','description','project_image','urls']

class RatingForm(ModelForm):
  class Meta:
    model = Ratings
    fields = ['design','usability','content']

class UpdateUserForm(ModelForm):
  email = forms.EmailField(max_length=254)
  class Meta:
    model = User
    fields = ['username', 'email']

class UpdateProfile(ModelForm):
  class Meta:
    model = Profile
    fields = ['location','profile_pic','bio','email']