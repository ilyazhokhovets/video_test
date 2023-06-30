from django.db import models

# Create your models here.
class Log(models.Model):
    text = models.CharField('text', max_length=255)
    request_date = models.DateTimeField()