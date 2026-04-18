from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("zero-division/", views.zero_division, name="zero_division"),
    path("key-error/", views.key_error, name="key_error"),
    path("db-error/", views.db_error, name="db_error"),
    path("slow/", views.slow_endpoint, name="slow"),
    path("custom-error/", views.custom_error, name="custom_error"),
    path("user-context/", views.user_context, name="user_context"),
]
