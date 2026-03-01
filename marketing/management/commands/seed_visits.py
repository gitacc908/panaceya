import random
from datetime import timedelta

from django.db import OperationalError, close_old_connections
from django.core.management.base import BaseCommand
from django.utils import timezone

from marketing.models import IPGeoCache, VisitEvent


class Command(BaseCommand):
	help = "Генерирует тестовые посещения для аналитики"

	COUNTRIES = [
		("US", "United States"),
		("RU", "Russia"),
		("KZ", "Kazakhstan"),
		("KG", "Kyrgyzstan"),
		("UA", "Ukraine"),
		("DE", "Germany"),
		("TR", "Turkey"),
		("AE", "United Arab Emirates"),
	]

	PATHS = [
		"/",
		"/contacts/",
		"/deposits/",
		"/roadmap/",
		"/services/",
		"/faq/",
	]

	AGENTS = [
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
		"Mozilla/5.0 (Linux; Android 14) Chrome/122.0 Mobile",
		"Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) Safari/604.1",
	]

	def add_arguments(self, parser):
		parser.add_argument("--days", type=int, default=30, help="За сколько последних дней генерировать")
		parser.add_argument("--rows", type=int, default=3000, help="Сколько визитов создать")
		parser.add_argument("--clear", action="store_true", help="Удалить старые посещения перед генерацией")

	def handle(self, *args, **options):
		days = max(1, options["days"])
		rows = max(1, options["rows"])
		clear = options["clear"]

		if clear:
			VisitEvent.objects.all().delete()
			self.stdout.write(self.style.WARNING("Старые VisitEvent удалены."))

		now = timezone.now()
		pool_size = min(max(rows // 12, 40), 800)
		ip_pool = [self._random_public_ip() for _ in range(pool_size)]
		cache_rows = {}
		for ip in ip_pool:
			country_code, country_name = random.choices(self.COUNTRIES, weights=[35, 18, 14, 8, 7, 6, 7, 5], k=1)[0]
			cache_rows[ip] = IPGeoCache(
				ip_address=ip,
				country_code=country_code,
				country_name=country_name,
			)
		IPGeoCache.objects.bulk_create(
			cache_rows.values(),
			update_conflicts=True,
			unique_fields=["ip_address"],
			update_fields=["country_code", "country_name"],
		)

		chunk_size = 200
		created = 0
		while created < rows:
			batch = []
			for _ in range(min(chunk_size, rows - created)):
				ip = random.choice(ip_pool)
				country = cache_rows[ip]
				delta_seconds = random.randint(0, days * 24 * 60 * 60)
				visited_at = now - timedelta(seconds=delta_seconds)
				batch.append(
					VisitEvent(
						ip_address=ip,
						country_code=country.country_code,
						country_name=country.country_name,
						path=random.choices(self.PATHS, weights=[40, 12, 16, 11, 12, 9], k=1)[0],
						user_agent=random.choice(self.AGENTS),
						visited_at=visited_at,
					)
				)
			try:
				VisitEvent.objects.bulk_create(batch, batch_size=chunk_size)
			except OperationalError:
				close_old_connections()
				VisitEvent.objects.bulk_create(batch, batch_size=chunk_size)
			created += len(batch)

		self.stdout.write(self.style.SUCCESS(f"Готово: создано {rows} посещений за {days} дней."))

	@staticmethod
	def _random_public_ip() -> str:
		first = random.choice([8, 9, 11, 23, 31, 37, 45, 52, 54, 63, 66, 77, 78, 85, 91, 95, 103, 109, 141, 151, 172, 176, 178, 185, 188, 193, 194, 195, 212])
		return f"{first}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
