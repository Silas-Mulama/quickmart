from accounts.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from orders.models import Order
from products.models import Product
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


# -------------------------
# REGISTER
# -------------------------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Ensure profile exists (signals will handle this too)
            Profile.objects.get_or_create(user=user)

            # Send email to admin (optional)
            try:
                send_mail(
                    subject='🧑‍💻 New User Registration',
                    message=f"""
A new user has registered:

Username: {user.username}
Full Name: {user.first_name} {user.last_name}
Email: {user.email}
""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['team.eduquestm.com@gmail.com'],
                    fail_silently=True,
                )
            except Exception as e:
                print("Email send failed:", e)

            messages.success(request, "Registration successful. Please log in.")
            return redirect('login-user')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


# -------------------------
# LOGIN
# -------------------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('logged in')
            messages.success(request, f"Welcome {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'accounts/login.html')


# -------------------------
# LOGOUT
# -------------------------
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login-user')


# -------------------------
# PROFILE VIEW
# -------------------------
@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        profile.phone = request.POST['phone']

        user.save()
        profile.save()

        messages.success(request, "Your changes have been saved successfully!")
        return redirect('home')  # replace with your URL name

    return render(request, 'accounts/profile.html', {'profile': profile})


# -------------------------
# PROFILE EDIT
# -------------------------
@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



@login_required
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')


@login_required
def dashboard_redirect(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')
def about_pg(request):
    return render(request,'accounts/about.html')


def contact_pg(request):
    return render(request,'accounts/contact.html')
