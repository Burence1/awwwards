# Generated by Django 3.2.3 on 2021-05-28 12:11

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', cloudinary.models.CloudinaryField(max_length=255, verbose_name='photo')),
                ('bio', models.TextField()),
                ('location', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('url', models.URLField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('project_image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='project_images')),
                ('urls', models.URLField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('voters', models.IntegerField(default=0)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='awwwardsapp.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('design', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0)),
                ('usability', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0)),
                ('content', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('design_average', models.FloatField(default=0)),
                ('usability_average', models.FloatField(default=0)),
                ('content_average', models.FloatField(default=0)),
                ('average_rating', models.FloatField(default=0)),
                ('projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='awwwardsapp.projects')),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='awwwardsapp.profile')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
    ]