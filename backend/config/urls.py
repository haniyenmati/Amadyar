from django.contrib import admin
from django.urls import path, include


admin.site.site_header = 'Amadyar Admin Panel'
admin.site.site_title = 'Amadyar'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('haul/', include('haul.urls', namespace='haul')),
]
