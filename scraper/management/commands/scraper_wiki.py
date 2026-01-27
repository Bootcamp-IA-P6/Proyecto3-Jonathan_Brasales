from django.core.management.base import BaseCommand
from scraper.models import ScrapedData
from scraper.services.scrape import scrape_website


class Command(BaseCommand):
    help = "Scrapea el Recurso del Día de Wikipedia"

    def handle(self, *args, **kwargs):
        self.stdout.write("🌐 Ejecutando scraper de Wikipedia...")

        data = scrape_website()

        obj, created = ScrapedData.objects.get_or_create(
            title=data["title"],
            source=data["source"],
            defaults={
                "text": data["text"],
                "img_url": data["img_url"],
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS("✅ Recurso guardado"))
        else:
            self.stdout.write("ℹ️ El recurso ya existía")
