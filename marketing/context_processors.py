from .models import ContactLink, ContactsPage


def global_contacts(request):
    return {
        "footer_contacts": ContactLink.objects.all()[:4],
        "global_contacts_page": ContactsPage.objects.first(),
    }
