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

    def save(self, *args, **kwargs):
        # помечаем слот как занятый
        self.slot.is_booked = True
        self.slot.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.username} → {self.slot}"