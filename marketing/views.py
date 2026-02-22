from django.shortcuts import redirect, render
from django.urls import reverse

from .models import (
	ContactLink,
	ContactsPage,
	DepositsPage,
	ExampleLink,
	FaqItem,
	FaqPage,
	FeatureBlock,
	HomePage,
	RoadmapItem,
	ServiceItem,
	ServicesPage,
)


def home_view(request):
	homepage = HomePage.objects.first()
	features = FeatureBlock.objects.filter(show_on_home=True)
	site_examples = ExampleLink.objects.filter(link_type=ExampleLink.SITE)
	bot_examples = ExampleLink.objects.filter(link_type=ExampleLink.BOT)
	contacts_page = ContactsPage.objects.first()
	contacts = ContactLink.objects.all()
	deposits_page = DepositsPage.objects.first()
	forums = deposits_page.forums.all() if deposits_page else []
	done_items = RoadmapItem.objects.filter(status=RoadmapItem.DONE).order_by("order", "id")
	planned_items = RoadmapItem.objects.filter(status=RoadmapItem.PLANNED).order_by("order", "id")
	items_all = [*done_items, *planned_items]
	services_page = ServicesPage.objects.first()
	service_items = ServiceItem.objects.all()
	faq_page = FaqPage.objects.first()
	faq_items = FaqItem.objects.all()

	return render(
		request,
		"marketing/home.html",
		{
			"homepage": homepage,
			"features": features,
			"site_examples": site_examples,
			"bot_examples": bot_examples,
			"contacts_page": contacts_page,
			"contacts": contacts,
			"deposits_page": deposits_page,
			"forums": forums,
			"done_items": done_items,
			"planned_items": planned_items,
			"items_all": items_all,
			"services_page": services_page,
			"service_items": service_items,
			"faq_page": faq_page,
			"faq_items": faq_items,
		},
	)


def contacts_view(request):
	return redirect(f"{reverse('marketing:home')}#contacts")


def deposits_view(request):
	return redirect(f"{reverse('marketing:home')}#deposits")


def roadmap_view(request):
	return redirect(f"{reverse('marketing:home')}#roadmap")


def services_view(request):
	return redirect(f"{reverse('marketing:home')}#services")


def faq_view(request):
	return redirect(f"{reverse('marketing:home')}#faq")

# Create your views here.
