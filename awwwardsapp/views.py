from django import forms
from django.contrib.auth import authenticate
from django.core.checks import messages
from django.http.request import HttpHeaders
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from .forms import SignupForm,AddProjectForm,RatingForm,UpdateUserForm,UpdateProfile
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
  project_ratings=projects.order_by('-ratings__average_rating')
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
  return render(request,'/project/new_project.html',{"form":form})

def search_project(request):
  if "project" in request.GET and request.GET["project"]:
    search=request.GET.get("project")
    rated=False
    try:
      project=Projects.search_project(search)
      if len(project)==1:
        single_project=project[0]
        form = RatingForm()
        project_votes=Ratings.project_votes(single_project.id)
        project_voters=single_project.voters
        voters_list=[i.voters for i in project_voters]

        for vote in project_votes:
          current_user=request.user
          try:
            user=User.objects.get(pk=current_user.id)
            profile=Profile.objects.get(user=user)
            voters=Ratings.project_voters(profile)
            rated=False
            if current_user.id in voters_list:
              rated=True
          except Profile.DoesNotExist:
            rated=False
        return render(request,'search/search.html',{"form":form,"single_project":single_project,"rated":rated,"project_votes":project_votes,"project_voters":project_voters})
      elif len(project) >= 2:
        stats=project.count()
        return render(request,"search/all_search.html",{"stats":stats,"project":project})
    except Projects.DoesNotExist:
      all_projects=Projects.get_all_projects()
      message = f"{search} Does not exist"
      return render(request,"search/all_search.html",{"message":message,"all_projects":all_projects})

  else:
    message="No search made"
    return render(request,"search/search.html",{"message":message})

def project(request,project_id):
  project=Projects.objects.get(pk=project_id)
  ratings=Ratings.project_votes(project.id)
  rating_stats=ratings.count()
  current_user=request.user
  rating_status=None
  if rating_status is None:
    rating_status = False
  else:
    rating_status = True

  if request.method == 'POST':
    form = RatingForm(request.POST)
    if form.is_valid():
      new_rating =form.save(commit=False)
      new_rating.rater=current_user
      new_rating.projects=project
      new_rating.save_rating()

      project_ratings=Ratings.objects.get(project)

      content_rating=[i.content for i in project_ratings]
      content_average=sum(content_rating)/len(content_rating)

      design_rating = [i.design for i in project_ratings]
      design_average=sum(design_rating)/len(design_rating)

      usability_rating = [i.usability for i in project_ratings]
      usability_average = sum(usability_rating)/len(usability_rating) 

      average_rating=(content_average + usability_average + design_average)/3  

      new_rating.content_average=round(content_average,2)
      new_rating.design_average=round(design_average,2)
      new_rating.usability_average=round(usability_average,2)
      new_rating.average_rating=round(average_rating,2)
      new_rating.save_rating()
      return render(request,'project/project.html',{"form":form,"project":project,"ratings":ratings,"rating_stats":rating_stats,"rating_status":rating_status})

def profile(request,profile_id):
  try:
    user=User.objects.get(pk=profile_id)
    profile=Profile.objects.get(user=user)
    profile_projects=Projects.user_projects(profile)
    projects_stats=profile_projects.count()
    votes=[i.average_rating for i in profile_projects]
    total_ratings=sum(votes)
    average=total_ratings/len(profile_projects)
  except Profile.DoesNotExist:
    raise Http404()
  return render(request,'profile/profile.html',{"profile":profile,"profile_projects":profile_projects,"projects_stats":projects_stats,"ratings":total_ratings,"average":average})

def update_profile(request,username):
  user=User.objects.get(username=username)
  current_user=request.user
  if request.methos =='POST':
    user_form=UpdateUserForm(request.POST,instance=current_user)
    profile_form=UpdateProfile(request.POST,request.FILES, instance=current_user.profile)
    if user_form.is_valid and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      return redirect('profile',user.username)
  else:
    user_form=UpdateUserForm(instance=current_user)
    update_profile=UpdateProfile(instance=current_user.profile)
  
  return render(request,"profile/updateprof.html",{"user_form":user_form,"update_profile":update_profile})