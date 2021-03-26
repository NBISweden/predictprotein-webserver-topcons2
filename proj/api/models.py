from django.db import models

# Create your models here.

class Entry(models.Model):
    jobid = models.CharField(max_length=100)
    submit_date = models.DateTimeField('date submitted')
    ip = models.CharField(max_length=100)

