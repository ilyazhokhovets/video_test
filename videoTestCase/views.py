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
    try:
        text = request.GET['text']
    except:
        text ='Hello world, Привет мир'

    filename = create_video(text)
    with open(f'{settings.BASE_DIR}/{filename}', 'rb') as f:
        file = f.read()
    file = io.BytesIO(file)
    mime_type, _ = mimetypes.guess_type(filename)
    response = FileResponse(file, content_type=mime_type,)
    response['Content-Disposition'] = f"attachment; filename={filename}"

    log = Log(text=text, request_date=timezone.now())
    log.save()
    return response

def home(request):
    return render(request, 'videoTestCase/main.html')