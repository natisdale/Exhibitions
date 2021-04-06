from datetime import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth.models import AbstractUser, BaseUserManager


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')
                
#         user = self.model(
#             email=self.normalize_email(email),
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None):
#         user = self.create_user(
#             username=username,
#             email=self.normalize_email(email),
#             password=password,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.username

# image path functions adapated from
# https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.FileField.upload_to
def exhibitionImagePath(instance, filename):
    return 'student_{0}/{1}'.format(instance.student.id, filename)


def artImagePath(instance, filename):
    return 'student_{0}/{1}'.format(instance.exhibition.student.id, filename)


def getRequestUser(request):
    return request.user.id


def getUserExhibition(instance):
    return Exhibition.objects.filter(user=instance.user).first()


class Mentor(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=40)

    def __str__(self):
        return self.lastName + ', ' + self.firstName

class Category(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Exhibition(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=150)
    BFA = 'B'
    MFA = 'M'
    TYPE = [
        (BFA, 'BFA'),
        (MFA, 'MFA'),
    ]
    degree = models.CharField(
        max_length=1,
        choices=TYPE,
        default=BFA,
    )
    public = models.BooleanField(default=False)
    flyer = models.ImageField(
        upload_to=exhibitionImagePath,
        blank=True,
        null=True,)
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
    artistStatement = models.TextField(
        blank=True,
        null=True,
    )
    mentors = models.ManyToManyField(Mentor)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class ArtWork(models.Model):
    title = models.CharField(max_length=150)
    exhibition = models.ForeignKey(
        Exhibition,
        on_delete=models.CASCADE,
        null=True,
    )
    image = models.ImageField(upload_to=artImagePath)

    def __str__(self):
        return self.title
