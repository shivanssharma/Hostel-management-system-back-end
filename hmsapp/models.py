#from django.db import models

# Create your models here.
#from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     # Inherits from AbstractUser and extends it with a primary key field
#     username = models.CharField(max_length=100, primary_key=True)



# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin           
# from django.contrib.auth.hashers import make_password
from django.db import models

# from hmsDjango.settings import AUTH_USER_MODEL

# class CustomUserManager(BaseUserManager):
#     def _create_any_user(self,userName,is_superuser,password,is_staff,is_active):
       
#         if not userName:
#             raise ValueError(("Not a valid userID"))
#         user = self.model(
#             userName=userName,
#             is_superuser=is_superuser,
#             is_staff=is_staff,
#             is_active=is_active
#         )
#         user.set_password(password)
#         user.save()
#         return user

#     #this func calls above func to create account for a normal user
#     def create_regular_user(self, userName,password):
#         return self._create_any_user(userName,False,password,False,True)
    
#     #this func is to create account for a superuser.
#     def create_superuser(self, userName, password):
#         return self._create_any_user(userName,True,password,True,True)
# class CustomUserManager(BaseUserManager):
#     def create_user(self, userName, password=None, email=None, **extra_fields):
#         if not userName:
#             raise ValueError('The username field must be set')
#         user = self.model(userName=userName, email=email, **extra_fields)
#         if password:
#             user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, userName, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
        
#         return self.create_user(userName, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     # id = models.AutoField(primary_key=True)
#     userName = models.CharField(primary_key=True,max_length=100, unique=True)
#     password = models.CharField(max_length=128)  # Adjusted for password hashing
#     email = models.EmailField(blank=True, null=True, unique=True)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)

#     USERNAME_FIELD = 'userName'
#     REQUIRED_FIELDS = []  # Specify required fields

#     objects = CustomUserManager()  # Activated custom user manager

#     def save(self, *args, **kwargs):
#         self.password = make_password(self.password)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.userName

from django.contrib.auth.models import User


class Student(models.Model):

    RegistrationNumber = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    CourseName = models.CharField(max_length=100)
    DateOfJoining = models.DateField()
    FatherName = models.CharField(max_length=100)
    MotherName = models.CharField(max_length=100)
    DateOfBirth = models.DateField()
    EmailID = models.EmailField(max_length=100)
    Address = models.CharField(max_length=100)
    is_Room=models.BooleanField(default=False)
    MobileNumber=models.IntegerField()


class Room(models.Model):
    RoomID = models.AutoField(primary_key=True)
    RegistrationNumber = models.ManyToManyField(Student)
    FloorNumber = models.CharField(max_length=100)
    RoomNumber = models.CharField(max_length=100)
    roomLeader = models.BooleanField(default=False)
    

class Electronics(models.Model):
    RegistrationNumber = models.ForeignKey(Student, on_delete=models.CASCADE)
    mobilePhone = models.BooleanField()
    laptop = models.BooleanField()
    earphone = models.BooleanField()
    kindle = models.BooleanField()

class NecessityStoreItem(models.Model):
    ItemID = models.AutoField(primary_key=True)
    ItemName = models.CharField(max_length=100)
    ItemDescription = models.CharField(max_length=100)
    ItemPrice = models.IntegerField()
    ItemImage = models.ImageField(upload_to='static/images')

class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    RegistrationNumber = models.ForeignKey(Student, on_delete=models.CASCADE)
    ItemID = models.ForeignKey(NecessityStoreItem, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    # totalPrice = models.IntegerField()
    OrderDate = models.DateTimeField()

# class RoomLeader(models.Model):
#     RoomLeaderID = models.AutoField(primary_key=True)
#     RegistrationNumber = models.ForeignKey(Student, on_delete=models.CASCADE)
#     RoomNumber =models.IntegerField()
#     FloorNumber= models.CharField(max_length=100)

class Medicine(models.Model):
    MedicineID = models.AutoField(primary_key=True)
    MedicineName = models.CharField(max_length=100)
    Uses = models.CharField(max_length=100)
    SideEffects = models.CharField(max_length=100)
    Dosage = models.CharField(max_length=100)

class Ailment(models.Model):
    AilmentID = models.AutoField(primary_key=True)
    AilmentName = models.CharField(max_length=100)
    AilmentDescription = models.CharField(max_length=100)
    MedicineID = models.ForeignKey(Medicine, on_delete=models.CASCADE)

class Hospital(models.Model):
    HospitalID = models.AutoField(primary_key=True)
    HospitalName = models.CharField(max_length=100)
    hospitalType = models.CharField(max_length=100)

class Department(models.Model):
    departmentID = models.AutoField(primary_key=True)
    HospitalID = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    departmentName = models.CharField(max_length=100)

class HospitalVisit(models.Model):
    VisitID = models.AutoField(primary_key=True)
    RegistrationNumber = models.ForeignKey(Student, on_delete=models.CASCADE)
    HospitalID = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    Purpose = models.CharField(max_length=100)
    VisitDate = models.DateTimeField()

class HostelAsset(models.Model):
    AssetID = models.AutoField(primary_key=True)
    AssetName = models.CharField(max_length=100)
    Description = models.CharField(max_length=100)
    AvailabilityStatus = models.BooleanField()

class Reservation(models.Model):
    ReservationID = models.AutoField(primary_key=True)
    RegistrationNumber = models.ForeignKey(Student, on_delete=models.CASCADE)
    AssetID = models.ForeignKey(HostelAsset, on_delete=models.CASCADE)
    ReservationDate = models.DateTimeField()

class HealthRecord(models.Model):
    healthId = models.AutoField(primary_key=True)
    RegistrationNumber = models.ForeignKey(Student, on_delete=models.CASCADE)
    AilmentID = models.ForeignKey(Ailment, on_delete=models.CASCADE)
    Description = models.CharField(max_length=100)
    diagnosis = models.CharField(max_length=100)
    date = models.DateTimeField()
    VisitID = models.ForeignKey(HospitalVisit, on_delete=models.CASCADE)    