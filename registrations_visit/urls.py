from django.urls import path
from .views import (home_page, general_info, menu_reservations,
                    select_spec, doctor_profile,
                    specializations_list, PostListView, PostDetailView, DoctorSlotsView)


urlpatterns = [
    path('home-page/', home_page, name='home_page'),
    path('general-informations/', general_info, name='general_informations'),
    path('menu-reservations/', menu_reservations, name='menu_reservations'),
    path('specializations-list/', specializations_list, name='specializations_list'),
    path('doctors/<str:specialization>/', select_spec, name='select_spec'),
    path('doctor/<str:specialization>/<int:doctor_id>/', doctor_profile, name='doctor_profile'),
    path('post/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    path('doctor-slots/<int:doctor_id>/', DoctorSlotsView.as_view(), name='doctor_detail'),



]

