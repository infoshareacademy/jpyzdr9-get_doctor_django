from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/get-doctor/home/', permanent=False), name='home'),
    path('patients_login/', include('patients_login.urls')),
    path('patients_registration/', include('patients_registration.urls')),
    path('get-doctor/', include('registrations_visit.urls')),
    path('booking/', include('booking.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
