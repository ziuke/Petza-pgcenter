from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class Register(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('adopter', 'Adopter'),
        ('shelter', 'Shelter'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    # Common attributes
    phone = models.CharField(max_length=15, blank=True)
    location = models.TextField(blank=True)
    
    # Shelter-specific
    shelter_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"

from django.db import models
from django.conf import settings

def pet_image_upload_path(instance, filename):
    return f'pets/{instance.shelter.id}/{filename}'

class Pet(models.Model):
    pet_id = models.CharField(max_length=10, unique=True, blank=True)
    shelter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'shelter'}
    )
    foster_home_name = models.CharField(max_length=150, blank=True, null=True)
    foster_home_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    health_status = models.TextField()
    image = models.ImageField(upload_to=pet_image_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.breed}) - ID: {self.pet_id}"

class AdoptionRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    adopter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'adopter'})
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.adopter.username} -> {self.pet.name}"