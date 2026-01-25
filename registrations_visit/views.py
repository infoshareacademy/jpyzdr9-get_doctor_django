from django.shortcuts import render, redirect
from user.models import User
from .models import Post, TimeSlot
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


User = get_user_model()


def home_page(request):
    random_posts = Post.objects.filter(is_published=True).order_by('?')[:6]
    context = {
        'random_posts': random_posts,
        'today': timezone.now(),
    }
    return render(request, 'registrations_visit/home_page.html', context)

def general_info(request):
    return render(request, 'registrations_visit/general_informations.html', {} )

def menu_reservations(request):
    return render(request, 'registrations_visit/menu_reservations.html', {})

def specializations_list(request):
    specialization = request.GET.get('specialization')

    if specialization:
        return redirect('select_spec', specialization=specialization)

    return render(request, 'registrations_visit/specializations.html')

def select_spec(request, specialization):
    doctors = User.objects.filter(specialization__iexact=specialization)
    context = {
        'specialization': specialization,
        'doctors': doctors
    }
    return render(request, 'registrations_visit/select_spec.html', context)

def doctor_profile(request, specialization, doctor_id):
    doctor = get_object_or_404(User, id=doctor_id, specialization__iexact=specialization, role='doctor')
    slots = TimeSlot.objects.filter(doctor=doctor).order_by('start_datetime')

    context = {
        'doctor': doctor,
        'slots': slots
    }
    return render(request, 'registrations_visit/doctor_profile.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'registrations_visit/news/post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(is_published=True).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post
    template_name = 'registrations_visit/news/post_detail.html'
    context_object_name = 'post'


class DoctorSlotsView(LoginRequiredMixin, ListView):
    model = TimeSlot
    template_name = 'registrations_visit/doctor_detail.html'
    context_object_name = 'slots'
    ordering = ['start_datetime']