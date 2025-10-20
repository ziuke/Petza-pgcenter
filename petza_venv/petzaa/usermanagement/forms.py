from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Register

# Adopter registration
class AdopterForm(UserCreationForm):
    class Meta:
        model = Register
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'location']

# Shelter registration
class ShelterForm(UserCreationForm):
    class Meta:
        model = Register
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'location', 'shelter_name']

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))

from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['pet_id', 'name', 'breed', 'age', 'health_status', 'image', 'foster_home_name', 'foster_home_id']
        widgets = {
            'health_status': forms.Textarea(attrs={'rows': 3}),
        }


from django import forms
from .models import AdoptionRequest

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['pet']

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Register
        fields = ['username', 'location', 'phone', 'profile_image']  # default fields

from django import forms
from .models import Message, Register


class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=Register.objects.all(), required=False, widget=forms.HiddenInput())

    class Meta:
        model = Message
        fields = ['content', 'receiver']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Type your message...'}),
        }
