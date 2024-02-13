from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('calculator.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('calculator.api.urls')),
]
