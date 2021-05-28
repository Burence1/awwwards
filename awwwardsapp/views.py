from django import forms
from django.contrib.auth import authenticate
from django.http.response import Http404
from django.shortcuts import redirect, render
from .forms import SignupForm,AddProjectForm
from django.contrib.auth import login, authenticate
from .models import Profile,Projects,Ratings
from django.core.exceptions import ObjectDoesNotExist
import datetime as dt
from django.contrib.auth.models import User

# Create your views here.
def index(request):
  date=dt.date.today()
  try:
    projects=Projects.get_all_projects()
  except Projects.DoesNotExist:
    raise Http404()
  project_ratings=projects.order_by('ratings__average_rating')
  best_rating=None
  best_votes=None
  if len(project_ratings)>=1:
    best_rating=project_ratings[0]
    ratings=Ratings.project_votes(best_rating.id)
    best_votes=ratings[:3]
  return render(request,'index.html',{"date":date,"highest_vote":best_votes,"ratings":ratings,"projects":projects})

def signup(request):
  if request.method =='POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      form.save()
      username=form.cleaned_data.get('username')
      first_password=form.cleaned_data.get('password1')

      user=authenticate(username=username,password=first_password)
      login(request,user)
      return redirect('home')
  else:
    form=SignupForm()
  return render(request,'registration/registration.html',{"form":form})

def new_project(request):
  if request.method == "POST":
    form = AddProjectForm(request.POST,request.FILES)
    user=request.user
    try:
      profile=Profile.objects.get(user=user)
    except Profile.DoesNotExist:
      raise Http404()
    if form.is_valid():
      added_project=form.save(commit=False)
      added_project.profile = profile
      added_project.save()
    return redirect('home')
  else:
    form=AddProjectForm()
  return render(request,'new_project.html',{"form":form})