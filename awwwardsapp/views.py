from django import forms
from django.contrib.auth import authenticate
from django.core.checks import messages
from django.http import response
from django.http.request import HttpHeaders
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from rest_framework import serializers
from .forms import SignupForm,AddProjectForm,RatingForm,UpdateUserForm,UpdateProfile
from django.contrib.auth import login, authenticate
from .models import Profile,Projects,Ratings
from django.core.exceptions import ObjectDoesNotExist
import datetime as dt
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import statistics
from django.urls import reverse
from .email import send_welcome_email
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectsSerializer
from awwwardsapp import serializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# Create your views here.


@login_required
def welcome_mail(request):
  user = request.user
  email = user.email
  name = user.username
  send_welcome_email(name, email)
  return redirect(index)

@login_required
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
  return render(request,'index.html',{"date":date,"highest_vote":best_votes,"projects":projects,"highest_rating":best_rating})


def signup(request):
  if request.method =='POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      form.save()
      username=form.cleaned_data.get('username')
      first_password=form.cleaned_data.get('password1')

      user=authenticate(username=username,password=first_password)
      login(request,user)
      return redirect('welcome')
  else:
    form=SignupForm()
  return render(request,'registration/registration.html',{"form":form})

@login_required
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
  return render(request,'project/new_project.html',{"form":form})

@login_required
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
        project_voters=single_project
        voters_lists=Ratings.project_voters(single_project.id)
        ratings = Ratings.project_votes(single_project.id)
        voters_list=[i.rater for i in voters_lists]

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
        
        project = Projects.objects.get(name=search)
        ratings = Ratings.project_votes(project.id)
        rating_stats = ratings.count()
        form = RatingForm()
        current_user = request.user
        profile = Profile.objects.get(user=current_user)
        rating_status = None
        raters = []
        project_average = []
        content_list = []
        design_list = []
        usability_list = []
        for rate in ratings:
          raters.append(rate.rater.id)
          sum_average = rate.usability + rate.design + rate.content
          average = sum_average/3
          project_average.append(average)
          content_list.append(rate.content)
          usability_list.append(rate.usability)
          design_list.append(rate.design)
          try:
            user = User.objects.get(pk=request.user.id)
            profile = Profile.objects.get(user=user)
            rater = Ratings.project_voters(profile)
            rating_status = False
            if request.user.id in raters:
              rating_status = True
          except Profile.DoesNotExist:
            rating_status = False

        average_rating = 0
        design_average = 0
        usability_average = 0
        content_average = 0
        if len(project_average) > 0:
          average_rating = sum(project_average)/len(project_average)
          project.average_rating = round(average_rating, 2)
          project.save()
        if rating_stats != 0:
          usability_average = sum(usability_list)/rating_stats
          content_average = sum(content_list)/rating_stats
          design_average = sum(design_list)/rating_stats
          project.usability_average = round(usability_average, 2)
          project.content_average = round(content_average, 2)
          project.design_average = round(design_average, 2)
          project.save()

        return render(request,'search/search.html',{"projects":project,"ratings":ratings,"form":form,"project":single_project,"rating_status":rated,"project_votes":project_votes,"project_voters":project_voters,"voters":voters})
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

@login_required
def profile(request,profile_id):
  try:
    user=User.objects.get(pk=profile_id)
    profile=Profile.objects.get(user=user)
    profile_projects=Projects.user_projects(profile)
    projects_stats=profile_projects.count()
    project_ratings = Ratings.objects.filter(projects=profile_projects.first())
    if len(project_ratings) >= 1:
      votes=[i.average_rating for i in project_ratings]
      total_ratings=sum(votes)
      average=total_ratings/len(profile_projects)
      return render(request,'profile/profile.html',{"profile":profile,"profile_projects":profile_projects,"projects_stats":projects_stats,"ratings":total_ratings,"average":average})
  except Profile.DoesNotExist:
    raise Http404()
  return render(request,'profile/profile.html',{"profile":profile,"profile_projects":profile_projects,"projects_stats":projects_stats})

@login_required
def update_profile(request,profile_id):
  user=User.objects.get(pk=profile_id)
  current_user=request.user
  if request.method =='POST':
    user_form=UpdateUserForm(request.POST,instance=current_user)
    profile_form=UpdateProfile(request.POST,request.FILES, instance=current_user.profile)
    if user_form.is_valid and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      return redirect('profile',user.pk)
  else:
    user_form=UpdateUserForm(instance=current_user)
    update_profile=UpdateProfile(instance=current_user.profile)
  
  return render(request,"profile/updateprof.html",{"user_form":user_form,"update_profile":update_profile})


@login_required
def project(request, project_id):
  project = Projects.objects.get(pk=project_id)
  ratings = Ratings.project_votes(project.id)
  rating_stats = ratings.count()
  form = RatingForm()
  current_user=request.user
  profile = Profile.objects.get(user=current_user)
  rating_status = None
  raters = []
  project_average = []
  content_list = []
  design_list = []
  usability_list = []
  for rate in ratings:
    raters.append(rate.rater.id)
    sum_average = rate.usability + rate.design + rate.content
    average = sum_average/3
    project_average.append(average)
    content_list.append(rate.content)
    usability_list.append(rate.usability)
    design_list.append(rate.design)
    try:
      user=User.objects.get(pk=request.user.id)
      profile=Profile.objects.get(user=user)
      rater =Ratings.project_voters(profile)
      rating_status=False
      if request.user.id in raters:
        rating_status=True
    except Profile.DoesNotExist:
      rating_status=False
  
  average_rating=0
  design_average=0
  usability_average=0
  content_average=0
  if len(project_average) > 0:
    average_rating=sum(project_average)/len(project_average)
    project.average_rating=round(average_rating,2)
    project.save()
  if rating_stats != 0:
    usability_average=sum(usability_list)/rating_stats
    content_average=sum(content_list)/rating_stats
    design_average=sum(design_list)/rating_stats
    project.usability_average=round(usability_average,2)
    project.content_average=round(content_average,2)
    project.design_average=round(design_average,2)
    project.save()

  return render(request, 'project/project.html', {"form":form,"project": project, "ratings": ratings, "rating_stats": rating_stats, "rated": rating_status})


@login_required
def rate_project(request, project_id):
  if request.method == "POST":
    form = RatingForm(request.POST)
    project = Projects.objects.get(pk=project_id)
    current_user = request.user
    try:
        user = User.objects.get(pk=current_user.id)
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        raise Http404()
    if form.is_valid():
      ratings = form.save(commit=False)
      ratings.rater = profile
      ratings.projects = project
      ratings.save()
      return HttpResponseRedirect(reverse('project', args=[int(project.id)]))
  else:
      form = RatingForm()
  return render(request, 'project/project.html', {"form": form})

#class-based developed api end-points
class ProfileList(APIView):
  def get(self,request,format=None):
    profiles=Profile.objects.all()
    serializers=ProfileSerializer(profiles,many=True)
    return Response(serializers.data)

class ProjectsList(APIView):
  def get(self,request,format=None):
    projects=Projects.objects.all()
    serializers=ProjectsSerializer(projects,many=True)
    return Response(serializers.data)
#end of class based api-endpoints


#function based api-endpoints
@api_view(['GET'])
@csrf_exempt
def ProfilesList(request):
  if request.method == 'GET':
    profiles=Profile.objects.all()
    serializers=ProfileSerializer(profiles,many=True)
    return Response(serializers.data)

@api_view(['GET'])
@csrf_exempt
def ProjectList(request):
  if request.method == 'GET':
    projects=Projects.objects.all()
    serializers=ProjectsSerializer(projects,many=True)
    return Response(serializers.data)
#end of funtion-based api-endpoints