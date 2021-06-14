from django.db import models


class Model0(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    value = models.IntegerField(default=0)
