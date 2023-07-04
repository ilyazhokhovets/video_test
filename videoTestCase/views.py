import json
from datetime import datetime

from django.shortcuts import render
from django.utils import timezone
from django.http import FileResponse
from .video_create import create_video
import mimetypes
import io
from django.conf import settings
from .models import Log

def runtest(request):
    print(request.GET)
    try:
        text = request.GET['text']
    except KeyError:
        text ='Default text, дефолтный текст'

    try:
        font = request.GET['font']
    except KeyError:
        font = None

    try:
        size = float(request.GET['size'])
    except (KeyError, ValueError):
        size = None

    filename = create_video(text, font, size)

    with open(f'{settings.BASE_DIR}/{filename}', 'rb') as f:
        file = f.read()
    file = io.BytesIO(file)
    mime_type, _ = mimetypes.guess_type(filename)
    response = FileResponse(file, content_type=mime_type,)
    response['Content-Disposition'] = f"attachment; filename={filename}"

    with open('videoTestCase/fonts.json', 'r') as f:
        font_settings = json.load(f)
        font = font or font_settings['font']
        size = size or font_settings['size']


    log = Log(text=text, request_date=timezone.now(), font=font, size=size)
    log.save()

    return response

def home(request):
    log_objs = Log.objects.all()
    queries = []
    for obj in log_objs:
        queries.append({
            'text_value': obj.text,
            'date': obj.request_date,
            'font': obj.font,
            'size': obj.size
        })
    return render(request, 'videoTestCase/main.html', context={'queries': queries,})
