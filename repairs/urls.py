from django.urls import path

from . import views


app_name = "repairs"

urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),
    path(
        "track/<str:tracking_code>/",
        views.ticket_detail,
        name="ticket_detail",
    ),
]