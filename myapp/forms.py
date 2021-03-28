import datetime

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . import models



# class CustomUserCreationForm(UserCreationForm):
    
#     class Meta:
#         model = models.CustomUser
#         fields = UserCreationForm.Meta.fields

# class CustomUserChangeForm(UserChangeForm):
    
#     class Meta:
#         model = models.CustomUser
#         fields = UserCreationForm.Meta.fields

class ExhibitionForm(forms.Form):
    #student = forms.ModelChoiceField(queryset=models.CustomUser.objects.all())
    student = forms.ModelChoiceField(queryset=models.User.objects.all())
    title = forms.CharField(label="Title")
    degree = forms.ChoiceField(
        choices=models.Exhibition.TYPE,
        initial='BFA',
    )
    flyer = forms.ImageField(required=True)
    startDate = forms.DateField(
        label="Start Date",
        required=False,
        initial=datetime.datetime.now
    )
    endDate = forms.DateField(
        label="End Date",
        required=False,
        initial=datetime.datetime.now,
    )
    public = forms.BooleanField(
        initial=False,
        required=False,
    )

    def save(self, request):
        newExhibition = models.Exhibition()
        newExhibition.student = self.cleaned_data["student"]
        newExhibition.title = self.cleaned_data["title"]
        newExhibition.degree = self.cleaned_data["degree"]
        newExhibition.flyer = request.FILES['flyer']
        newExhibition.startDate = self.cleaned_data["startDate"]
        newExhibition.endDate = self.cleaned_data["endDate"]
        return newExhibition

class ExhibitionForm2(ModelForm):
    class Meta:
        model = models.Exhibition
        fields = '__all__'

class ArtForm(forms.Form):
    title = forms.CharField(label="Title")
    exhibition = forms.ModelChoiceField(queryset=models.Exhibition.objects.all())
    image = forms.ImageField(
        required=True
    )

    def save(self, request):
        newArt = models.ArtWork()
        newArt.title = self.cleaned_data("title")
        newArt.exhibition = self.cleaned_data("exhibition")
        newArt.image = request.FILES['image']
        return newArt


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
    )
    first_name = forms.CharField(
        required=True,
        max_length=30,
    )
    last_name = forms.CharField(
        required=True,
        max_length=30,
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name",
                  "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user