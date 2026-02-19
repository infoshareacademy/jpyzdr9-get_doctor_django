from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from localflavor.pl.forms import PLPESELField
from notifications.emails import welcome_mail

User = get_user_model()

class BaseUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Hasło',
        widget=forms.PasswordInput,
        help_text='Minimum 8 znaków, wielka litera, cyfra i znak specjalny'
    )
    password2 = forms.CharField(
        label='Potwierdź hasło',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'pesel']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Hasła nie są identyczne!')

        validate_password(password1, self.instance)

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class PatientRegistrationForm(BaseUserCreationForm):
    first_name = forms.CharField(label='Imię', max_length=150)
    last_name = forms.CharField(label='Nazwisko', max_length=150)
    pesel = PLPESELField(label='PESEL')

    class Meta(BaseUserCreationForm.Meta):
        fields = [
            'username',
            'first_name',
            'last_name',
            'pesel',
            'password1',
            'password2',
            'date_of_birth',
            'address',
            'emergency_contact',
            'blood_type',
            'allergies',
            'email'
        ]

        labels = {
            'username': 'Nazwa użytkownika',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'pesel': 'PESEL',
            'password1': 'Hasło',
            'password2': 'Powtórz hasło',
            'date_of_birth': 'Data urodzenia',
            'address': 'Adres',
            'emergency_contact': 'Kontakt awaryjny',
            'blood_type': 'Grupa krwi',
            'allergies': 'Alergie',
            'email': 'E-mail',
        }

        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')

        if commit:
            user.save()
            welcome_mail(user)

        return user

