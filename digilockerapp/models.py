from django.db import models

# Create your models here.
class DocumentModel(models.Model):
    userid = models.IntegerField()
    title = models.TextField()
    file = models.FileField(upload_to='documents/')