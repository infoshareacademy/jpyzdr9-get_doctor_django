from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from patients_login.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('patients_login/', include('patients_login.urls')),
    path('patients_registration/', include('patients_registration.urls')),
    path('get-doctor/', include('registrations_visit.urls')),
    path('rezerwacje/', include('booking.urls')),
    path('home-home', HomeView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
