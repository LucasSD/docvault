from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import DeleteView

from .forms import UserUploadForm
from .models import LegalDoc


class LegalDocListView(LoginRequiredMixin, generic.ListView):
    """Render a list of LegalDoc objects."""

    model = LegalDoc
    paginate_by = 8

    def get_queryset(self):
        """Override to return LegalDoc objects uploaded by current user.

        Returns:
            QuerySet: A list of LegalDoc objects.
        """
        return LegalDoc.objects.filter(user=self.request.user)


class LegalDocDeleteView(LoginRequiredMixin, DeleteView):
    """Delete selected instance from database."""

    model = LegalDoc
    success_url = "/documents/"


# conside changing to generic CreateView
@login_required
def upload(request):
    """Render page and store LegalDoc model on POST.

    Args:
        request (HttpRequest): Basic HTTP request.

    Returns:
        HttpResponse: Includes blank form in context on GET.
    """
    if request.method == "POST":
        form = UserUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist("doc"):
                obj = LegalDoc.objects.create(doc=f, user=request.user)
                for t in form.cleaned_data["tag"]:
                    obj.tag.add(t)
                obj.save()
            return render(request, "documents/confirm_upload.html")

    else:
        form = UserUploadForm()

    context = {
        "form": form,
    }
    return render(request, "documents/user_upload.html", context)
