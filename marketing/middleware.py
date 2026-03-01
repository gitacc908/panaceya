from datetime import timedelta

from django.utils import timezone

from .geo import resolve_country
from .models import VisitEvent


class VisitTrackingMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		self._track_request(request)
		return response

	@staticmethod
	def _should_track(request) -> bool:
		if request.method != "GET":
			return False
		path = request.path or ""
		if path.startswith("/admin") or path.startswith("/static/") or path.startswith("/media/"):
			return False
		return True

	def _track_request(self, request) -> None:
		if not self._should_track(request):
			return

		ip_address = self._extract_ip(request)
		if not ip_address:
			return

		now = timezone.now()
		dedupe_since = now - timedelta(minutes=30)
		if VisitEvent.objects.filter(
			ip_address=ip_address,
			path=request.path,
			visited_at__gte=dedupe_since,
		).exists():
			return

		country_code, country_name = resolve_country(ip_address)
		VisitEvent.objects.create(
			ip_address=ip_address,
			country_code=country_code,
			country_name=country_name,
			path=(request.path or "")[:255],
			user_agent=(request.META.get("HTTP_USER_AGENT", "") or "")[:500],
		)

	@staticmethod
	def _extract_ip(request) -> str:
		x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
		if x_forwarded_for:
			return x_forwarded_for.split(",")[0].strip()
		return (request.META.get("REMOTE_ADDR", "") or "").strip()
