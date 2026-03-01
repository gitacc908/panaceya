import json
from urllib.error import URLError
from urllib.request import urlopen

from .models import IPGeoCache


def _fetch_country_from_api(ip_address: str) -> tuple[str, str]:
	url = f"https://ipwho.is/{ip_address}"
	try:
		with urlopen(url, timeout=0.8) as response:
			payload = json.loads(response.read().decode("utf-8"))
	except (URLError, TimeoutError, OSError, json.JSONDecodeError):
		return "", ""

	if not payload.get("success"):
		return "", ""

	country_code = (payload.get("country_code") or "").upper()
	country_name = payload.get("country") or ""
	return country_code[:2], country_name[:100]


def resolve_country(ip_address: str) -> tuple[str, str]:
	if not ip_address or not IPGeoCache.is_public_ip(ip_address):
		return "", ""

	cached = IPGeoCache.objects.filter(ip_address=ip_address).first()
	if cached:
		return cached.country_code, cached.country_name

	country_code, country_name = _fetch_country_from_api(ip_address)
	IPGeoCache.objects.create(
		ip_address=ip_address,
		country_code=country_code,
		country_name=country_name,
	)
	return country_code, country_name
