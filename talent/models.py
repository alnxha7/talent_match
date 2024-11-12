from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Aspirant', 'Aspirant'),
        ('Company', 'Company'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    def __str__(self):
        return f"{self.user.email} - {self.role}"

class Aspirants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    image = models.ImageField(upload_to='user_images/')

    def __str__(self):
        return self.email
    
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    url = models.URLField()
    logo = models.ImageField(upload_to='company_logo/')
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.email 

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

class CompanyJobs(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    key_skills = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

    class Meta:
        verbose_name = "Company Job"
        verbose_name_plural = "Company Jobs"

class Applications(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(Aspirants, on_delete=models.CASCADE)
    job = models.ForeignKey(CompanyJobs, on_delete=models.CASCADE)