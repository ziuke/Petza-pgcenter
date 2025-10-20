from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

class Register(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('adopter', 'Adopter'),
        ('shelter', 'Shelter'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    location = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)  # ✅ add this
    shelter_name = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"{self.username} ({self.user_type})"

from django.db import models
from django.conf import settings

def pet_image_upload_path(instance, filename):
    return f'pets/{instance.shelter.id}/{filename}'

class Pet(models.Model):
    PET_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('rabbit', 'Rabbit'),
        ('bird', 'Bird'),
    ]
    pet_id = models.CharField(max_length=10, unique=True, blank=True)
    shelter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'shelter'}
    )
    adopter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={'user_type': 'adopter'},
        related_name='adopted_pets'
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
    type = models.CharField(max_length=10, choices=PET_CHOICES, default='dog')  # new field

    def __str__(self):
        return f"{self.name} ({self.breed}) - ID: {self.pet_id}"

class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Reviewing', 'Reviewing'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Adopted', 'Adopted'),
    ]
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='requests')
    adopter = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.adopter.username} → {self.pet.name} ({self.status})"
    
    @property
    def shelter(self):
        """Return the shelter of the pet for convenience."""
        return self.pet.shelter


class Message(models.Model):
    sender = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='received_messages')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['timestamp']
    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.content[:20]}"
