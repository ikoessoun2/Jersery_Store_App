from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
        path(
        "official-docs/",
        views.official_docs,
        name="official-docs",
    ),
    path(
        "official-docs/<path:page>",
        views.official_docs,
        name="official-docs-page",
    ),
]