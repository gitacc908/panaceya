import json
from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from .models import VisitEvent


def get_visit_dashboard_data(days: int = 30, top_countries: int = 8) -> dict:
	since = timezone.now() - timedelta(days=days)
	base_qs = VisitEvent.objects.filter(visited_at__gte=since)

	total_visits = base_qs.count()
	unique_visitors = base_qs.values("ip_address").distinct().count()
	today = timezone.localdate()
	today_visits = VisitEvent.objects.filter(visited_at__date=today).count()

	by_day = list(
		base_qs.annotate(day=TruncDate("visited_at"))
		.values("day")
		.annotate(total=Count("id"))
		.order_by("day")
	)
	day_labels = [item["day"].isoformat() for item in by_day]
	day_values = [item["total"] for item in by_day]

	countries = list(
		base_qs.values("country_name", "country_code")
		.annotate(total=Count("id"))
		.order_by("-total", "country_name")[:top_countries]
	)
	country_labels = [
		(item["country_name"] or "Unknown") + (f" ({item['country_code']})" if item["country_code"] else "")
		for item in countries
	]
	country_values = [item["total"] for item in countries]

	return {
		"days": days,
		"total_visits": total_visits,
		"unique_visitors": unique_visitors,
		"today_visits": today_visits,
		"top_countries": countries,
		"chart_day_labels_json": json.dumps(day_labels),
		"chart_day_values_json": json.dumps(day_values),
		"chart_country_labels_json": json.dumps(country_labels),
		"chart_country_values_json": json.dumps(country_values),
	}
