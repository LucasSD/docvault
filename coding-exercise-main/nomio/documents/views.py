from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy

from .models import LegalDoc

'''
@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "documents/index.html")'''

class LegalDocListView(generic.ListView):
    model = LegalDoc
    paginate_by = 7

    def get_queryset(self):
        # change this to filter for logged in User only
        return LegalDoc.objects.all()