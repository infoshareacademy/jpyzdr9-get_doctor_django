from django.db import models
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="tytuł")
    content = models.TextField(verbose_name="treść")
    published_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='Opublikowany')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Autor",null=True, blank=True)

    def __str__(self):
        return self.title

class TimeSlot(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'}
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    is_booked = models.BooleanField(default=False)

    def clean(self):
        if not self.end_datetime:
            self.end_datetime = self.start_datetime + timedelta(minutes=30)
        if self.start_datetime >= self.end_datetime:
            raise ValidationError("Czas rozpoczęcia musi być wcześniejszy niż czas zakończenia.")

        overlapping = TimeSlot.objects.filter(
            doctor=self.doctor,
            start_datetime__lt=self.end_datetime,
            end_datetime__gt=self.start_datetime
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError("Ten przedział czasowy nakłada się na istniejący slot.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doctor.username} - {self.start_datetime} / {self.end_datetime}"

