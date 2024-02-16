from django.db import models

class WatchedAnime(models.Model):
    title = models.CharField(max_length=100)
    site = models.CharField(max_length=100, null=True)
    rating = models.CharField(max_length=100)
    link = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title