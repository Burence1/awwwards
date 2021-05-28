from django import forms
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from .forms import SignupForm
from django.contrib.auth import login, authenticate

# Create your views here.
def index(request):
  return render(request,'index.html',{})

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