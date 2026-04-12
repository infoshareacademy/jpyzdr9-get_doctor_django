from django.shortcuts import render, redirect
from .models import Post, TimeSlot
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
import logging
from django.utils import timezone
from datetime import datetime, timedelta, time


logger = logging.getLogger(__name__)
User = get_user_model()

def service_unavailable(request):
    logging.info(f"Service Unavailable: path={request.path}, user={request.user}")
    return render(request, 'registrations_visit/503.html', {})


def home_page(request):
    random_posts = Post.objects.filter(is_published=True).order_by('?')[:4]
    context = {
        'random_posts': random_posts,
    }
    logging.debug(f"Home page opened by user: {request.user}")
    return render(request, 'registrations_visit/home.html', context)


def general_info(request):
    logging.info(f"Service Unavailable: path={request.path}, user={request.user}")
    return render(request, 'registrations_visit/general_information.html', {} )


def specializations_list(request):
    logging.debug(f"Specializations list viewed by user {request.user}")
    return render(request, 'registrations_visit/specializations_list.html')


def select_spec(request, specialization):
    doctors = User.objects.filter(
        specialization__iexact=specialization,
        role='doctor'
    )

    plural_map = {
                'chirurg': 'chirurdzy',
                'stomatolog': 'stomatolodzy',
                'onkolog': 'onkolodzy',
                'neurolog': 'neurolodzy',
                'dermatolog': 'dermatolodzy',
                'pediatra': 'pediatrzy',
                'kardiolog': 'kardiolodzy',
    }

    now = timezone.now()
    today = now.date()
    TOTAL_DAYS = 14
    DAYS_PER_PAGE = 7

    next_days = [today + timedelta(days=i) for i in range(TOTAL_DAYS)]

    WORK_START = time(8, 0)
    WORK_END = time(14, 0)
    SLOT_INTERVAL = timedelta(minutes=30)

    for doctor in doctors:
        page_param = f"page_{doctor.id}"
        page = int(request.GET.get(page_param, 0))

        start_index = page * DAYS_PER_PAGE
        end_index = start_index + DAYS_PER_PAGE
        visible_days = next_days[start_index:end_index]

        doctor.week_schedule = []

        for day in visible_days:
            day_slots = TimeSlot.objects.filter(
                doctor=doctor,
                start_datetime__date=day,
                is_booked=False
            ).order_by('start_datetime')

            doctor.week_schedule.append({
                'date': day,
                'slots': day_slots
            })

        doctor.current_page = page
        doctor.page_param = page_param
        doctor.max_page = (TOTAL_DAYS // DAYS_PER_PAGE) - 1

    context = {
        'specialization': specialization,
        'specialization_plural': plural_map.get(specialization, specialization),
        'doctors': doctors,
    }

    return render(request, 'registrations_visit/select_specializations.html', context)


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
    logging.debug(f"User opened doctor profile")