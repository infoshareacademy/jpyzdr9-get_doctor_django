from django.urls import path
from .views import (home_page, general_info,
                    select_spec, doctor_profile,
                    specializations_list, PostListView, PostDetailView, DoctorSlotsView, service_unavailable)

app_name = 'visit'

urlpatterns = [
    path('maintenance/', service_unavailable, name='service_unavailable'),
    path('strona-glowna/', home_page, name='home_page'),
    path('informacje-ogolne/', general_info, name='general_information'),
    path('lista-specjalizacji/', specializations_list, name='specializations_list'),
    path('lekarze/<str:specialization>/', select_spec, name='select_spec'),
    path('lekarz/<str:specialization>/<int:doctor_id>/', doctor_profile, name='doctor_profile'),
    path('lekarz/<int:doctor_id>/grafik/', DoctorSlotsView.as_view(), name='doctor_detail'),
    path('posty/', PostListView.as_view(), name='post_list'),
    path('posty/<int:pk>/', PostDetailView.as_view(), name='post_detail'),




]

