from django.contrib import admin
from .models import Post, TimeSlot

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'content')
    ordering = ('-published_date',)
    list_editable = ('is_published',)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'start_datetime', 'end_datetime', 'is_booked')
    list_filter = ('doctor', 'start_datetime', 'is_booked')
    exclude = ('is_booked',)