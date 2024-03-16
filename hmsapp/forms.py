# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django import forms
# # from django.forms import *
# from .models import *

# #to create a form for user creation. This extends in-built User Creation Form of django since we have over ridden Abstarct Base User.
# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)  # Add the email field
#     class Meta:
#         model = User
#         fields = ("userName","password1","password2","email")

# #to create a form for user updation. This extends in-built User Updation Form of django since we have over ridden Abstarct Base User.
# class UserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ("password","is_active","is_staff","is_superuser")


