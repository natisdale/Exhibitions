# Generated by Django 3.1.7 on 2021-02-28 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0005_auto_20210228_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibit',
            name='mfa',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(default='https://www.linkedin.com')),
                ('mentor', models.ManyToManyField(to='myapp.Artist')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
