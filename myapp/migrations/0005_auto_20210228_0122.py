# Generated by Django 3.1.7 on 2021-02-28 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20210228_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='exhibit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='myapp.exhibit'),
        ),
    ]