from django.urls import path

from . import views

urlpatterns = [
    path("", views.LegalDocListView.as_view(), name="index"),
]
