from django.shortcuts import render, redirect
from user.models import User
from .models import Post, TimeSlot
from .forms import DoctorForm
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
        'today': timezone.now(),  # <-- передаём дату в шаблон
    }
    return render(request, 'registrations_visit/home_page.html', context)

def general_info(request):
    return render(request, 'registrations_visit/general_informations.html', {} )

def login(request):
    return render(request, 'registrations_visit/login.html', {})

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


def upload_doctor_photo(request, doctor_id):
    try:
        doctor = User.objects.get(id=doctor_id)
    except User.DoesNotExist:
        from django.http import Http404
        raise Http404("Doctor not found")

    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_profile', specialization=doctor.specialization, doctor_id=doctor.id)
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'registrations_visit/upload_photo/upload_photo.html', {'form': form, 'doctor': doctor})


class PostListView(ListView):
    model = Post
    template_name = 'registrations_visit/news/post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(is_published=True).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post
    template_name = 'registrations_visit/news/post_detail.html'
    context_object_name = 'post'

# class HomeView(TemplateView):
#     template_name = "registrations_visit/home_page.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['random_posts'] = Post.objects.filter(is_published=True)
#         print("DEBUG HomeView called", list(context['random_posts']))
#         return context

# class RandomPostView(TemplateView):
#     template_name = "registrations_visit/news/post_random.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # берём все опубликованные новости
#         posts = list(Post.objects.filter(is_published=True))
#         # выбираем 1 случайную новость (если есть)
#         if posts:
#             context['random_post'] = random.choice(posts)
#         else:
#             context['random_post'] = None
#         return context

class DoctorSlotsView(LoginRequiredMixin, ListView):
    model = TimeSlot
    template_name = 'registrations_visit/doctor_detail.html'
    context_object_name = 'slots'
    ordering = ['start_datetime']