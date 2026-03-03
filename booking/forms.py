from django import forms
from .models import Appointment

class AppointmentDoctorForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor_notes']
        widgets = {
            'doctor_notes': forms.Textarea(attrs={
                'class': 'visit-textarea',
                'rows': 5,
                'placeholder': 'Wpisz notatki lekarza...'
            })
        }