from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import CustomUserCreationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect(reverse("index"))
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request=request, template_name="landing/register.html", context={"form": CustomUserCreationForm})
