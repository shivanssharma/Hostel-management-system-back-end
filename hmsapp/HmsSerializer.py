from rest_framework import serializers 
from hmsapp.models import *
from django.contrib.auth.models import User
 
# class UserRegistrationSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True)  # Add the email field

#     class Meta:
#         model = User
#         fields = ('userName', 'password1', 'password2', 'email')

#     def create(self, validated_data):
#         # Custom create method to handle password hashing
#         user = User.objects.create_user(
#             username=validated_data['userName'],
#             password=validated_data['password1'],
#             email=validated_data['email']
#         )
#         return user

# class UserChangeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('password', 'is_active', 'is_staff', 'is_superuser')

# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(style={'input_type': 'password'})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_superuser', 'is_active']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    #student = StudentSerializer(many=True,read_only=True)
    class Meta:
        model = Room
        fields = '__all__'


class AilmentSerializer(serializers.ModelSerializer):
    #student = StudentSerializer(many=True,read_only=True)
    class Meta:
        model = Ailment
        fields = '__all__'        

class MedicineSerializer(serializers.ModelSerializer):
    #student = StudentSerializer(many=True,read_only=True)
    class Meta:
        model = Medicine
        fields = '__all__'        

class NecessityStoreItemSerializer(serializers.ModelSerializer):
    #student = StudentSerializer(many=True,read_only=True)
    class Meta:
        model = NecessityStoreItem
        fields = '__all__'         

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'          
class HostelAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelAsset
        fields = '__all__'

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'        


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'          

class HospitalVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalVisit
        fields = '__all__'          

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'  