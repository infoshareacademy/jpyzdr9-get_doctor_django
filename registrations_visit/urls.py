from django.urls import path
from .views import (home_page, general_info,
                    select_spec, doctor_profile,
                    specializations_list, PostListView, PostDetailView, DoctorSlotsView, service_unavailable)

app_name = 'visit'

urlpatterns = [
    path('maintenance/', service_unavailable, name='service_unavailable'),
    path('home-page/', home_page, name='home_page'),
    path('general-information/', general_info, name='general_information'),
    path('specializations-list/', specializations_list, name='specializations_list'),
    path('doctors/<str:specialization>/', select_spec, name='select_spec'),
    path('doctor-profile/<str:specialization>/<int:doctor_id>/', doctor_profile, name='doctor_profile'),
    path('doctor-detail/<int:doctor_id>/grafik/', DoctorSlotsView.as_view(), name='doctor_detail'),
    path('post-list/', PostListView.as_view(), name='post_list'),
    path('post-detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),




]

