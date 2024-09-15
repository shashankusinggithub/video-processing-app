

import datetime
import re
import subprocess
import webvtt
from .models import *


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
