from django.shortcuts import render

# Create your views here.
from pathlib import Path
from django.conf import settings
from django.http import FileResponse

def home(request):
    index_file = Path(settings.BASE_DIR) / "static"/ "dist" / "index.html"
    return FileResponse(open(index_file, "rb"))