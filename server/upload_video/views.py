from django.db.models import Count
from django.http import JsonResponse
from .models import SubtitleSearchIndex
from django.db.models import Q
from .models import Subtitle, SubtitleSearchIndex
import webvtt
import os
from pathlib import Path
import subprocess
from django.http import JsonResponse, HttpResponse
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import FileResponse
import os
from django.http import StreamingHttpResponse, HttpResponse, Http404
from .models import Video
import re
from .serializers import *


@csrf_exempt
def dump(request):
    # return HttpResponse("Done")
    now = datetime.datetime.now().timestamp()
    video_file = request.FILES["video_file"]
    title = request.POST.get('title', '')
    file_name = f'{now}_{title}'

    video = Video.objects.create(
        title=title, video_file=video_file,)
    extract_subtitles(
        video)
    serialize = VideoSerializer(video)
    return JsonResponse({"filename":
                         serialize.data['video_file'].lstrip("/videos/"), 'video_id': serialize.data['id']})


def get_subtitles(request, subtitle_id):
    # Assuming subtitles are stored in the "subtitles" directory
    subtitle = Subtitle.objects.get(pk=subtitle_id)
    serialize = SubtitleSerializer(subtitle)
    # return HttpResponse(file_path)
    file_path = serialize.data['subtitle_file']
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='text/vtt')
    else:
        return JsonResponse({"error": "Subtitles not found"}, status=404)


def search_subtitle(request):
    """
    Search for a phrase in the subtitle and return the matching phrases with timestamps.
    """
    query = request.GET.get('q', '').strip().lower()  # Case-insensitive search
    # Filter by subtitle if necessary
    subtitle_id = request.GET.get('subtitle_id')

    if not query:
        return JsonResponse({'error': 'Search query cannot be empty'}, status=400)

    # Perform case-insensitive search
    search_results = SubtitleSearchIndex.objects.filter(
        subtitle_id=subtitle_id,
        phrase__icontains=query
    ).values('phrase', 'timestamp')

    return JsonResponse({'results': list(search_results)})


def get_video(request, video_id):
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        raise Http404("Video not found")

    video_path = video.video_file.path
    file_size = os.path.getsize(video_path)
    range_header = request.headers.get('Range', '').strip()

    if range_header:
        # HTTP Range request - extract byte range
        range_match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if range_match:
            start = int(range_match.group(1))
            end = range_match.group(2)
            end = int(end) if end else file_size - 1
            length = end - start + 1

            response = StreamingHttpResponse(
                get_chunk(open(video_path, 'rb'), start), status=206, content_type='video/mp4'
            )
            response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
            response['Accept-Ranges'] = 'bytes'
            response['Content-Length'] = str(length)
        else:
            return HttpResponse(status=416)  # Range not satisfiable
    else:
        response = StreamingHttpResponse(
            open(video_path, 'rb'), content_type='video/mp4'
        )
        response['Content-Length'] = str(file_size)

    return response


def extract_subtitles(video):
    try:
        video_file = video.video_file.path
        # Step 1: Get the available subtitle streams
        cmd = ['ffmpeg', '-i', video_file]
        process = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        output = process.stderr

        # Step 2: Find all subtitle streams (regex to match subtitles and their languages)
        pattern = r'Stream #0:(\d+)(?:\[\w+\])?\((\w{3})\): Subtitle: \w+'

        subtitle_streams = re.findall(
            pattern, output)

        if not subtitle_streams:
            print("No subtitles found in the video.")
            video.delete()
            raise Exception("No subtitles found in the video.")

        # Step 3: Extract each subtitle stream and save as .vtt
        for ind, (stream_index, lang) in enumerate(subtitle_streams):
            if not lang:
                lang = 'unknown'
            now = datetime.datetime.now().timestamp()

            output_file = f'{video_file}_{now}_{lang}.vtt'
            cmd = [
                'ffmpeg', '-i', video_file, "-y",
                '-map', f'0:s:{ind}?', '-c:s', 'webvtt', output_file
            ]
            try:
                subprocess.run(cmd, check=True)
                print(f"Extracted  {lang} to {output_file}")

                subtitle = Subtitle.objects.create(
                    video=video,
                    language=lang,
                    subtitle_file=output_file
                )
                create_search_index(subtitle)
            except subprocess.CalledProcessError as e:
                print(f"Error extracting  {stream_index}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")


def create_search_index(subtitle):
    """
    Parses the WebVTT subtitle file using the webvtt library and creates search indices
    based on phrases and timestamps.
    """

    # Parse the VTT file using webvtt
    for caption in webvtt.read(subtitle.subtitle_file):
        start_seconds = convert_timestamp_to_seconds(caption.start)

        # Save each phrase and its corresponding timestamp to the database
        SubtitleSearchIndex.objects.create(
            subtitle=subtitle, phrase=caption.text.strip(), timestamp=start_seconds
        )


def convert_timestamp_to_seconds(timestamp):
    """
    Converts a VTT timestamp (HH:MM:SS.mmm) to seconds.
    """
    hours, minutes, seconds = timestamp.split(':')
    seconds, milliseconds = seconds.split('.')
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + \
        int(seconds) + int(milliseconds) / 1000
    return total_seconds


def get_chunk(file, start, size=8192):
    file.seek(start)
    while True:
        data = file.read(size)
        if not data:
            break
        yield data


def list_videos(request):
    """
    List all uploaded videos with their titles and the array of available languages.
    """
    # Fetch distinct video files and their associated languages
    videos = Video.objects.all()

    # Prepare the list of videos with title and array of languages
    video_list = []

    for video in videos:
        # Get all languages for the current video
        languages = video.subtitle_languages
        all_langs = []

        for lang_obj in languages:
            lang = SubtitleSerializer(lang_obj)
            all_langs.append(
                {'language': lang.data['language'], "id": lang.data["id"]})

        video_list.append({
            'id': video.id,
            'title': video.title.split('/')[-1],
            'uploaded_at': video.uploaded_at,
            "subtitle_ids": all_langs
        })
    return JsonResponse({'videos': video_list})
