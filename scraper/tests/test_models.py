from django.test import TestCase
from scraper.models import ScrapedData
from django.core.management import call_command
from django.db import IntegrityError
from django.db import transaction


class ScrapedDataModelTest(TestCase):

    def test_create_scraped_data(self):
        data = ScrapedData.objects.create(
            title="Test Title",
            text="Test Description",
            img_url="http://example.com/image.jpg",
            source="Wikipedia"
        )

        self.assertEqual(ScrapedData.objects.count(), 1)
        self.assertEqual(data.title, "Test Title")


class ScrapedDataDuplicateTest(TestCase):

    def test_no_duplicate_entries(self):
        ScrapedData.objects.create(
            title="Titulo",
            text="Desc",
            img_url="url-imagen1",
            source="Wikipedia"
        )
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                ScrapedData.objects.create(
                    title="Titulo",
                    text="Desc 2",
                    img_url="url-imagen2",
                    source="Wikipedia"
                )

        self.assertEqual(ScrapedData.objects.count(), 1)


class ScraperCommandTest(TestCase):

    def test_scraper_command_runs(self):
        call_command("scraper_wiki")
        self.assertTrue(True)
