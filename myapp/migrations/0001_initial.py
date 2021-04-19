# Generated by Django 3.1.7 on 2021-03-20 21:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import myapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exhibition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('degree', models.CharField(choices=[('B', 'BFA'), ('M', 'MFA')], default='B', max_length=1)),
                ('public', models.BooleanField(default=False)),
                ('flyer', models.ImageField(blank=True, null=True, upload_to=myapp.models.exhibitionImagePath)),
                ('startDate', models.DateField(default=datetime.datetime.now)),
                ('endDate', models.DateField(default=datetime.datetime.now)),
                ('artistStatement', models.TextField(blank=True, null=True)),
                ('student', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArtWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to=myapp.models.artImagePath)),
                ('exhibition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.exhibition')),
            ],
        ),
    ]
