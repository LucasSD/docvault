from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from .forms import UserUploadForm
from .models import LegalDoc


class LegalDocListView(LoginRequiredMixin, generic.ListView):
    """Render a list of LegalDoc objects.
    """
    model = LegalDoc
    paginate_by = 8

    def get_queryset(self):
        """Override to return LegalDoc objects uploaded by current user.

        Returns:
            QuerySet: A list of LegalDoc objects.
        """
        return LegalDoc.objects.filter(user=self.request.user)


@login_required
def upload(request):
    """Render page and store LegalDoc model on POST.

    Args:
        request (HttpRequest): Basic HTTP request.

    Returns:
        HttpResponse: Includes blank form in context on GET.
    """
    form = UserUploadForm()
    if request.method == "POST":
        form = UserUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_conf = form.save(commit=False)
            upload_conf.doc = request.FILES["doc"]
            upload_conf.user = request.user
            upload_conf.save()
            return render(request, "documents/confirm_upload.html")
    else:
        context = {
            "form": form,
        }
        return render(request, "documents/user_upload.html", context)
