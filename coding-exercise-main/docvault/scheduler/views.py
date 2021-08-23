from django.http import HttpResponse
from rest_framework.decorators import api_view
from docvault.scheduler.task import mod

@api_view(['GET'])
def get_test_add(request):
    x, y = int(request.query_params.get('x')), int(request.query_params.get('y'))
    mod.apply_async(args=(x, y), countdown=20)
    return HttpResponse(f'Success !')
