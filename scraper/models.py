from django.db import models

# Create your models here.
class ScrapedData(models.Model):


    title = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField()
    img_url = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=100, default="Wikipedia")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("title", "source")

    def __str__(self):
        return self.title