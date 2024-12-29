from django.contrib import admin
from django.urls import path
from scrape_management.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('AlertTentant/', AlertRequest.as_view()),
    path('WatchdogFailure/', AlertClientError.as_view()),
]