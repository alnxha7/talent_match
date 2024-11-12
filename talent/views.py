from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Aspirants, Company, UserProfile, CompanyJobs, Applications
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'index.html')

def register_company(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        number = request.POST.get('number')
        url = request.POST.get('url')
        password = request.POST.get('password')
        logo = request.FILES.get('logo')

        # Validation checks
        if Company.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered for a company.')
            return redirect('register_company')
        
        user = User.objects.create(
            username=username,
            email=email,
            password=password  # Hash the password for security
        )

        UserProfile.objects.create(user=user, role='Company')
        
        company = Company(
            user=user,
            username=username,
            email=email,
            address=address,
            number=number,
            url=url,
            logo=logo
        )
        company.save()
        print('Company registered successfully.')
        return redirect('login') 

    return render(request, 'register_company.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('number')
        password = request.POST.get('password')
        image = request.FILES.get('image')

        try:
            user = User.objects.create(
            username=username,
            email=email,
            password=password  # Hash the password for security
        )
            
            UserProfile.objects.create(user=user, role='Aspirant')

            asp = Aspirants(
                user=user,
                username=username,
                email=email,
                phone_number=phone_number,  
                image=image
            )
            asp.save()
            print('Registration successful! You can now log in.')
            return redirect('login')  # Replace 'login' with your actual login URL name
        except ValidationError as e:
            print('Registration failed')
    
    return render(request, 'register_user.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Get the custom User model
        User = get_user_model()
        
        try:
            # Retrieve the user by email
            user = User.objects.get(email=email)
            
            # Check if the password is correct
            if (password==user.password):
                # Log the user in
                login(request, user)
                
                # Check user role from UserProfile
                user_profile = UserProfile.objects.get(user=user)
                
                # Redirect based on role
                if user_profile.role == 'Aspirant':
                    return redirect('user_index')
                elif user_profile.role == 'Company':
                    company = Company.objects.get(user=user)
                    if company.approved:
                        return redirect('company_index')
                    else:
                        # Company not approved
                        return render(request, 'login.html', {'error': "Company approval pending."})
                else:
                    return render(request, 'login.html', {'error': "User role not recognized."})
            else:
                # Invalid password
                return render(request, 'login.html', {'error': "Invalid email or password."})
        
        except User.DoesNotExist:
            # User with this email does not exist
            return render(request, 'login.html', {'error': "User with this email does not exist."})
        
        except UserProfile.DoesNotExist:
            # User profile is missing
            return render(request, 'login.html', {'error': "User profile is missing."})

    # If not POST, render the login page
    return render(request, 'login.html')

def logout_user(request):
    logout(request)  # Django's built-in logout function
    return redirect('home')

@login_required
def user_index(request):
    return render(request, 'user_index.html')

@login_required
def company_index(request):
    return render(request, 'company_index.html')

@login_required
def view_jobs(request):
    if request.method == 'POST':
        resume = request.FILES.get('resume')

        jobs=CompanyJobs.objects.all()
        return render(request, 'view_jobs.html', {'jobs': jobs})
    
    return render(request, 'view_jobs.html')

@login_required
def post_job(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        location=request.POST.get('location')
        description=request.POST.get('description')
        key_skills=request.POST.get('key_skills')

        company = get_object_or_404(Company, user=request.user)
        job = CompanyJobs(
            company=company,
            title=title,
            location=location,
            description=description,
            key_skills=key_skills
        )
        job.save()
        return render(request, 'post_job.html', {'success': 'Job Posted Succesfully...!!!'})

    return render(request, 'post_job.html')

@login_required
def company_jobs(request):
    company = get_object_or_404(Company, user=request.user)
    jobs = CompanyJobs.objects.filter(company=company)
    return render(request, 'company_jobs.html', {'jobs': jobs})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(CompanyJobs, id=job_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location')
        description = request.POST.get('description')
        key_skills = request.POST.get('key_skills')

        job.title = title
        job.location = location
        job.description = description
        job.key_skills = key_skills
        job.save()
        
        return redirect('company_jobs')
    return render(request, 'edit_job.html', {'job': job})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(CompanyJobs, id=job_id)
    if request.method == "POST":
        job.delete()
        return redirect('company_jobs')  
    return render(request, 'confirm_delete.html', {'job': job})

@login_required
def show_job(request, job_id):
    job = CompanyJobs.objects.get(id=job_id)
    return render(request, 'show_job.html', {'job': job})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(CompanyJobs, id=job_id)
    user = get_object_or_404(Aspirants, user=request.user)  # Get the Aspirant associated with the logged-in user
    company = job.company

    # Check if the application already exists
    application_exists = Applications.objects.filter(company=company, user=user, job=job).exists()
    if application_exists:
        # Display a message if the user has already applied
        return render(request, 'show_job.html', {
            'already_applied': 'You have already applied for this job.',
            'job': job
        })
    else:
        # Create a new application if not already applied
        Applications.objects.create(company=company, user=user, job=job)
        return render(request, 'show_job.html', {
            'success': 'You have successfully applied for this job!',
            'job': job
        })