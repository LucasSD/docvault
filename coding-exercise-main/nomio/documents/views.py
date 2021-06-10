from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy

from .models import LegalDoc
from .forms import UserUploadForm
'''
@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "documents/index.html")'''

class LegalDocListView(generic.ListView):
    model = LegalDoc
    paginate_by = 8

    def get_queryset(self):
        # change this to filter for logged in User only?
        return LegalDoc.objects.all()

def upload(request):
    form = UserUploadForm()
    if request.method == 'POST':
        form = UserUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_conf = form.save(commit=False)
            upload_conf.doc = request.FILES['doc']
            upload_conf.save()
            return render(request, 'documents/confirm_upload.html', {'upload_conf': upload_conf})
    context = {"form": form,}
    return render(request, 'documents/user_upload.html', context)