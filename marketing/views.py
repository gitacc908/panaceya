from django.shortcuts import render

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
	RoadmapPage,
	ServiceItem,
	ServicesPage,
)


def home_view(request):
	homepage = HomePage.objects.first()
	features = FeatureBlock.objects.filter(show_on_home=True)
	site_examples = ExampleLink.objects.filter(link_type=ExampleLink.SITE)
	bot_examples = ExampleLink.objects.filter(link_type=ExampleLink.BOT)
	contacts_page = ContactsPage.objects.first()

	return render(
		request,
		"marketing/home.html",
		{
			"homepage": homepage,
			"features": features,
			"site_examples": site_examples,
			"bot_examples": bot_examples,
			"contacts_page": contacts_page,
		},
	)


def contacts_view(request):
	contacts_page = ContactsPage.objects.first()
	contacts = ContactLink.objects.all()
	return render(
		request,
		"marketing/contacts.html",
		{
			"contacts_page": contacts_page,
			"contacts": contacts,
		},
	)


def deposits_view(request):
	deposits_page = DepositsPage.objects.first()
	forums = deposits_page.forums.all() if deposits_page else []
	return render(
		request,
		"marketing/deposits.html",
		{
			"deposits_page": deposits_page,
			"forums": forums,
		},
	)


def roadmap_view(request):
	roadmap_page = RoadmapPage.objects.first()
	items = RoadmapItem.objects.all()
	return render(
		request,
		"marketing/roadmap.html",
		{
			"roadmap_page": roadmap_page,
			"items": items,
		},
	)


def services_view(request):
	services_page = ServicesPage.objects.first()
	items = ServiceItem.objects.all()
	return render(
		request,
		"marketing/services.html",
		{
			"services_page": services_page,
			"items": items,
		},
	)


def faq_view(request):
	faq_page = FaqPage.objects.first()
	items = FaqItem.objects.all()
	return render(
		request,
		"marketing/faq.html",
		{
			"faq_page": faq_page,
			"items": items,
		},
	)

# Create your views here.
