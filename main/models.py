from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(
        'auth.User', related_name='devices', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
