# server/app/serializers.py

from rest_framework import serializers
from .models import Video, Subtitle, SubtitleSearchIndex


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id',  'title', 'video_file', 'uploaded_at']


class SubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtitle
        fields = ['id', 'video', 'language', 'subtitle_file']


class SubtitleSearchIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtitleSearchIndex
        fields = ['id', 'subtitle', 'phrase', 'timestamp']
