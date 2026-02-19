from django.urls import path

from .views import (
    contacts_view,
    deposits_view,
    faq_view,
    home_view,
    roadmap_view,
    services_view,
)

app_name = "marketing"

urlpatterns = [
    path("", home_view, name="home"),
    path("contacts/", contacts_view, name="contacts"),
    path("deposits/", deposits_view, name="deposits"),
    path("roadmap/", roadmap_view, name="roadmap"),
    path("services/", services_view, name="services"),
    path("faq/", faq_view, name="faq"),
]
