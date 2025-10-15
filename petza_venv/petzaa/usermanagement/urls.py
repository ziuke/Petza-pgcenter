from django.urls import path
from . import views

urlpatterns = [
    path ('',views.index),
    path ('about', views.about, name='about'),
    path ('contact', views.contact, name='contact'),
    path ('gallery', views.gallery, name='gallery'),
    path('register_adopter/', views.register_adopter, name='register_adopter'),
    path('register_shelter/', views.register_shelter, name='register_shelter'),
    path('do_login/', views.login_view, name='do_login'),
    path('do_logout/', views.do_logout, name='do_logout'),
    path('view_adopters/', views.manage_adopters, name='manage_adopters'),
    path('view_shelters/', views.manage_shelters, name='manage_shelters'),
    path('add_pet/', views.add_pet, name='add_pet'),
    path('edit_pet/<int:pet_id>/', views.edit_pet, name='edit_pet'),
    path('delete_pet/<str:pet_id>/', views.delete_pet, name='delete_pet'),
    path('my_pets/', views.my_pets, name='my_pets'),
    path('view_pets/', views.view_pets, name='view_pets'),
    path('adopt_pet/<int:pet_id>/', views.adopt_pet, name='adopt_pet'),
    path('request_adoption/<int:pet_id>/', views.request_adoption, name='request_adoption'),
    

   


    
]