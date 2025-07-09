from django.core.management.base import BaseCommand
from zooner.models import Town
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Generate 20 major towns in Kenya'

    def handle(self, *args, **kwargs):
        towns_data = [
            {"name": "Nairobi", "region": "Nairobi", "lat": -1.286389, "lon": 36.817223},
            {"name": "Mombasa", "region": "Coast", "lat": -4.043477, "lon": 39.668206},
            {"name": "Kisumu", "region": "Nyanza", "lat": -0.091703, "lon": 34.767956},
            {"name": "Nakuru", "region": "Rift Valley", "lat": -0.303099, "lon": 36.080025},
            {"name": "Eldoret", "region": "Rift Valley", "lat": 0.520360, "lon": 35.269779},
            {"name": "Thika", "region": "Central", "lat": -1.033262, "lon": 37.069327},
            {"name": "Naivasha", "region": "Rift Valley", "lat": -0.716667, "lon": 36.433334},
            {"name": "Machakos", "region": "Eastern", "lat": -1.516667, "lon": 37.266667},
            {"name": "Nyeri", "region": "Central", "lat": -0.420130, "lon": 36.947601},
            {"name": "Meru", "region": "Eastern", "lat": 0.047035, "lon": 37.649803},
            {"name": "Kakamega", "region": "Western", "lat": 0.282730, "lon": 34.751866},
            {"name": "Kericho", "region": "Rift Valley", "lat": -0.368333, "lon": 35.283333},
            {"name": "Bungoma", "region": "Western", "lat": 0.563222, "lon": 34.560596},
            {"name": "Embu", "region": "Eastern", "lat": -0.538888, "lon": 37.450000},
            {"name": "Narok", "region": "Rift Valley", "lat": -1.078056, "lon": 35.860556},
            {"name": "Voi", "region": "Coast", "lat": -3.396667, "lon": 38.556667},
            {"name": "Lamu", "region": "Coast", "lat": -2.271744, "lon": 40.902046},
            {"name": "Isiolo", "region": "Eastern", "lat": 0.354621, "lon": 37.582184},
            {"name": "Nanyuki", "region": "Central", "lat": 0.0061, "lon": 37.0739},
            {"name": "Kitui", "region": "Eastern", "lat": -1.3750, "lon": 38.0150},
        ]

        created = 0
        skipped = 0

        for town in towns_data:
            slug = slugify(town["name"])
            obj, created_flag = Town.objects.get_or_create(
                name=town["name"],
                defaults={
                    "slug": slug,
                    "region": town["region"],
                    "latitude": town["lat"],
                    "longitude": town["lon"],
                    "country": "Kenya",
                    "is_active": True
                }
            )
            if created_flag:
                created += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created} towns created, {skipped} already existed."))
