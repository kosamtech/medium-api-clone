from django.urls import path

from .views import CustomerUserDetailsView

urlpatterns = [
    path("", CustomerUserDetailsView.as_view(), name="user-details"),
]
