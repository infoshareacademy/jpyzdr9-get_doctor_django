from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.views.generic import RedirectView
from patients_login.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-doctor/', include('registrations_visit.urls')),
    path('rezerwacje/', include('booking.urls')),
    path('home-home', HomeView.as_view(), name='home'),
    path('logowanie-pacjenta/', include('patients_login.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)