from django.contrib.auth.models import User
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
    mode = Ratings
    fields = ['design','usability','content']

class UpdateUserForm(ModelForm):
  email = forms.EmailField(max_length=254)
  class Meta:
    model = Profile
    fields = ['username', 'email']
