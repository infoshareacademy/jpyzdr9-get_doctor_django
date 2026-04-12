from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    pesel = models.CharField(max_length=11, unique=True)
    sex = models.CharField(max_length=10, choices=[('M', 'Mężczyzna'), ('F', 'Kobieta')])
    phone_number = models.CharField(max_length=15)

    # Pola dla lekarzy
    specialization = models.CharField(max_length=100,blank=True)
    accepts_children = models.BooleanField(default=False)
    languages = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)

    # Pola dla pacjentów
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)

    def _set_sex_from_pesel(self):
        if self.pesel and len(self.pesel) == 11:
            gender_digit = int(self.pesel[9])
            self.sex = 'F' if gender_digit % 2 == 0  else 'M'

    def save(self, *args, **kwargs):
        self._set_sex_from_pesel()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        db_table = 'users'