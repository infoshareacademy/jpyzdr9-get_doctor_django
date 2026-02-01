from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')

    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {'fields': (
            'role','pesel','sex','phone_number',
            'specialization','accepts_children','languages','photo',
            'date_of_birth','address','emergency_contact','blood_type','allergies'
        )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role','pesel','sex','phone_number')}),
    )