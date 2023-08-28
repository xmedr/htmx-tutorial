from django.db import models  # noqa


class Task(models.Model):
    description = models.TextField()
