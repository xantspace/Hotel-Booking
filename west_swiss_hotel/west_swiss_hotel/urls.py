from django.urls import path, include
from bookings.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('bookings.urls')),
]
