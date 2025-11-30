from django.urls import path
from django.http import FileResponse, Http404
import os
def index(request):
    base = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'frontend')
    fp = os.path.join(base, 'index.html')
    try:
        return FileResponse(open(fp,'rb'))
    except Exception:
        raise Http404
urlpatterns = [path('', index)]
