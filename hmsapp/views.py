from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Room,Student,Ailment,Medicine,HostelAsset,NecessityStoreItem,HealthRecord # Assuming Room is the model you're working with
import json
from django.views.decorators.csrf import csrf_exempt
from .HmsSerializer import *
from rest_framework.views import APIView 
from rest_framework import generics
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


#-----------------------for room------------------------
def get_room_list(request, floor_type, room_type):
    
    if request.method == 'GET':
            rooms = Room.objects.filter(FloorNumber=floor_type, RoomNumber=room_type)
            student_first_names = [room.RegistrationNumber.FirstName for room in rooms]
            # student_first_names = rooms
            return JsonResponse(student_first_names, safe=False)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)




def get_students_by_room_type(request, course_type):
    students = Student.objects.filter(CourseName=course_type).values_list('FirstName', flat=True)
    return JsonResponse(list(students), safe=False)    



#---------------------------Hospital----------------------------------
def medicines(request):
    students = Student.objects.filter(CourseName="3 ug").values_list('FirstName', flat=True)
    print(list(students))   
    return JsonResponse(list(students), safe=False)    
 
def ailment_suggestion(request, ailment_name):
    if request.method == 'GET':
        try:
            ailment = Ailment.objects.get(AilmentName=ailment_name)
            medicine_id = ailment.MedicineID_id  # Assuming MedicineID is the ForeignKey field
            medicines = Medicine.objects.filter(MedicineID=medicine_id)
            medicine_names = medicines.values_list('MedicineName', flat=True)
            return JsonResponse(list(medicine_names), safe=False)
        except Ailment.DoesNotExist:
            return JsonResponse({"error": "Ailment not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"})
    
     
#------------------------------For switch in assets----------------------
def get_switch_value(request):
        switch_instance = HostelAsset.objects.first()  # Assuming SwitchModel is your model
        switch_value = switch_instance.AvailabilityStatus  # Assuming you have a field called 'value' in your model
        return JsonResponse({'AvailabilityStatus': switch_value})


#-----------------------------------registration-----------------------------


class form_data(generics.CreateAPIView):
    queryset = Student.objects.all()
    print(queryset)
    serializer_class = StudentSerializer    

#-----------------------------for saving the room----------------------------------------
    
from django.shortcuts import get_object_or_404

@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        right_list = data.get('rightList', [])
        selected_floor = data.get('selectedFloor', None)
        selected_room = data.get('selectedRoom', None)
        selected_position = data.get('selectedPosition', None)

        if not (selected_floor and selected_room and selected_position):
            return JsonResponse({'error': 'Incomplete data provided'}, status=400)

        students = Student.objects.filter(FirstName__in=right_list)

        for student in students:
            room = Room.objects.create(
                RegistrationNumber=student,
                FloorNumber=selected_floor,
                RoomNumber=selected_room,
                roomLeader=(student.FirstName in right_list and selected_position == "room leader")
            )

        return JsonResponse({'message': 'Room data saved successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)   
# from django.db import IntegrityError

# @csrf_exempt
# def save_data(request):
#     print(request.body)
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))

#         right_list = data.get('rightList', [])
#         selected_floor = data.get('selectedFloor', None)
#         selected_room = data.get('selectedRoom', None)
#         selected_position = data.get('selectedPosition', None)

#         if not (selected_floor and selected_room and selected_position):
#             return JsonResponse({'error': 'Incomplete data provided'}, status=400)

#         students = Student.objects.filter(FirstName__in=right_list)
#         print(students)
#         try:
#             # Check if room already exists for the provided details
#             existing_room = Room.objects.get(
#                 RegistrationNumber__in=students,
#                 FloorNumber=selected_floor,
#                 RoomNumber=selected_room
#             )

#             if existing_room:
#                 return JsonResponse({'error': 'Room already exists'}, status=400)
            
#             # Create room if it doesn't exist
#             room = Room.objects.create(
#                 FloorNumber=selected_floor,
#                 RoomNumber=selected_room
#             )
#             for student in students:
#                 room.RegistrationNumber.add(student)
#             room.roomLeader = any(student.FirstName in right_list and selected_position == "room leader" for student in students)
#             room.save()
#         except IntegrityError:
#             return JsonResponse({'error': 'Failed to save data. Integrity error occurred.'}, status=500)


    
#for room component

def get_student_list(request, floor_number, room_number):
    print(request)
    try:
        rooms = Room.objects.filter(FloorNumber=floor_number, RoomNumber=room_number)
        print(rooms)
    except Room.DoesNotExist:
        return JsonResponse("Room not found", status=404)
    print('here')
    student_list = []
    for room in rooms:
        students = room.RegistrationNumber      #.all()
        # for student in students:
        if students:
            student_list.append({
                'FirstName': students.FirstName,
                'LastName': students.LastName,
                'CourseName': students.CourseName,
            })
    print(student_list)
    return JsonResponse(student_list, safe=False)

#this is for student room for student pannel
def get_student_list_pannel(request, floor_number, room_number):
    print(request)
    try:
        rooms = Room.objects.filter(FloorNumber=floor_number, RoomNumber=room_number)
        print(rooms)
    except Room.DoesNotExist:
        return JsonResponse("Room not found", status=404)
    print('here')
    student_list = []
    for room in rooms:
        students = room.RegistrationNumber      #.all()
        # for student in students:
        if students:
            student_list.append({
                'FirstName': students.FirstName,
                'LastName': students.LastName,
                'CourseName': students.CourseName,
            })
    print(student_list)
    return JsonResponse(student_list, safe=False)


#--------------------------------stores but not in use for now-------------------------------
import base64

def get_items(request):
    items = NecessityStoreItem.objects.all()
    items_data = []
    
    for item in items:
        item_data = {
            'ItemName': item.ItemName,
            'ItemDescription': item.ItemDescription,
            'ItemPrice': item.ItemPrice,
            'ItemImage': None
        }
        
        if item.ItemImage:
            with open(item.ItemImage.path, "rb") as img_file:
                item_data['ItemImage'] = base64.b64encode(img_file.read()).decode('utf-8')
        
        items_data.append(item_data)
    
    return JsonResponse(items_data, safe=False)



#----------------------------------------------------------------------------------------
#this is for admin store page

def get_admin_store(request,course_name):
    print(request)
    if request.method == 'GET':
        students = Student.objects.filter(CourseName=course_name)
        student_data = []
        for student in students:
            student_data.append({
                'RegistrationNumber': student.RegistrationNumber,
                # 'userName': student.userName.username,
                'FirstName': student.FirstName,
                'LastName': student.LastName,
                'CourseName': student.CourseName,
                'DateOfJoining': student.DateOfJoining,
                'FatherName': student.FatherName,
                'MotherName': student.MotherName,
                'DateOfBirth': student.DateOfBirth,
                'EmailID': student.EmailID,
                'Address': student.Address,
                'roomLeader': student.roomLeader,
            })
        return JsonResponse(student_data, safe=False)
#-------------------------------deleting student in user manager --------------------------------
@csrf_exempt
def delete_student(request):
    if request.method == 'POST':
        student_data = request.POST  # You may need to adjust this depending on how the data is sent
        registration_number = student_data.get('RegistrationNumber')
        try:
            student = Student.objects.get(RegistrationNumber=registration_number)
            student.delete()
            return JsonResponse({'message': 'Student deleted successfully'})
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)




#------------------------------this is for login----------------------------------------------


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            if not (username and password):  # Check if username and password are provided
                return JsonResponse({'error': 'Username and password are required'}, status=400)
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'username': user.username,
                    'is_superuser': user.is_superuser,
                    'is_staff': user.is_staff,
                    'is_active': user.is_active,
                })
            else:
                return JsonResponse({'error': 'Invalid username or password'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400) 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def signup(request):
    print(request.body)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('newpassword')
            confirm_password = data.get('confirmpassword')
            print(username,password,confirm_password)
            # Check if passwords match
            if password != confirm_password:
                return JsonResponse({'error': 'Passwords do not match'}, status=400)

            # Add validation and error handling as needed
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'message': 'Signup successful'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


#-------------------------------admin manage view------------------------------
def get_all_usernames(request):
    users = User.objects.all()
    usernames = [user.username for user in users]
    return JsonResponse({'usernames': usernames})       


#-------------------------------- in user manager in admin-------------------------------------
# @csrf_exempt
# @login_required
# @require_POST
# def change_password(request):
#     print(request.username)
#     form = PasswordChangeForm(request.user, request.POST)
#     if form.is_valid():
#         user = form.save()
#         update_session_auth_hash(request, user)  # Important to update the session hash
#         return JsonResponse({'message': 'Password changed successfully.'})
#     else:
#         return JsonResponse({'error': form.errors}, status=400)

@csrf_exempt
def delete_user(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)

@csrf_exempt
def password_reset(request):
    if request.method == 'POST':
        # Parse JSON data from request body
        data = json.loads(request.body)
        
        # Extract username and new password from parsed JSON data
        username = data.get('username')
        new_password = data.get('newPassword')
        
        # Check if the username exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

        # Set the new password
        user.set_password(new_password)
        user.save()

        return JsonResponse({'message': 'Password reset successfully'})
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


#this is for status of user
# views.py



@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_user_status(request, username):
    try:
        user = User.objects.get(username=username)
        user.is_superuser = request.data.get('is_superuser', user.is_superuser)
        user.is_staff = request.data.get('is_staff', user.is_staff)
        user.is_active = request.data.get('is_active', user.is_active)
        user.save()
        return Response({'message': 'User status updated successfully.'})
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)
    
#------------------------------------------------------------------------------------
class AilmentListCreateView(generics.ListCreateAPIView):
    queryset = Ailment.objects.all()
    serializer_class = AilmentSerializer


@api_view(['DELETE'])
def delete_ailment_by_name(request, name):
    try:
        ailment = Ailment.objects.get(AilmentName=name)
        ailment.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)
    except Ailment.DoesNotExist:
        return JsonResponse({"error": "Ailment not found."}, status=status.HTTP_404_NOT_FOUND)
# generic views encapsulate common behavior, making it easier to create views for various CRUD (Create, Read, Update, Delete) operations without having to write the same boilerplate code repeatedly.
#----------------------------------------------------------------------------------------------    
    # -------------------------------------------------
class HostelAssetListCreateView(generics.ListCreateAPIView):
    queryset = HostelAsset.objects.all()
    print(queryset)
    serializer_class = HostelAssetSerializer

class HostelAssetDetail(APIView):
    def delete(self, request, pk):
        try:
            asset = get_object_or_404(HostelAsset, pk=pk)
            asset.delete()
            return JsonResponse(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



#------------------------    
#------------------------
class MedicineListCreateView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

class MedicineRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

#------------------------hospital visit----------
                  
class HospitalList(generics.ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class HospitalTypeList(generics.ListAPIView):
    serializer_class = HospitalSerializer

    def get_queryset(self):
        hospital_name = self.request.query_params.get('hospital_name', None)
        if hospital_name:
            return Hospital.objects.filter(HospitalName__iexact=hospital_name)
        return Hospital.objects.all()

class DepartmentList(generics.ListAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        hospital_type = self.request.query_params.get('hospital_type', None)
        if hospital_type:
            return Department.objects.filter(HospitalID__hospitalType__iexact=hospital_type)
        return Department.objects.all()            
    
#----------------student assest view-------------
class HostelAssetList(generics.ListAPIView):
    queryset = HostelAsset.objects.all()
    serializer_class = HostelAssetSerializer    

#------------------hospital visit------------
class HospitalVisitListCreateView(generics.ListCreateAPIView):
    queryset = HospitalVisit.objects.all()
    serializer_class = HospitalVisitSerializer 

#------------------
def save_hospital_visit(request):
    if request.method == 'POST':
        data = request.POST  # Assuming data is sent as form data

        # Fetch HospitalID from the selected hospital name
        hospital_name = data.get('HospitalName')
        try:
            hospital = Hospital.objects.get(HospitalName=hospital_name)
        except Hospital.DoesNotExist:
            return JsonResponse({'error': 'Hospital not found'}, status=404)

        # Create the HospitalVisit instance with Purpose, VisitDate, and HospitalID
        visit = HospitalVisit.objects.create(
            HospitalID=hospital,
            Purpose=data.get('Purpose'),
            VisitDate=data.get('VisitDate')
        )

        # Create a serializer instance with the created visit
        serializer = HospitalVisitSerializer(visit)

        return JsonResponse(serializer.data, status=201)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    


#--------------------
def search_health_records(request):
    if request.method == 'GET':
        registration_number = request.GET.get('registrationNumber', '')
        # Assuming Student model has a field named 'registrationNumber', adjust accordingly
        health_records = HealthRecord.objects.filter(RegistrationNumber__registrationNumber__icontains=registration_number)
        # Adjust the field names based on your model structure

        records_data = []
        for record in health_records:
            record_data = {
                'healthId': record.healthId,
                'studentName': record.RegistrationNumber.studentName,
                'ailmentName': record.AilmentID.ailmentName,
                'Description': record.Description,
                'diagnosis': record.diagnosis,
                'date': record.date.strftime('%Y-%m-%d %H:%M:%S')  # Format date as needed
            }
            records_data.append(record_data)

        return JsonResponse(records_data, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)          