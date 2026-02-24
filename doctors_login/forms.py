from django import forms
from user.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'phone_number',
            'specialization',
            'accepts_children',
            'languages',
            'photo'
        ]
        labels = {
            'phone_number': 'Telefon',
            'specialization': 'Specjalizacja',
            'accepts_children': 'Przyjmuje dzieci',
            'languages': 'Języki',
            'photo': 'Zdjęcie profilowe',
        }
        widgets = {
            'languages': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'np. Polski, Angielski, Niemiecki'
            }),
        }
        help_texts = {
            'accepts_children': 'Zaznacz jeśli przyjmujesz pacjentów poniżej 18 roku życia',
            'languages': 'Wpisz języki którymi się posługujesz, oddzielone przecinkami',
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '')

        if phone:
            phone = phone.replace(' ', '').replace('-', '')

            if not phone.replace('+', '').isdigit():
                raise forms.ValidationError('Numer telefonu może zawierać tylko cyfry i znak +')

            if len(phone) < 9:
                raise forms.ValidationError('Numer telefonu jest za krótki (min. 9 cyfr)')

        return phone

    def clean_specialization(self):
        spec = self.cleaned_data.get('specialization', '').strip()

        if not spec:
            raise forms.ValidationError('Specjalizacja jest wymagana dla lekarza')

        if len(spec) < 3:
            raise forms.ValidationError('Specjalizacja musi mieć minimum 3 znaki')

        return spec