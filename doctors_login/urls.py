from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('login/', views.DoctorLoginView.as_view(), name='login'),
    path('logout/', views.DoctorLogoutView.as_view(), name='logout'),
    path('start/', views.DoctorDashboardView.as_view(), name='start'),
    path('profile/', views.DoctorProfileView.as_view(), name='profile'),
    path('profile/edit/', views.DoctorProfileEditView.as_view(), name='profile_edit'),
    path('office/', views.DoctorVisitsView.as_view(), name='visits'),
    path('office/<int:pk>/', views.DoctorAppointmentDetailView.as_view(), name='appointment_detail'),
]