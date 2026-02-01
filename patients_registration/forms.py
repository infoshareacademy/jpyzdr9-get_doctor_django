from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

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
    class Meta(BaseUserCreationForm.Meta):
        fields = BaseUserCreationForm.Meta.fields + [
            'date_of_birth',
            'address',
            'emergency_contact',
            'blood_type',
            'allergies',
        ]

        help_texts = {
            'username': None,
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'

        if commit:
            user.save()
        return user
