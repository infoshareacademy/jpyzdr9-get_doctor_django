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
            day_slots = []

                # Берем существующие слоты на этот день
            existing_slots = TimeSlot.objects.filter(
                doctor=doctor,
                start_datetime__date=day
            )
            existing_dict = {}

            for slot in existing_slots:
                local_dt = timezone.localtime(slot.start_datetime)
                existing_dict[local_dt.time()] = slot

            # Генерируем все слоты для рабочей смены с таймзоной
            current_time = timezone.make_aware(datetime.combine(day, WORK_START))
            end_time = timezone.make_aware(datetime.combine(day, WORK_END))

            while current_time < end_time:
                slot_time = current_time.time()
                if slot_time in existing_dict:
                    day_slots.append(existing_dict[slot_time])
                else:
                    day_slots.append(None)
                current_time += SLOT_INTERVAL

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