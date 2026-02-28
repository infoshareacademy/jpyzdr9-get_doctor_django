from django.db import models
from django.conf import settings
from registrations_visit.models import TimeSlot

class Appointment(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'},
        related_name='appointments'
    )
    slot = models.OneToOneField(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name='appointment'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    doctor_notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.slot.is_booked = True
        self.slot.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.username} → {self.slot}"


class Service(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'},
        related_name='services'
    )
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} – {self.price} PLN ({self.doctor.get_full_name()})"