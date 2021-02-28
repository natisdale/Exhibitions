from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


# adapated from https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.FileField.upload_to
def userDirectoryPath(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

def getRequestUser(request):
    return request.user.id

def getUserExhibit(instance):
    return models.Exhibit.objects.filter(user=instance.user).first()

class Exhibit(models.Model):
    title = models.CharField(max_length=150)
    user = models.ForeignKey(
        User,
        default = models.ForeignKey(User, default=getRequestUser, on_delete=models.PROTECT),
        blank = False,
        null = False,
        on_delete=models.PROTECT)
    image = models.ImageField(upload_to=userDirectoryPath)
    startDate = models.DateField(
        auto_now=False,
        auto_now_add=False,
        default=datetime.now,
    )
    endDate = models.DateField(
        auto_now=False,
        auto_now_add=False,
        default=datetime.now
    )
    artistStatement = models.TextField()

    def _str_(self):
        return self.title

class ArtWork(models.Model):
    title = models.CharField(max_length=150)
    user = models.ForeignKey(
        User,
        default = models.ForeignKey(
            User,
            default=getRequestUser,
            on_delete=models.PROTECT),
        blank = False,
        null = False,
        on_delete=models.PROTECT)
    exhibit = models.ForeignKey(
        Exhibit,
        default=1,
        on_delete=models.PROTECT)
    image = models.ImageField(upload_to=userDirectoryPath)
    
    def __str__(self):
        return self.title
