from django.urls import path

from . import views

urlpatterns = [
    path("", views.LegalDocListView.as_view(), name="index"),
    path("upload/", views.upload, name="upload"),
    path('delete/<int:pk>', views.LegalDocDeleteView.as_view(), name="delete"),
]

