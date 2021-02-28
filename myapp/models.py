from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


# adapated from
# https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.FileField.upload_to
def userDirectoryPath(instance, filename):
    return 'user_{0}/{1}'.format(instance.artist.user.id, filename)


def getRequestUser(request):
    return request.user.id


def getUserExhibit(instance):
    return Exhibit.objects.filter(user=instance.user).first()


class Artist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )
    url = models.URLField(default='https://www.linkedin.com')
    mentorship = models.ManyToManyField(
        "self",
        blank=True
    )

    def _str_(self):
        return self.user.username


class Exhibit(models.Model):
    title = models.CharField(max_length=150)
    artist = models.ForeignKey(
        Artist,
        blank=False,
        null=True,
        on_delete=models.PROTECT,
    )
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
    mfa = models.BooleanField(default=False)

    def _str_(self):
        return str(self.title)


class ArtWork(models.Model):
    title = models.CharField(max_length=150)
    artist = models.ForeignKey(
        Artist,
        blank=False,
        null=True,
        on_delete=models.PROTECT,
    )
    exhibit = models.ForeignKey(
        Exhibit,
        default=1,
        on_delete=models.PROTECT
    )
    image = models.ImageField(upload_to=userDirectoryPath)

    def __str__(self):
        return self.title
