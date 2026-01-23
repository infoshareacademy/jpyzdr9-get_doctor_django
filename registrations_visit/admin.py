from django.contrib import admin
from .models import Post, TimeSlot
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_superuser',
    )

    list_filter = ('role', 'is_staff', 'is_superuser')

    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {
            'fields': (
                'role',
                'pesel',
                'sex',
                'phone_number',
                'specialization',
                'accepts_children',
                'languages',
                'photo',
                'date_of_birth',
                'address',
                'emergency_contact',
                'blood_type',
                'allergies',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': (
                'role',
                'pesel',
                'sex',
                'phone_number',
            )
        }),
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'content')
    ordering = ('-published_date',)
    list_editable = ('is_published',)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'start_datetime', 'is_booked')
    exclude = ('is_booked',)