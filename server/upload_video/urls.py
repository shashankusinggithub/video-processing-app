# server/app/urls.py

from django.urls import path, include
from .views import dump, get_subtitles, get_video, list_videos, search_subtitle


urlpatterns = [
    path('upload/', dump),
    path('subtitles/<str:subtitle_id>/', get_subtitles, name='get_subtitles'),
    path('videos/<str:video_id>/', get_video, name='video-stream'),
    path('videos/', list_videos, name='list_videos'),
    path('search-subtitles/', search_subtitle, name='search_query')

]
