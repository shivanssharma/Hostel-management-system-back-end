from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .models import User
# from .forms import UserCreationForm, UserChangeForm

# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .HmsSerializer import UserRegistrationSerializer, UserChangeSerializer

# class DRFUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('userName', 'password1', 'password2', 'email')

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         serializer = UserRegistrationSerializer(data=self.cleaned_data)
#         if serializer.is_valid():
#             user = serializer.save()
#         if commit:
#             user.save()
#         return user

# class DRFUserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('password', 'is_active', 'is_staff', 'is_superuser')

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         serializer = UserChangeSerializer(user, data=self.cleaned_data)
#         if serializer.is_valid():
#             user = serializer.save()
#         if commit:
#             user.save()
#         return user
# class CustomUserAdmin(UserAdmin):
#     add_form = DRFUserCreationForm
#     form = DRFUserChangeForm
#     model = User
#     list_display = ['userName', 'is_staff', 'is_superuser']
#     ordering = ['userName']
    
#     fieldsets = (
#         (None, {'fields': ('userName', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('userName', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')}
#         ),
#     )

# admin.site.register(User, CustomUserAdmin)

# class CustomUserAdmin(UserAdmin):
#     add_form = UserCreationForm
#     form = UserChangeForm
#     model = User
#     list_display = ['userName', 'is_staff', 'is_superuser']
#     ordering = ['userName']
    
#     fieldsets = (
#         (None, {'fields': ('userName', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('userName', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')}
#         ),
#     )

# admin.site.register(User, CustomUserAdmin)

# Register your models here.
# from django.contrib import admin
# from django.contrib.auth.models import User
# admin.site.register(User),
admin.site.register(Student),
# admin.site.register(User)
#admin.site.register(Admin)
admin.site.register(Room),
admin.site.register(Ailment),
admin.site.register(Medicine),
admin.site.register(HostelAsset),
admin.site.register(NecessityStoreItem),
admin.site.register(Hospital),
admin.site.register(HealthRecord),
admin.site.register(Department),

