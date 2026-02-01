from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    ]
    #role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    role = models.CharField(max_length=20)
    pesel = models.CharField(max_length=11, unique=True)
    sex = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    phone_number = models.CharField(max_length=15)

    # Pola dla lekarzy
    specialization = models.CharField(max_length=100)
    accepts_children = models.BooleanField(default=False)
    languages = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)

    # Pola dla pacjentów
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        db_table = 'users'