from django.urls import path
from .views import (home_page, general_info,
                    select_spec,
                    specializations_list, PostListView, PostDetailView, DoctorSlotsView, service_unavailable)

app_name = 'visit'

urlpatterns = [
    path('maintenance/', service_unavailable, name='service_unavailable'),
    path('home/', home_page, name='home_page'),
    path('general-info/', general_info, name='general_information'),
    path('specializations/', specializations_list, name='specializations_list'),
    path('doctors/<str:specialization>/', select_spec, name='select_spec'),
    path('doctor/<int:doctor_id>/schedule/', DoctorSlotsView.as_view(), name='doctor_detail'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),



]

