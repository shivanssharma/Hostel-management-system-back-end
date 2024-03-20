# from django.urls import path
# from .views import *  

# urlpatterns = [
#      #path('3ug/', get_3ug_list, name='get_3ug_list'),
#    # path('rooms/', get_room_list, name='get_room_list'),
#     path('students/<str:course_type>/', get_students_by_room_type, name='get_room_list_by_room_type'),
#     path('room/<str:floor_type>/<int:room_type>/<str:position>', get_room_list, name='get_room_list'),
#     path('save_data/', assign_room, name='save_data'),

#     path('medicines/', medicines, name='medicines'),
#     # path('ailment/<str:ailment_type>/', ailment, name='ailment'),
#     path('suggest_medicine/<str:ailment_name>/', ailment_suggestion, name='ailment_suggestion'),
#     # path('medicine_equipment/', medicine_equipment, name='medicines'),
#     path('form_data/', form_data.as_view(), name='form_data'),
#     path('list/<str:floor_number>/<int:room_number>/', get_student_list, name='get_student_list'),
#     path('store/', get_items, name='get_items'),
#     path('student_pannel/<str:floor_number>/<int:room_number>/', get_student_list_pannel, name='get_items'),
#     path('adminstore/<str:course_name>/', get_admin_store, name='get_items'),
#     path('delete-student/',delete_student, name='delete_student'),
#     path('login/', user_login, name='login'),
#     path('signup/', signup, name='createuser'),
#     # path('/admin/login/?next=/admin/', my_custom_login, name='login'),
#     # path('login/', user_signin, name='login'),
#     # path('signup/', user_signup, name='login'),
#     path('usernames/', get_all_usernames.as_view(), name='get_all_usernames'),
#     # path('change_password/', change_password, name='get_all_usernames'),
    
#     path('delete-user/<str:username>/', delete_user, name='delete_user'),
#     path('password-reset/', password_reset, name='password_reset'),
#     path('update-user-status/', UpdateUserStatusView.as_view(), name='password_reset'),

#     path('ailment/', AilmentListCreateView.as_view(), name='ailment-list-create'),
#     path('ailment/<str:name>/', delete_ailment_by_name, name='ailment-delete'),

#     path('hostel_assets/', HostelAssetListCreateView.as_view(), name='hostel-asset-list-create'),
#     # path('hostel_assets/<int:pk>/', HostelAssetDetail.as_view(), name='hostel-asset-detail'),

#     path('medicine/', MedicineListCreateView.as_view(), name='medicine-list-create'),
#     path('medicine/<int:pk>/', MedicineRetrieveUpdateDestroyView.as_view(), name='medicine-retrieve-update-destroy'),

#     path('hospitals/', HospitalList.as_view(), name='hospital-list'),
#     path('hospital-types/', HospitalTypeList.as_view(), name='hospital-type-list'),
#     path('departments/',DepartmentList.as_view(), name='department-list'),

#     path('hostel_assets/', HostelAssetList.as_view(), name='hostel_asset_list'),

#     path('hospital_visits/', HospitalVisitListCreateView.as_view(), name='hospital-visit-list-create'),
#     path('hospital_visits/',save_hospital_visit,name='saving_hostel_visits'),

#     path('healthrecords/<int:registrationnumber>', search_health_records, name='search_health_records'),

#     path('save_student_data/',student_list,name="form_data"),
#     path('logout/',logout_view,name="log_out"),

#     path('remove_student/<str:first_name>',delete_student_and_room,name="remove_room"),






#     path('suggest_medicine/<str:ailment_name>/', ailment_suggestion, name='ailment_suggestion'),
#     path('ailment/', AilmentListCreateView.as_view(), name='ailment-list-create'),
#     path('ailment/<str:name>/', delete_ailment_by_name, name='ailment-delete'),   
    
#     # path('notifications/',NotificationView.as_view(),name='notifications-list'),

#     path('login/', user_login, name='login'),
#     path('signup/',signup, name='createuser'),

#     path('save_student_data/',student_list,name="form_data"),
    
#     path('hostel_assets/', HostelAssetListCreateView.as_view(), name='hostel-asset-list-create'),
#     # path('hostel_assets/<str:name>/', HostelAssetDetail.as_view(), name='hostel-asset-detail'),

#     path('medicine/', MedicineListCreateView.as_view(), name='medicine-list-create'),
#     path('medicine/<int:pk>/', MedicineRetrieveUpdateDestroyView.as_view(), name='medicine-retrieve-update-destroy'),

#     path('submit-electronic/', SubmitElectronicView.as_view(), name='submit-electronic'),

#     path('hospitals/', HospitalList.as_view(), name='hospital-list'),
#     path('hospital-types/', HospitalTypeList.as_view(), name='hospital-type-list'),
#     path('departments/', DepartmentList.as_view(), name='department-list'),

#     path('hostel_assets/', HostelAssetList.as_view(), name='hostel_asset_list'),

#     path('hospital_visits/', HospitalVisitListCreateView.as_view(), name='hospital-visit-list-create'),

#     path('list/<str:floor_number>/<int:room_number>/', get_student_list, name='get_student_list'),
#     path('hospital_visits/',save_hospital_visit,name='saving_hostel_visits'),

#     path('healthrecords/', search_health_records, name='search_health_records'),

#     path('get_floor_and_room_numbers/', get_floor_and_room_numbers, name='get_floor_and_room_numbers'),
    
#     path('student_pannel/<str:floor_number>/<str:room_number>/', get_student_list_pannel, name='get_student_panel'),

#     path('save_hospital_visit/',save_hospital_visit,name='save_hospital_visit'),

#     path('hospital-visits/', get_hospital_visits, name='hospital_visits'),

#     path('delete_assets/<str:assetName>/', HostelAssetDetail.as_view(), name='delete_asset'),
# ]
from django.urls import path
from .views import *  

urlpatterns = [
    path('students/<str:course_type>/', get_students_by_room_type, name='get_room_list_by_room_type'),
    path('room/<str:floor_type>/<int:room_type>/<str:position>', get_room_list, name='get_room_list'),
    path('save_data/', assign_room, name='save_data'),
    path('medicines/', medicines, name='medicines'),
    path('suggest_medicine/<str:ailment_name>/', ailment_suggestion, name='ailment_suggestion'),
    path('form_data/', form_data.as_view(), name='form_data'),
    path('list/<str:floor_number>/<int:room_number>/', get_student_list, name='get_student_list'),
    path('store/', get_items, name='get_items'),
    path('student_pannel/<str:floor_number>/<int:room_number>/', get_student_list_pannel, name='get_items'),
    path('adminstore/<str:course_name>/', get_admin_store, name='get_items'),
    path('delete-student/',delete_student, name='delete_student'),
    path('login/', user_login, name='login'),
    path('signup/', signup, name='createuser'),
    path('usernames/', get_all_usernames.as_view(), name='get_all_usernames'),
    path('delete-user/<str:username>/', delete_user, name='delete_user'),
    path('password-reset/', password_reset, name='password_reset'),
    path('update-user-status/', UpdateUserStatusView.as_view(), name='password_reset'),
    path('ailment/', AilmentListCreateView.as_view(), name='ailment-list-create'),
    path('ailment/<str:name>/', delete_ailment_by_name, name='ailment-delete'),
    path('hostel_assets/', HostelAssetListCreateView.as_view(), name='hostel-asset-list-create'),
    path('medicine/', MedicineListCreateView.as_view(), name='medicine-list-create'),
    path('medicine/<int:pk>/', MedicineRetrieveUpdateDestroyView.as_view(), name='medicine-retrieve-update-destroy'),
    path('hospitals/', HospitalList.as_view(), name='hospital-list'),
    path('hospital-types/', HospitalTypeList.as_view(), name='hospital-type-list'),
    path('departments/', DepartmentList.as_view(), name='department-list'),
    path('hostel_assets/', HostelAssetList.as_view(), name='hostel_asset_list'),
    path('hospital_visits/', HospitalVisitListCreateView.as_view(), name='hospital-visit-list-create'),
    path('healthrecords/<int:registrationnumber>', search_health_records, name='search_health_records'),
    path('save_student_data/',student_list,name="form_data"),
    path('logout/',logout_view,name="log_out"),
    path('remove_student/<str:first_name>',delete_student_and_room,name="remove_room"),
    path('submit-electronic/', SubmitElectronicView.as_view(), name='submit-electronic'),
    path('hospital_visits/',save_hospital_visit,name='saving_hostel_visits'),
    path('get_floor_and_room_numbers/', get_floor_and_room_numbers, name='get_floor_and_room_numbers'),
    path('student_pannel/<str:floor_number>/<str:room_number>/', get_student_list_pannel, name='get_student_panel'),
    path('save_hospital_visit/',save_hospital_visit,name='save_hospital_visit'),
    path('hospital-visits/', get_hospital_visits, name='hospital_visits'),
    path('delete_assets/<str:assetName>/', HostelAssetDetail.as_view(), name='delete_asset'),
    
    path('book_asset/', book_asset, name='book_asset'),

    path('asset_bookings/',asset_bookings,name='asset_bookings')
]
