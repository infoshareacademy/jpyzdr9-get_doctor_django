from django import forms
from .models import Appointment

class AppointmentNotesForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Dodaj notatki...'
            })
        }