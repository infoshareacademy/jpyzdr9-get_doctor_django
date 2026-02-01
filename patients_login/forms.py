from django import forms
from user.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=False, label='Telefon')

    class Meta:
        model = User
        fields = ['date_of_birth', 'address', 'emergency_contact', 'blood_type', 'allergies']
        labels = {
            'date_of_birth': 'Data urodzenia',
            'address': 'Adres',
            'emergency_contact': 'Kontakt awaryjny',
            'blood_type': 'Grupa krwi',
            'allergies': 'Alergie',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone_number'].initial = self.instance.phone_number

    def save(self, commit=True):
        user = super().save(commit=False)


        user.phone_number = self.cleaned_data.get('phone_number')

        if commit:
            user.save()

        return user
