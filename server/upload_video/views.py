from .models import *
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse, HttpResponse, Http404, FileResponse, JsonResponse
import re
from .serializers import *
from django.views.decorators.http import require_POST, require_GET
from .utils import *


@csrf_exempt
@require_POST
def dump(request):
    # return HttpResponse("Done")
    video_file = request.FILES["video_file"]
    title = request.POST.get('title', '')

    video = Video.objects.create(
        title=title, video_file=video_file,)
    extract_subtitles(
        video)
    serialize = VideoSerializer(video)
    return JsonResponse({"filename":
                         serialize.data['video_file'].lstrip("/videos/"), 'video_id': serialize.data['id']})


@require_GET
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


@require_GET
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


@require_GET
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


@require_GET
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
