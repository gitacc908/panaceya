from django.contrib import admin
from django.utils.html import format_html

from .models import (
	ContactLink,
	ContactsPage,
	DepositForum,
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


class SingletonAdminMixin:
	def has_add_permission(self, request):
		if self.model.objects.exists():
			return False
		return super().has_add_permission(request)


@admin.register(HomePage)
class HomePageAdmin(SingletonAdminMixin, admin.ModelAdmin):
	list_display = ("hero_title", "available_currencies")


@admin.register(FeatureBlock)
class FeatureBlockAdmin(admin.ModelAdmin):
	list_display = ("title", "image_preview", "show_on_home", "order")
	list_filter = ("show_on_home",)
	search_fields = ("title", "text")
	ordering = ("order", "id")

	@admin.display(description="Превью")
	def image_preview(self, obj):
		if not obj.image:
			return "—"
		return format_html('<img src="{}" style="height:48px;border-radius:8px;" />', obj.image.url)


@admin.register(ExampleLink)
class ExampleLinkAdmin(admin.ModelAdmin):
	list_display = ("title", "link_type", "url", "order")
	list_filter = ("link_type",)
	search_fields = ("title", "url")
	ordering = ("link_type", "order", "id")


@admin.register(ContactsPage)
class ContactsPageAdmin(SingletonAdminMixin, admin.ModelAdmin):
	list_display = ("title", "telegram_channel_url")


@admin.register(ContactLink)
class ContactLinkAdmin(admin.ModelAdmin):
	list_display = ("title", "role", "url", "order")
	list_filter = ("role",)
	search_fields = ("title", "description", "url")
	ordering = ("order", "id")


class DepositForumInline(admin.TabularInline):
	model = DepositForum
	extra = 1
	fields = ("forum_name", "forum_url", "deposit_amount", "order")
	ordering = ("order", "id")


@admin.register(DepositsPage)
class DepositsPageAdmin(SingletonAdminMixin, admin.ModelAdmin):
	list_display = ("title", "total_deposits")
	inlines = [DepositForumInline]


@admin.register(DepositForum)
class DepositForumAdmin(admin.ModelAdmin):
	list_display = ("forum_name", "deposit_amount", "order")
	search_fields = ("forum_name", "deposit_amount")
	ordering = ("order", "id")


@admin.register(RoadmapPage)
class RoadmapPageAdmin(SingletonAdminMixin, admin.ModelAdmin):
	list_display = ("title",)


@admin.register(RoadmapItem)
class RoadmapItemAdmin(admin.ModelAdmin):
	list_display = ("title", "status_label", "planned_date", "order")
	list_filter = ("status_label",)
	search_fields = ("title", "description")
	ordering = ("order", "id")


@admin.register(ServicesPage)
class ServicesPageAdmin(SingletonAdminMixin, admin.ModelAdmin):
	list_display = ("title",)


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
	list_display = ("title", "order")
	search_fields = ("title", "description")
	ordering = ("order", "id")


@admin.register(FaqPage)
class FaqPageAdmin(SingletonAdminMixin, admin.ModelAdmin):
	list_display = ("title",)


@admin.register(FaqItem)
class FaqItemAdmin(admin.ModelAdmin):
	list_display = ("question", "order")
	search_fields = ("question", "answer")
	ordering = ("order", "id")

# Register your models here.
