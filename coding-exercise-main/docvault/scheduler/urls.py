from django.urls import path

from docvault.scheduler import views

urlpatterns = [
    path('mod', views.get_test_add)
]