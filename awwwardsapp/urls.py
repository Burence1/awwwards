from os import name
from django.conf import settings
from django.urls import path,re_path
from django.conf.urls.static import static
from . import views

urlpatterns=[
  path('',views.index,name='home'),
  path('signup/',views.signup,name='signup'),
  path('new_project/',views.new_project,name='new_project'),
  path('search/',views.search_project,name='search'),
  path('project/<int:project_id>/',views.project,name='project'),
  # path('profile/(?P<profile_id>\d+)', views.profile, name='profile'),
  path('profile/<int:profile_id>/',views.profile,name='profile'),
  re_path('update_profile/(?P<profile_id>\d+)',views.update_profile,name='update_profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
