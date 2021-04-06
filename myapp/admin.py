from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
#from .forms import CustomUserChangeForm, CustomUserCreationForm
from . import models

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = models.CustomUser
#     list_display = [
#         'email',
#         'username',
#         'first_name',
#         'last_name',
#         'is_active',
#     ]
#     fieldsets = UserAdmin.fieldsets
#     add_fieldsets = UserAdmin.add_fieldsets

# admin.site.register(models.CustomUser, CustomUserAdmin)

# Register your models here.
admin.site.register(models.ArtWork)
admin.site.register(models.Exhibition)
admin.site.register(models.Category)
admin.site.register(models.Mentor)
