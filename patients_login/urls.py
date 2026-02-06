from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('login/', views.PatientLoginView.as_view(), name='login'),
    path('logout/', views.PatientLogoutView.as_view(), name='logout'),
    path('profile/', views.PatientProfileView.as_view(), name='profile'),

]

