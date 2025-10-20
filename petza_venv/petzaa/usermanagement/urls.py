from django.urls import path
from . import views

urlpatterns = [
    path ('',views.index),
    path ('about', views.about, name='about'),
    path ('services', views.services, name='service'),
    path('register_adopter/', views.register_adopter, name='register_adopter'),
    path('register_shelter/', views.register_shelter, name='register_shelter'),
    path('do_login/', views.login_view, name='do_login'),
    path('do_logout/', views.do_logout, name='do_logout'),
    path('view_adopters/', views.manage_adopters, name='manage_adopters'),
    path('view_shelters/', views.manage_shelters, name='manage_shelters'),
    path('add_pet/', views.add_pet, name='add_pet'),
    path('edit_pet/<int:pet_id>/', views.edit_pet, name='edit_pet'),
    path('pets/<str:pet_id>/confirm-delete/', views.confirm_delete_pet, name='confirm_delete_pet'),
    path('delete_pet/<str:pet_id>/', views.delete_pet, name='delete_pet'),
    path('my_pets/', views.my_pets, name='my_pets'),
    path('view_pets/', views.view_pets, name='view_pets'),
    
    path('request_adoption/<int:pet_id>/', views.request_adoption, name='request_adoption'),
    path('adoptions/', views.shelter_adoption_requests, name='shelter_adoption_requests'),
    path('adoption/<int:request_id>/<str:status>/', views.update_adoption_status, name='update_adoption_status'),
    path('my-adoptions/', views.my_adoptions, name='my_adoptions'),
   path('track-adoption/<int:request_id>/', views.track_adoption_status, name='track_adoption_status'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('chat/<int:pet_id>/', views.chat_view, name='chat_view'),
    path('messages/', views.message_list, name='message_list'),

    path('adoption-dashboard/', views.admin_adoption_dashboard, name='admin_adoption_dashboard'),
    path('adoption-list/', views.admin_adoption_list, name='admin_adoption_list'),

    

    
]