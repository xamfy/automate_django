from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=20)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name
