from django.core.exceptions import ValidationError
from django.db import models


class SingletonModel(models.Model):
	class Meta:
		abstract = True

	def clean(self):
		super().clean()
		if not self.pk and self.__class__.objects.exists():
			raise ValidationError("Можно создать только одну запись этого типа.")


class HomePage(SingletonModel):
	hero_title = models.CharField(max_length=255)
	hero_subtitle = models.CharField(max_length=255)
	hero_cta_text = models.TextField()
	available_currencies = models.CharField(max_length=255)
	features_title = models.CharField(max_length=255, default="Преимущества")
	example_sites_title = models.CharField(max_length=255, default="Примеры сайтов")
	example_bots_title = models.CharField(max_length=255, default="Примеры ботов")

	class Meta:
		verbose_name = "Главная страница"
		verbose_name_plural = "Главная страница"

	def __str__(self):
		return "Контент главной страницы"


class FeatureBlock(models.Model):
	title = models.CharField(max_length=255)
	text = models.TextField()
	image = models.ImageField(upload_to="marketing/features/", blank=True, null=True)
	show_on_home = models.BooleanField(default=True)
	use_telegram_channel_link = models.BooleanField(default=False)
	telegram_link_label = models.CharField(max_length=255, blank=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name = "Блок преимуществ"
		verbose_name_plural = "Блоки преимуществ"
		ordering = ["order", "id"]

	def __str__(self):
		return self.title


class ExampleLink(models.Model):
	SITE = "site"
	BOT = "bot"
	TYPE_CHOICES = (
		(SITE, "Сайт"),
		(BOT, "Бот"),
	)

	link_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
	title = models.CharField(max_length=255)
	url = models.URLField()
	order = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name = "Пример ссылки"
		verbose_name_plural = "Примеры ссылок"
		ordering = ["link_type", "order", "id"]

	def __str__(self):
		return f"{self.get_link_type_display()}: {self.title}"


class ContactsPage(SingletonModel):
	title = models.CharField(max_length=255, default="Контакты")
	description = models.TextField(blank=True)
	telegram_channel_url = models.URLField(blank=True)

	class Meta:
		verbose_name = "Страница контактов"
		verbose_name_plural = "Страница контактов"

	def __str__(self):
		return "Настройки контактов"


class ContactLink(models.Model):
	MANAGER = "manager"
	SUPPORT = "support"
	OTHER = "other"
	ROLE_CHOICES = (
		(MANAGER, "Менеджер"),
		(SUPPORT, "Техническая поддержка"),
		(OTHER, "Другое"),
	)

	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=OTHER)
	title = models.CharField(max_length=255)
	url = models.URLField()
	description = models.TextField(blank=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name = "Контакт"
		verbose_name_plural = "Контакты"
		ordering = ["order", "id"]

	def __str__(self):
		return f"{self.get_role_display()}: {self.title}"


class DepositsPage(SingletonModel):
	title = models.CharField(max_length=255, default="Депозиты")
	big_text = models.TextField()
	total_deposits = models.CharField(max_length=255)

	class Meta:
		verbose_name = "Страница депозитов"
		verbose_name_plural = "Страница депозитов"

	def __str__(self):
		return "Настройки страницы депозитов"


class DepositForum(models.Model):
	page = models.ForeignKey(
		DepositsPage,
		on_delete=models.CASCADE,
		related_name="forums",
	)
	forum_name = models.CharField(max_length=255)
	forum_url = models.URLField()
	deposit_amount = models.CharField(max_length=255)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name = "Форум с депозитом"
		verbose_name_plural = "Форумы с депозитами"
		ordering = ["order", "id"]

	def __str__(self):
		return f"{self.forum_name} — {self.deposit_amount}"


class RoadmapItem(models.Model):
	DONE = "DONE"
	PLANNED = "PLANNED"
	STATUS_CHOICES = (
		(DONE, "Выполнено"),
		(PLANNED, "Запланировано"),
	)

	title = models.CharField(max_length=255)
	text = models.TextField()
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PLANNED)
	date_label = models.CharField(max_length=100, blank=True)
	order = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Пункт roadmap"
		verbose_name_plural = "Пункты roadmap"
		ordering = ["status", "order", "id"]

	def __str__(self):
		return self.title


class ServicesPage(SingletonModel):
	title = models.CharField(max_length=255, default="Услуги")
	intro_text = models.TextField(blank=True)

	class Meta:
		verbose_name = "Страница услуг"
		verbose_name_plural = "Страница услуг"

	def __str__(self):
		return "Настройки страницы услуг"


class ServiceItem(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name = "Услуга"
		verbose_name_plural = "Услуги"
		ordering = ["order", "id"]

	def __str__(self):
		return self.title


class FaqPage(SingletonModel):
	title = models.CharField(max_length=255, default="FAQ")
	intro_text = models.TextField(blank=True)

	class Meta:
		verbose_name = "Страница FAQ"
		verbose_name_plural = "Страница FAQ"

	def __str__(self):
		return "Настройки страницы FAQ"


class FaqItem(models.Model):
	question = models.CharField(max_length=255)
	answer = models.TextField()
	order = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name = "FAQ пункт"
		verbose_name_plural = "FAQ пункты"
		ordering = ["order", "id"]

	def __str__(self):
		return self.question
