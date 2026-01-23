from django import forms
from user.models import User

class DoctorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['photo']