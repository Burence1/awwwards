from django.contrib import admin
from .models import Projects,Profile,Ratings

# Register your models here.
admin.site.register(Profile)
admin.site.register(Projects)
admin.site.register(Ratings)