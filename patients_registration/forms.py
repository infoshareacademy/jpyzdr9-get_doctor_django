from datetime import date
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from localflavor.pl.forms import PLPESELField

from notifications.emails import welcome_mail


User = get_user_model()


class PatientRegistrationForm(forms.ModelForm):
    pesel = PLPESELField(label='PESEL')
    first_name = forms.CharField(label='Imię', max_length=150)
    last_name = forms.CharField(label='Nazwisko', max_length=150)
    date_of_birth = forms.DateField(
        label='Data urodzenia',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

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
        fields = [
            'first_name',
            'last_name',
            'pesel',
            'date_of_birth',
            'email',
            'phone_number',
            'address',
            'username',
            'password1',
            'password2',
        ]

        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'pesel': 'PESEL',
            'date_of_birth': 'Data urodzenia',
            'email': 'E-mail',
            'phone_number': 'Numer telefonu',
            'address': 'Adres',
            'username': 'Nazwa użytkownika',
        }

        help_texts = {
            'username': 'Wpisz nazwę użytkownika, która będzie używana do logowania.',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Użytkownik o podanym adresie e-mail już istnieje')
        return email

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        pesel = cleaned_data.get('pesel')
        date_of_birth = cleaned_data.get('date_of_birth')

        if pass1 and pass2 and pass1 != pass2:
            self.add_error('password2', 'Hasła nie są identyczne!')

        if pass1:
            try:
                validate_password(pass1, self.instance)
            except forms.ValidationError as e:
                self.add_error('password1', e)

        if pesel and date_of_birth and len(pesel) == 11:
            year = int(pesel[0:2])
            month = int(pesel[2:4])
            day = int(pesel[4:6])

            if month > 20:
                year += 2000
                month -= 20
            else:
                year += 1900

            if date_of_birth != date(year, month, day):
                self.add_error('date_of_birth', 'Data urodzenia nie zgadza się z numerem PESEL!')
                self.add_error('pesel', 'Numer PESEL nie zgadza się z datą urodzenia!')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = 'patient'
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')

        if commit:
            user.save()
            welcome_mail(user)

        return user