from os import name
from django.conf import settings
from django.urls import path,re_path
from . import views

urlpatterns=[
  path('',views.index,name='home'),
]