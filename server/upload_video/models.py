# server/app/models.py

import logging
from django.db import models


class Video(models.Model):

    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def subtitle_languages(self):
        """Returns a list of available languages for this video."""
        return self.subtitles.all()


class Subtitle(models.Model):
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="subtitles")
    language = models.CharField(max_length=20)  # e.g., "en" for English
    subtitle_file = models.CharField(max_length=200, default="/")

    def __str__(self):
        return f"{self.video.title} ({self.language})"


class SubtitleSearchIndex(models.Model):
    subtitle = models.ForeignKey(
        Subtitle, on_delete=models.CASCADE, related_name="search_indices")
    phrase = models.CharField(
        max_length=255, db_index=True)  # Searchable phrase
    timestamp = models.DecimalField(
        max_digits=10, decimal_places=2)  # Time in seconds

    def __str__(self):
        return f"{self.phrase} @ {self.timestamp}s"


logger = logging.getLogger(__name__)
