from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .forms import  AdopterForm, ShelterForm, LoginForm, PetForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from .models import Register, Pet, AdoptionRequest, Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count

def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def services(request):
    return render(request, 'service.html')

def register_adopter(request):
    return HttpResponse("Adopter Registration Page")
def register_shelter(request):
     return HttpResponse("Shelter Registration Page")
def login_view(request):
    return HttpResponse("Login Page")


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


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request, f"Welcome {user.username}!")
                if user.is_superuser:
                    user.user_type ='admin'
                    user.save()
                request.session['ut'] = user.user_type
                if user.user_type == 'admin':
                    return redirect('/')   
                elif user.user_type == 'adopter':
                    return redirect('/') 
                elif user.user_type == 'shelter':
                    return redirect('/') 
                else:
                    return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def do_logout(request):
    logout(request)
    if 'ut' in request.session:
        del request.session['ut']
    messages.success(request, "You have successfully logged out.")
    return redirect('do_login')  

def manage_adopters(request):
    if request.user.user_type != 'admin':
        return render(request, 'access_denied.html')
    adopters = Register.objects.filter(user_type='adopter')
    return render(request, 'manage_adopters.html', {'adopters': adopters})

def manage_shelters(request):
    if request.user.user_type != 'admin':
        return render(request, 'access_denied.html')
    shelters = Register.objects.filter(user_type='shelter')
    return render(request, 'manage_shelters.html', {'shelters': shelters})


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

def view_pets(request):
    query = request.GET.get('search', '')
    if query:
        pets = Pet.objects.filter(name__icontains=query)
    else:
        pets = Pet.objects.all()
    return render(request, 'view_pets.html', {'pets': pets, 'query': query})

def request_adoption(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        # Prevent the shelter from sending adoption requests for their own pets
        if request.user == pet.shelter:
            messages.warning(request, "You cannot adopt your own pet.")
            return redirect('view_pets')
        # Prevent duplicate requests
        existing = AdoptionRequest.objects.filter(pet=pet, adopter=request.user).first()
        if existing:
            messages.info(request, "You have already requested adoption for this pet.")
        else:
            AdoptionRequest.objects.create(pet=pet, adopter=request.user)
            pet.adopter = request.user
            pet.save()
           
            messages.success(request, f"Adoption request sent for {pet.name}.")
        return redirect('view_pets')
    
    return render(request, 'request_adoption.html', {'pet': pet})

def shelter_adoption_requests(request):
    if not request.user.is_authenticated:
        return redirect('login')
    adoption_requests = AdoptionRequest.objects.filter(pet__shelter=request.user).select_related('pet', 'adopter')
    return render(request, 'shelter_adoption_requests.html', {'adoption_requests': adoption_requests})

def update_adoption_status(request, request_id, status):
    """Shelter updates status step-by-step"""
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id, pet__shelter=request.user)
    allowed = ['Reviewing', 'Approved', 'Rejected', 'Adopted']
    if status not in allowed:
        messages.error(request, "Invalid status update.")
        return redirect('shelter_adoption_requests')
    # Logic for transitions
    if adoption_request.status == 'Applied' and status == 'Reviewing':
        adoption_request.status = 'Reviewing'
    elif adoption_request.status == 'Reviewing' and status in ['Approved', 'Rejected']:
        adoption_request.status = status
    elif adoption_request.status == 'Approved' and status == 'Adopted':
        adoption_request.status = 'Adopted'
        adoption_request.pet.adopted = True
        adoption_request.pet.save()
    else:
        messages.warning(request, "Invalid step transition.")
        return redirect('shelter_adoption_requests')
    adoption_request.save()
    messages.success(request, f"Request for {adoption_request.pet.name} marked as {status}.")
    return redirect('shelter_adoption_requests')

def my_adoptions(request):
    """Adopter sees their own adoption requests"""
    adoptions = AdoptionRequest.objects.filter(adopter=request.user).select_related('pet', 'pet__shelter')
    return render(request, 'my_adoptions.html', {'adoptions': adoptions})

def track_adoption_status(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, pk=request_id)
    context = {
        'adoption_request': adoption_request,
        'current_step': adoption_request.status,
        'pet_icon': adoption_request.pet.type
    }
    return render(request, 'track_adoption_status.html', context)


def profile(request):
    user = request.user.id
    profile = None
    profile, _ = Register.objects.get_or_create(id=user)
    return render(request, 'profile.html', {
        'user_obj': user,
        'profile': profile,
    })

def edit_profile(request):
    user = request.user.id
    profile, _ = Register.objects.get_or_create(id=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {
        'form': form,
    })


def chat_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    user = request.user
    messages = Message.objects.filter(pet=pet).order_by('timestamp')
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            # Determine receiver
            if user == pet.shelter:
                # Shelter -> send to last adopter
                last_adopter_msg = messages.filter(sender__user_type='adopter').last()
                if last_adopter_msg:
                    receiver = last_adopter_msg.sender
                else:
                    return redirect('chat_view', pet_id=pet.id)
            else:
                # Adopter -> send to shelter
                receiver = pet.shelter
            Message.objects.create(
                sender=user,
                receiver=receiver,
                pet=pet,
                content=content
            )
        return redirect('chat_view', pet_id=pet.id)

    return render(request, 'chat.html', {
        'pet': pet,
        'messages': messages,
        'user': user
    })

@login_required
def message_list(request):
    user = request.user
    messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).select_related('pet', 'sender', 'receiver')
    pet_ids = messages.values_list('pet_id', flat=True).distinct()
    pets = Pet.objects.filter(id__in=pet_ids)
    # Build a list of tuples (pet, last_message)
    pet_messages = []
    for pet in pets:
        last_msg = messages.filter(pet=pet).order_by('-timestamp').first()
        pet_messages.append((pet, last_msg))
    return render(request, 'message_list.html', {
        'pet_messages': pet_messages
    })


def admin_adoption_dashboard(request):
    counts = (
        AdoptionRequest.objects
        .values('status')
        .annotate(count=Count('status'))
    )
    statuses = ['Applied', 'Reviewing', 'Approved', 'Rejected', 'Adopted']
    counts_dict = {status: 0 for status in statuses}
    for c in counts:
        counts_dict[c['status'].capitalize()] = c['count']
    total_requests = sum(counts_dict.values())
    return render(request, 'admin_adoption_dashboard.html', {
        'counts': counts_dict,
        'total_requests': total_requests
    })

def admin_adoption_list(request):
    adoption_requests = AdoptionRequest.objects.all().order_by('status')
    context = {
        'adoption_requests': adoption_requests,
    }
    return render(request, 'admin_adoption_list.html', context)

def confirm_delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, pet_id=pet_id)
    # Render the confirmation template (your existing "Are you sure?" template)
    return render(request, 'delete_pet_confirm.html', {'pet': pet})
