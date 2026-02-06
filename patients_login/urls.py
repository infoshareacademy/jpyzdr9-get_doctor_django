from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'patient'

urlpatterns = [
    path('login/', views.PatientLoginView.as_view(), name='login'),
    path('logout/', views.PatientLogoutView.as_view(), name='logout'),
    path('profile/', views.PatientProfileView.as_view(), name='profile'),
    #path('appointments/', views.PatientAppointmentsView.as_view(), name='appointments'),
]

