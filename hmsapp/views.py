from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Room,Student,Ailment,Medicine,HostelAsset,NecessityStoreItem,HealthRecord,Reservation # Assuming Room is the model you're working with
import json
from django.views.decorators.csrf import csrf_exempt
from .HmsSerializer import *
from rest_framework.views import APIView 
from rest_framework import generics
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib import auth 
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django.utils import timezone;

#-----------------------for room------------------------
# def get_room_list(request, floor_type, room_type):
    
#     if request.method == 'GET':
#             rooms = Room.objects.filter(FloorNumber=floor_type, RoomNumber=room_type)
#             student_first_names = [room.RegistrationNumber.FirstName for room in rooms]
#             # student_first_names = rooms
#             return JsonResponse(student_first_names, safe=False)
#     else:
#         return JsonResponse({"error": "Invalid request method"}, status=405)

# @csrf_exempt
# def get_room_list(request, floor_type, room_type,position):
#     print(request)
#     if request.method == 'GET':
#         try:
#             # Filter rooms based on floor and room type
#             rooms = Room.objects.filter(FloorNumber=floor_type, RoomNumber=room_type)
            
#             # Get first names of students assigned to these rooms
#             student_first_names = [student.FirstName for room in rooms for student in room.RegistrationNumber.all()]

#             return JsonResponse(student_first_names, safe=False)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     else:
#         return JsonResponse({"error": "Invalid request method"}, status=405)
    

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Room, Student

def get_room_list(request,floor_type, room_type, position):
    print(request.body)
    try:
        # Get the room object based on floor number and room number
        if position == 'room leader':
            rooms = Room.objects.filter(FloorNumber=floor_type, RoomNumber=room_type,roomLeader=True)
        elif position == 'room mate':
            rooms = Room.objects.filter(FloorNumber=floor_type, RoomNumber=room_type,roomLeader=False)

        
        print(rooms)

        student_first_names = []

        for room in rooms:
            students = room.RegistrationNumber.all()  
            student_first_names.extend([student.FirstName for student in students])
            print(student_first_names)

        # Return JSON response
        return JsonResponse(student_first_names, safe=False)
    except Room.DoesNotExist:
    # Handle the case where the room doesn't exist
        return JsonResponse({'error': 'Room not found'}, status=404)

    # Get all students in the room
    # students = room.RegistrationNumber.all()
    # print(students)
    # Filter students based on position
    # if position == 'room leader':
    #     students = students.filter(roomLeader=True)
    # elif position == 'room mate':
    #     students = students.filter(roomLeader=False)
    # else:
        # Handle invalid position input
    # return JsonResponse({'error': 'Invalid position'}, status=400)

    # Get the first names of the students
    # student_first_names = [student.FirstName for student in students]
    # print(student_first_names)
    # Return JSON response
    # return JsonResponse( student_first_names,safe=False)




def get_students_by_room_type(request, course_type):
    students = Student.objects.filter(CourseName=course_type).values_list('FirstName', flat=True)
    return JsonResponse(list(students), safe=False)    





#-----------------------admin view------------------------
@csrf_exempt
def delete_student_and_room(request, first_name):
    response_data = {}

    # Get the student instance by first name
    student = get_object_or_404(Student, FirstName=first_name)

    # Update is_Room to False in Student model
    student.is_Room = False
    student.save()

    # Get the room instances where this student is registered
    rooms = Room.objects.filter(RegistrationNumber=student)

    # Delete the student from each room
    for room in rooms:
        room.RegistrationNumber.remove(student)

    response_data['message'] = "Student and associated rooms deleted successfully."
    return JsonResponse(response_data)

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

# @csrf_exempt
# def save_data(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))

#         right_list = data.get('rightList', [])
#         selected_floor = data.get('selectedFloor', None)
#         selected_room = data.get('selectedRoom', None)
#         selected_position = data.get('selectedPosition', None)

#         if not (selected_floor and selected_room and selected_position):
#             return JsonResponse({'error': 'Incomplete data provided'}, status=400)

#         students = Student.objects.filter(FirstName__in=right_list)

#         for student in students:
#             room = Room.objects.create(
#                 RegistrationNumber=student,
#                 FloorNumber=selected_floor,
#                 RoomNumber=selected_room,
#                 roomLeader=(student.FirstName in right_list and selected_position == "room leader")
#             )

#         return JsonResponse({'message': 'Room data saved successfully'}, status=200)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)  
     
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
#         print('ye hai ',students)
#         try:
#             # Check if room already exists for the provided details
#             existing_room = Room.objects.get(
#                 RegistrationNumber__in=students,
#                 FloorNumber=selected_floor,
#                 RoomNumber=selected_room
#             )
#             print('exist',existing_room)
#             if existing_room:
#                 return JsonResponse({'error': 'Room already exists'}, status=400)
            
#             # Create room if it doesn't exist
#             room = Room.objects.create(
#                 FloorNumber=selected_floor,
#                 RoomNumber=selected_room
#             )
#             for student in students:
#                 # Associate the student with the room
#                 room.RegistrationNumber.add(student)
                
#             # Determine if any student in the room list is a room leader
#             room.roomLeader = any(student.FirstName in right_list and selected_position == "room leader" for student in students)

#             # Save the changes to the room
#             room.save()
#         except IntegrityError:
#             return JsonResponse({'error': 'Failed to save data. Integrity error occurred.'}, status=500)

# from django.shortcuts import HttpResponse
# import json
# from .models import Student, Room
# @csrf_exempt
# def assign_room(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         right_list = data.get('rightList', [])
#         selected_floor = data.get('selectedFloor', '')
#         selected_room = data.get('selectedRoom', '')
#         selected_position = data.get('selectedPosition', '')

#         # Filter students by first names in rightList
#         students = Student.objects.filter(FirstName__in=right_list)

#         # Check if the room already exists for the students
#         room_exists = Room.objects.filter(RegistrationNumber__in=students.values_list('RegistrationNumber', flat=True)).exists()
        
#         # Check if any student already has a room assigned
#         room_has_room_assigned = students.filter(is_Room=True).exists()

#         if room_exists and room_has_room_assigned:
#             # Room exists and at least one student already has a room assigned
#             return HttpResponse("Room already exists and some students already have rooms assigned.")
        
#         # If room doesn't exist, create a new room
#         if not room_exists:
#             room = Room.objects.create(RoomNumber=selected_room, FloorNumber=selected_floor,roomLeader=False)
#             room.RegistrationNumber.add(*students)

        

#         # If selected position is room leader, set roomLeader as True for all students
#         if selected_position == 'room leader':
#             room.RegistrationNumber.filter(FirstName__in=right_list).update(roomLeader=True)

#         # Assign selected floor and room to all students
#         students.update(is_Room=True)    

#         return HttpResponse("Rooms assigned successfully.")

#     return HttpResponse("Invalid request method.")
# from django.shortcuts import HttpResponse
# import json
# from .models import Student, Room
# @csrf_exempt
# def assign_room(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         right_list = data.get('rightList', [])
#         selected_floor = data.get('selectedFloor', '')
#         selected_room = data.get('selectedRoom', '')
#         selected_position = data.get('selectedPosition', '')

#         for student_name in right_list:
#             # Fetch the student object
#             student = Student.objects.filter(FirstName=student_name).first()

#             # Check if the student already has a room assigned
#             if student.is_Room:
#                 return HttpResponse(f"Room already exists for student {student_name}")

#             # Create a new room for the student
#             room = Room.objects.create(RoomNumber=selected_room, FloorNumber=selected_floor)
#             room.RegistrationNumber.add(student)

#             # Update roomLeader for this student if selected_position is 'room leader'
#             if selected_position == 'room leader':
#                 room.roomLeader = True
#                 room.save()

#             # Mark the student as having a room assigned
#             student.is_Room = True
#             student.save()

#         return HttpResponse("Rooms assigned successfully.")

#     return HttpResponse("Invalid request method.")
# from django.shortcuts import HttpResponse
# import json
# from .models import Student, Room
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def assign_room(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             right_list = data.get('rightList', [])
#             selected_floor = data.get('selectedFloor', '')
#             selected_room = data.get('selectedRoom', '')
#             selected_position = data.get('selectedPosition', '')

#             if not all(isinstance(name, str) for name in right_list):
#                 return HttpResponse("Invalid student name(s) provided.")

#             if not selected_floor or not selected_room:
#                 return HttpResponse("Floor number and room number must be provided.")

#             # Check if the room already exists for the students
#             existing_students = Student.objects.filter(FirstName__in=right_list, is_Room=True)
#             if existing_students.exists():
#                 return HttpResponse(f"The following students already have rooms assigned: {', '.join(existing_students.values_list('FirstName', flat=True))}")

#             # Create a new room
#             room = Room.objects.create(RoomNumber=selected_room, FloorNumber=selected_floor)

#             # Assign students to the room
#             for student_name in right_list:
#                 student = Student.objects.filter(FirstName=student_name).first()
#                 if not student:
#                     return HttpResponse(f"Student {student_name} does not exist.")
#                 if student.is_Room:
#                     return HttpResponse(f"Room already exists for student {student_name}.")
#                 room.RegistrationNumber.add(student)

#             # Update room leader if selected
#             if selected_position == 'room leader':
#                 room.roomLeader = True
#                 room.save()

#             # Mark students as having a room assigned
#             Student.objects.filter(FirstName__in=right_list).update(is_Room=True)

#             return HttpResponse("Rooms assigned successfully.")
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {str(e)}")

#     return HttpResponse("Invalid request method.")

# from django.shortcuts import HttpResponse
# import json
# from .models import Student, Room
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def assign_room(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             right_list = data.get('rightList', [])
#             selected_floor = data.get('selectedFloor', '')
#             selected_room = data.get('selectedRoom', '')
#             selected_position = data.get('selectedPosition', '')

#             if not all(isinstance(name, str) for name in right_list):
#                 return HttpResponse("Invalid student name(s) provided.")

#             if not selected_floor or not selected_room:
#                 return HttpResponse("Floor number and room number must be provided.")

#             # Filter the rightList to get only unassigned students
#             unassigned_students = []
#             for student_name in right_list:
#                 student = Student.objects.filter(FirstName=student_name, is_Room=False).first()
#                 if student:
#                     unassigned_students.append(student)
#                 else:
#                     return HttpResponse(f"Room already exists for student {student_name}.")

#             # Create a new room if it doesn't exist
#             room, _ = Room.objects.get_or_create(RoomNumber=selected_room, FloorNumber=selected_floor)

#             # Assign unassigned students to the room
#             for student in unassigned_students:
#                 room.RegistrationNumber.add(student)

#             # Update room leader if selected
#             if selected_position == 'room leader':
#                 room.roomLeader = True
#                 room.save()

#             # Mark unassigned students as having a room assigned
#             Student.objects.filter(FirstName__in=[student.FirstName for student in unassigned_students]).update(is_Room=True)

#             return HttpResponse("Rooms assigned successfully.")
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {str(e)}")

#     return HttpResponse("Invalid request method.")


# from django.shortcuts import HttpResponse
# import json
# from .models import Student, Room
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def assign_room(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             right_list = data.get('rightList', [])
#             selected_floor = data.get('selectedFloor', '')
#             selected_room = data.get('selectedRoom', '')
#             selected_position = data.get('selectedPosition', '')

#             if not all(isinstance(name, str) for name in right_list):
#                 return HttpResponse("Invalid student name(s) provided.")

#             if not selected_floor or not selected_room:
#                 return HttpResponse("Floor number and room number must be provided.")

#             # Filter the rightList to get only existing and unassigned students
#             unassigned_students = []
#             existing_students = set(Student.objects.filter(FirstName__in=right_list, is_Room=True).values_list('FirstName', flat=True))
#             for student_name in right_list:
#                 if student_name not in existing_students:
#                     student = Student.objects.filter(FirstName=student_name, is_Room=False).first()
#                     if student:
#                         unassigned_students.append(student)
#                     else:
#                         return HttpResponse(f"Student {student_name} does not exist.")

#             # Create a new room if it doesn't exist
#             room, _ = Room.objects.get_or_create(RoomNumber=selected_room, FloorNumber=selected_floor)

#             # Assign unassigned students to the room
#             for student in unassigned_students:
#                 room.RegistrationNumber.add(student)

#             # Update room leader if selected
#             if selected_position == 'room leader':
#                 room.roomLeader = True
#                 room.save()

#             # Mark unassigned students as having a room assigned
#             Student.objects.filter(FirstName__in=[student.FirstName for student in unassigned_students]).update(is_Room=True)

#             return HttpResponse("Rooms assigned successfully.")
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {str(e)}")

#     return HttpResponse("Invalid request method.")

# from django.shortcuts import HttpResponse
# import json
# from .models import Student, Room
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def assign_room(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             right_list = data.get('rightList', [])
#             selected_floor = data.get('selectedFloor', '')
#             selected_room = data.get('selectedRoom', '')
#             selected_position = data.get('selectedPosition', '')

#             if not all(isinstance(name, str) for name in right_list):
#                 return HttpResponse("Invalid student name(s) provided.")

#             if not selected_floor or not selected_room:
#                 return HttpResponse("Floor number and room number must be provided.")

#             # Filter the rightList to get only existing and unassigned students
#             unassigned_students = []
#             existing_students = set(Student.objects.filter(FirstName__in=right_list, is_Room=True).values_list('FirstName', flat=True))
#             for student_name in right_list:
#                 if student_name not in existing_students:
#                     student = Student.objects.filter(FirstName=student_name, is_Room=False).first()
#                     if student:
#                         unassigned_students.append(student)
#                     else:
#                         return HttpResponse(f"Student {student_name} does not exist.")

#             # Create a new room if it doesn't exist
#             room, _ = Room.objects.get_or_create(RoomNumber=selected_room, FloorNumber=selected_floor)

#             # Assign unassigned students to the room
#             for student in unassigned_students:
#                 room.RegistrationNumber.add(student)

#             # Update room leader if selected
#             if selected_position == 'room leader':
#                 room.roomLeader = True
#                 room.save()

#             # Mark unassigned students as having a room assigned
#             Student.objects.filter(FirstName__in=[student.FirstName for student in unassigned_students]).update(is_Room=True)

#             return HttpResponse("Rooms assigned successfully.")
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {str(e)}")

#     return HttpResponse("Invalid request method.")

# from django.shortcuts import HttpResponse
# import json
# from .models import Student, Room
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def assign_room(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             right_list = data.get('rightList', [])
#             selected_floor = data.get('selectedFloor', '')
#             selected_room = data.get('selectedRoom', '')
#             selected_position = data.get('selectedPosition', '')

#             if not all(isinstance(name, str) for name in right_list):
#                 return HttpResponse("Invalid student name(s) provided.")

#             if not selected_floor or not selected_room:
#                 return HttpResponse("Floor number and room number must be provided.")

#             # Filter the rightList to get only existing and unassigned students
#             unassigned_students = []
#             existing_students = set(Student.objects.filter(FirstName__in=right_list, is_Room=True).values_list('FirstName', flat=True))
#             for student_name in right_list:
#                 if student_name not in existing_students:
#                     student = Student.objects.filter(FirstName=student_name, is_Room=False).first()
#                     if student:
#                         unassigned_students.append(student)
#                     else:
#                         return HttpResponse(f"Student {student_name} does not exist.")

#             # Create a new room if it doesn't exist
#             room, _ = Room.objects.get_or_create(RoomNumber=selected_room, FloorNumber=selected_floor)

#             # Assign unassigned students to the room
#             for student in unassigned_students:
#                 room.RegistrationNumber.add(student)

#             # Update room leader if selected
#             if selected_position == 'room leader':
#                 room.roomLeader = True
#                 room.save()
#                 # Mark unassigned students as having a room assigned with room leader position
#                 Student.objects.filter(FirstName__in=[student.FirstName for student in unassigned_students]).update(is_Room=True, is_RoomLeader=True)

#             # Update room mate if selected
#             elif selected_position == 'room mate':
#                 # Mark unassigned students as having a room assigned with room mate position
#                 Student.objects.filter(FirstName__in=[student.FirstName for student in unassigned_students]).update(is_Room=True, is_RoomLeader=False)

#             return HttpResponse("Rooms assigned successfully.")
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {str(e)}")

#     return HttpResponse("Invalid request method.")

#for room component

# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import Room, Student

# @csrf_exempt
# def assign_room(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             assignments = data.get('assignments', [])

#             if not isinstance(assignments, list):
#                 return HttpResponse("Assignments must be provided as a list of dictionaries.")

#             for assignment in assignments:
#                 student_name = assignment.get('student_name', '')
#                 room_number = assignment.get('room_number', '')
#                 floor_number = assignment.get('floor_number', '')
#                 selected_position = assignment.get('selected_position', '')

#                 if not isinstance(student_name, str) or not isinstance(room_number, str) or not isinstance(floor_number, str):
#                     return HttpResponse("Student name, room number, and floor number must be provided as strings.")
                
#                 if not selected_position in ['room leader', 'room mate']:
#                     return HttpResponse("Selected position must be 'room leader' or 'room mate'.")

#                 student = Student.objects.filter(FirstName=student_name, is_Room=False).first()
#                 if not student:
#                     return HttpResponse(f"Student {student_name} does not exist or already assigned to a room.")

#                 room, _ = Room.objects.get_or_create(RoomNumber=room_number, FloorNumber=floor_number)

#                 room.RegistrationNumber.add(student)

#                 if selected_position == 'room leader':
#                     room.roomLeader = True
#                     room.save()
#                 # No need to set is_RoomLeader if the field doesn't exist in the Student model
#                 student.is_Room = True
#                 student.save()

#             return HttpResponse("Rooms assigned successfully.")
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {str(e)}")

#     return HttpResponse("Invalid request method.")

from django.http import JsonResponse
import json
@csrf_exempt
def assign_room(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        right_list = data.get('rightList', [])
        selected_floor = data.get('selectedFloor', '')
        selected_room = data.get('selectedRoom', '')
        selected_position = data.get('selectedPosition', '')

        for first_name in right_list:
            # Filter Student by FirstName
            students = Student.objects.filter(FirstName=first_name)

            for student in students:
                # Check if student already has a room
                if not student.is_Room:
                    # If not, create a room for the student
                    room = Room.objects.create(
                        FloorNumber=selected_floor,
                        RoomNumber=selected_room,
                        roomLeader=(selected_position == 'room leader')
                    )
                    # Add student to the room
                    room.RegistrationNumber.add(student)

                    # Update student's room status
                    student.is_Room = True
                    student.save()

        return JsonResponse({'message': 'Rooms assigned successfully'}, status=200)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

#--------------------------------------------------------------------------------
# def get_student_list(request, floor_number, room_number):
#     print(request)
#     try:
#         rooms = Room.objects.filter(FloorNumber=floor_number, RoomNumber=room_number)
#         print(rooms)
#     except Room.DoesNotExist:
#         return JsonResponse("Room not found", status=404)
#     print('here')
#     student_list = []
#     for room in rooms:
#         students = room.RegistrationNumber      #.all()
#         # for student in students:
#         if students:
#             student_list.append({
#                 'FirstName': students.FirstName,
#                 'LastName': students.LastName,
#                 'CourseName': students.CourseName,
#             })
#     print(student_list)
#     return JsonResponse(student_list, safe=False)


def get_student_list(request, floor_number, room_number):
    try:
        rooms = Room.objects.filter(FloorNumber=floor_number, RoomNumber=room_number)
    except Room.DoesNotExist:
        return JsonResponse("Room not found", status=404)
    
    student_list = []
    for room in rooms:
        students = room.RegistrationNumber.all()  # Access all students related to the room
        for student in students:
            student_list.append({
                'FirstName': student.FirstName,
                'LastName': student.LastName,
                'CourseName': student.CourseName,
            })

    return JsonResponse(student_list, safe=False)
#this is for student room for student pannel
# def get_student_list_pannel(request, floor_number, room_number):
#     print(request)
#     try:
#         rooms = Room.objects.filter(FloorNumber=floor_number, RoomNumber=room_number)
#         print(rooms)
#     except Room.DoesNotExist:
#         return JsonResponse("Room not found", status=404)
#     print('here')
#     student_list = []
#     for room in rooms:
#         students = room.RegistrationNumber.all()
#         # for student in students:
#         if students:
#             student_list.append({
#                 'FirstName': students.FirstName,
#                 'LastName': students.LastName,
#                 'CourseName': students.CourseName,
#             })
#     print(student_list)
#     return JsonResponse(student_list, safe=False)
def get_student_list_pannel(request, floor_number, room_number):
    try:
        rooms = Room.objects.filter(FloorNumber=floor_number, RoomNumber=room_number)
    except Room.DoesNotExist:
        return JsonResponse("Room not found", status=404)
    
    student_list = []
    for room in rooms:
        students = room.RegistrationNumber.all()  # accessing the related students
        for student in students:
            student_list.append({
                'FirstName': student.FirstName,
                'LastName': student.LastName,
                'CourseName': student.CourseName,
            })
    
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
                response_data = {
                    'username': user.username,
                    'is_superuser': user.is_superuser,
                    'is_staff': user.is_staff,
                    'is_active': user.is_active,
                }
                # Save username to local storage
                response = JsonResponse(response_data)
                response.set_cookie('username', user.username)  # Set a cookie with the username
                return response
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

  
@csrf_exempt
def logout_view(request):
    print(request)
    auth.logout(request)
    return JsonResponse({'message': 'Logout successful'})

#-------------------------------admin manage view------------------------------
# @login_required(login_url=/)
# def get_all_usernames(request):
#     users = User.objects.all()
#     usernames = [user.username for user in users]
#     return JsonResponse({'usernames': usernames})       

class get_all_usernames(APIView):
    def get(self, request):
        users = User.objects.all()
        user_data = []
        for user in users:
            user_data.append({
                'username': user.username,
                'is_superuser': user.is_superuser,
                'is_staff'
                'is_active': user.is_active,
            })
        return Response({'users': user_data})


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

# views.py

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserStatusView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            is_superuser = data.get('is_superuser')
            is_active = data.get('is_active')
            is_staff = data.get('is_staff')
            # Retrieve user object
            user = User.objects.get(username=username)

            # Update user properties
            user.is_superuser = is_superuser
            user.is_active = is_active
            user.is_staff = is_staff
            # Save changes
            user.save()

            return JsonResponse({'success': True, 'message': 'User status updated successfully'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


#this is for status of user
# views.py



# views.py


# class UserDetailView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user

    
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
    def get(self, request, assetName):
        try:
            asset = get_object_or_404(HostelAsset, AssetName=assetName)
            data = {
                'AssetName': asset.AssetName,
                'Description': asset.Description,
                'AvailabilityStatus': asset.AvailabilityStatus
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, assetName):
        try:
            asset = get_object_or_404(HostelAsset,AssetName=assetName)
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
@csrf_exempt
def save_hospital_visit(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Fetch HospitalID from the selected hospital name
        hospital_id = data.get('HospitalID')
        try:
            hospital = Hospital.objects.get(HospitalID=hospital_id)
        except Hospital.DoesNotExist:
            return JsonResponse({'error': 'Hospital not found'}, status=404)

        # Fetch the logged-in user based on username
        username = data.get('username')
        try:
            user = User.objects.get(username=username)
            # Find the corresponding student object
            student = Student.objects.get(user=user)
        except (User.DoesNotExist, Student.DoesNotExist):
            return JsonResponse({'error': 'Student not found'}, status=404)

        # Extract RegistrationNumber from the Student
        registration_number = student.RegistrationNumber

        # Create serializer instance with data
        serializer = HospitalVisitSerializer(data={
            'RegistrationNumber': registration_number,
            'HospitalID': hospital.HospitalID,
            'Purpose': data.get('Purpose'),
            'VisitDate': data.get('VisitDate')
        })

        # Validate and save serializer data
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
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
    
#-------------------------------registration----------------------------

@csrf_exempt

def student_list(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            username = data.get('username')  # Retrieve username from the request data

            # Query the User model to find the corresponding user with the given username
            user = User.objects.get(username=username)
            print(user)
            # Process the data and link it to the user
            mapped_data = {
                'RegistrationNumber': data.get('regis'),
                'user': user.id,  # Assign the user object retrieved from the request data
                'FirstName': data.get('fname'),
                'LastName': data.get('lname'),
                'CourseName': data.get('selectedCourse'),
                'DateOfJoining': data.get('date'),
                'FatherName': data.get('father'),
                'MotherName': data.get('mother'),
                'DateOfBirth': data.get('birth'),
                'MobileNumber': data.get('phone'),
                'EmailID': data.get('email'),
                'Address': data.get('address'),
            }

            serializer = StudentSerializer(data=mapped_data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)        
        

#--------------------------admin view hospital visit--------------
        
def get_hospital_visits(request):
    if request.method == 'GET':
        hospital_visits = HospitalVisit.objects.all()
        visit_data = []
        for visit in hospital_visits:
            hospital_name = visit.HospitalID.HospitalName
            department_name = None
            try:
                department = visit.HospitalID.department_set.first()
                if department:
                    department_name = department.departmentName
            except Department.DoesNotExist:
                pass
                
            visit_info = {
                'VisitID': visit.pk,
                'Purpose': visit.Purpose,
                'RegistrationNumber': visit.RegistrationNumber.RegistrationNumber,
                'HospitalName': hospital_name,
                'Department': department_name
            }
            visit_data.append(visit_info)
        return JsonResponse(visit_data, safe=False)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)        


    #--------------------student view room
@api_view(['GET'])

def get_floor_and_room_numbers(request):
    username = request.GET.get('username')  # Get the username from the query parameter
    try:
        # Find the user object based on the username
        user = User.objects.get(username=username)
        
        # Find the corresponding student object
        student = Student.objects.get(user=user)
        
        # Retrieve the room details using the ForeignKey relationship
        room = student.room_set.first()
        if room:
            floor_number = room.FloorNumber
            room_number = room.RoomNumber
            # Return floor and room numbers
            return Response({
                'floorNumber': floor_number,
                'roomNumber': room_number,
            })
        else:
            return Response({'error': 'Room details not found for the student'}, status=404)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # Return any other errors
    
#----------------------------------------------------
class SubmitElectronicView(APIView):
    def post(self, request):
        try:
            # Extract data from the request payload
            registration_number = request.data.get('registration_number')
            mobile_phone = request.data.get('mobile_phone')
            laptop = request.data.get('laptop')
            earphone = request.data.get('earphone')
            kindle = request.data.get('kindle')

            # Fetch the registration object based on the provided registration number
            registration = Student.objects.get(registration_number=registration_number)

            # Create an instance of Electronics model
            electronics_data = {
                'RegistrationNumber': registration,
                'mobilePhone': mobile_phone,
                'laptop': laptop,
                'earphone': earphone,
                'kindle': kindle
            }
            electronics_serializer = ElectronicsSerializer(data=electronics_data)
            
            # Validate and save the instance
            if electronics_serializer.is_valid():
                electronics_serializer.save()
                return JsonResponse({'success': True, 'message': 'Electronic record submitted successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'success': False, 'message': electronics_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Registration not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)    
        
#----------------------------Admin asset delete-----------------------------
       
# def delete_asset(request, asset_id):
#     # Retrieve the asset from the database
#     asset = get_object_or_404(HostelAsset, pk=asset_id)

#     # Delete the asset
#     asset.delete()

#     # Return a JSON response indicating success
#     return JsonResponse({'message': 'Hostel Asset deleted successfully.'})                
# class HostelAssetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = HostelAsset.objects.all()
#     serializer_class = HostelAssetSerializer
        
@api_view(['GET'])
@csrf_exempt
def asset_bookings(request):
    try:
        # Retrieve all reservations with related student's name and asset name
        bookings = Reservation.objects.select_related('RegistrationNumber', 'AssetID').all()

        # Prepare data to include student's name and asset name in each booking
        bookings_data = []
        for booking in bookings:
            booking_data = {
                'ReservationID': booking.ReservationID,
                'StudentName': f"{booking.RegistrationNumber.FirstName} {booking.RegistrationNumber.LastName}",
                'AssetName': booking.AssetID.AssetName,
                'ReservationDate': booking.ReservationDate,
            }
            bookings_data.append(booking_data)

        # Return the data as JSON response
        return Response(bookings_data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)        
    
@api_view(['POST'])
def book_asset(request):
    if request.method == 'POST':
        try:
            # Retrieve data from the request body
            data = request.data
            username = data.get('username')
            assetID = data.get('assetID')

            # Retrieve the corresponding Student object and get its registration number
            student = Student.objects.get(user__username=username)
            registration_number = student.RegistrationNumber

            # Create a serializer instance with the data
            serializer = ReservationSerializer(data={
                'RegistrationNumber': registration_number,
                'AssetID': assetID,
                'ReservationDate': timezone.now(),  # Include the reservation date
            })
            # Validate the serializer data
            if serializer.is_valid():
                # Save the serializer instance (create a new reservation)
                serializer.save()
                return Response({'message': 'Asset booked successfully'}, status=status.HTTP_201_CREATED)
            else:
                # Return validation errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Student.DoesNotExist:
            # Handle the case where the corresponding student does not exist
            return Response({'error': 'Student does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle other exceptions
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)    