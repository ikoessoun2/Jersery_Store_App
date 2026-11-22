from pathlib import Path
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import mimetypes

DOCS_ROOT = (Path(settings.BASE_DIR) / "static" / "docs").resolve()

@api_view(["GET"])
@permission_classes([AllowAny])
def home(request):
    index_file = Path(settings.BASE_DIR) / "static" / "dist" / "index.html"
    return FileResponse(index_file.open("rb"), content_type="text/html")

@api_view(["GET"])
@permission_classes([AllowAny])
def official_docs(request, page="index.html"):
    file_path = (DOCS_ROOT / page).resolve()

    # Prevent directory traversal
    if not file_path.is_relative_to(DOCS_ROOT):
        raise Http404

    # Resolve directory URLs to their index.html
    if file_path.is_dir():
        file_path = file_path / "index.html"

    if not file_path.is_file():
        raise Http404

    content_type, _ = mimetypes.guess_type(file_path)

    return FileResponse(
        open(file_path, "rb"),
        content_type=content_type or "application/octet-stream",
    )