# Generated by Django 3.2.3 on 2021-05-28 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awwwardsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratings',
            name='content',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]),
        ),
        migrations.AlterField(
            model_name='ratings',
            name='design',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]),
        ),
        migrations.AlterField(
            model_name='ratings',
            name='usability',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]),
        ),
    ]
