from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def gallery(request):
    return render(request, 'gallery.html')

from django.shortcuts import render, redirect
from django.http import HttpResponse

def register_adopter(request):
    # You can later replace with form logic
    return HttpResponse("Adopter Registration Page")

def register_shelter(request):
    # You can later replace with form logic
    return HttpResponse("Shelter Registration Page")

def login_view(request):
    # Replace with your login logic
    return HttpResponse("Login Page")


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import  AdopterForm, ShelterForm


def register_adopter(request):
    if request.method == 'POST':
        form = AdopterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'adopter'
            user.save()
            messages.success(request, "Adopter registered successfully!")
            return redirect('login_view')
    else:
        form = AdopterForm()
    return render(request, 'register_adopter.html', {'form': form})

def register_shelter(request):
    if request.method == 'POST':
        form = ShelterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'shelter'
            user.save()
            messages.success(request, "Shelter registered successfully!")
            return redirect('login_view')
    else:
        form = ShelterForm()
    return render(request, 'register_shelter.html', {'form': form})





from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate using Django's authenticate function
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request, f"Welcome {user.username}!")
                if user.is_superuser:
                    user.user_type ='admin'
                    user.save()
                request.session['ut'] = user.user_type
                # Redirect based on user_type
                if user.user_type == 'admin':
                    return redirect('/')   # define this URL
                elif user.user_type == 'adopter':
                    return redirect('/') # define this URL
                elif user.user_type == 'shelter':
                    return redirect('/') # define this URL
                else:
                    return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

def do_logout(request):
    # Log out the user
    logout(request)
    
    # Clear the session variable (optional but recommended)
    if 'ut' in request.session:
        del request.session['ut']
    
    # Optional message
    messages.success(request, "You have successfully logged out.")
    
    # Redirect to home or login page
    return redirect('do_login')  # or redirect('/') for homepage


# views.py
from django.shortcuts import render
from .models import Register
from django.contrib.auth.decorators import login_required

@login_required
def manage_adopters(request):
    # Ensure only admin can access
    if request.user.user_type != 'admin':
        return render(request, 'access_denied.html')
    
    adopters = Register.objects.filter(user_type='adopter')
    return render(request, 'manage_adopters.html', {'adopters': adopters})

@login_required
def manage_shelters(request):
    if request.user.user_type != 'admin':
        return render(request, 'access_denied.html')
    
    shelters = Register.objects.filter(user_type='shelter')
    return render(request, 'manage_shelters.html', {'shelters': shelters})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pet
from .forms import PetForm

@login_required
def add_pet(request):
    if request.user.user_type != 'shelter':
        return render(request, 'access_denied.html')

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.shelter = request.user
            pet.save()
            return redirect('my_pets')
    else:
        form = PetForm()
    return render(request, 'add_pet.html', {'form': form})

@login_required
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, pet_id=pet_id, shelter=request.user)
    if request.user.user_type != 'shelter':
        return render(request, 'access_denied.html')

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('my_pets')
    else:
        form = PetForm(instance=pet)
    return render(request, 'edit_pet.html', {'form': form, 'pet': pet})

def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, pet_id=pet_id, shelter=request.user)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, "Pet deleted successfully!")
        return redirect('my_pets')
    return render(request, 'delete_pet_confirm.html', {'pet': pet})

@login_required
def my_pets(request):
    if request.user.user_type != 'shelter':
        return render(request, 'access_denied.html')

    pets = Pet.objects.filter(shelter=request.user)
    return render(request, 'my_pets.html', {'pets': pets})




from django.shortcuts import render, redirect
from .models import Pet


def view_pets(request):
    query = request.GET.get('search', '')
    if query:
        pets = Pet.objects.filter(name__icontains=query)
    else:
        pets = Pet.objects.all()
    return render(request, 'view_pets.html', {'pets': pets, 'query': query})
from django.contrib import messages

def adopt_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    
    # Optionally: create an AdoptionRequest
    # AdoptionRequest.objects.create(adopter=request.user, pet=pet)

    messages.success(request, f"You requested to adopt {pet.name}!")
    return redirect('view_pets')


from .models import Pet, AdoptionRequest

def request_adoption(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        AdoptionRequest.objects.create(pet=pet, adopter=request.user)
        messages.success(request, f"Adoption request sent for {pet.name}.")
        return redirect('view_pets')
    return render(request, 'request_adoption.html', {'pet': pet})
