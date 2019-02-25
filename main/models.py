from django.db import models
from asgiref.sync import async_to_sync
from model_utils import FieldTracker

from channels.layers import get_channel_layer


async def update_device(instance):
    print(instance.owner)
    group_name = 'room_'+str(instance.owner)
    channel_layer = get_channel_layer()
    await channel_layer.group_send(group_name, {
        # This "type" defines which handler on the Consumer gets
        # called.
        "type": "device_status",
        "text": {
            'name': instance.name,
            'status': instance.status
        },
    })


class Device(models.Model):
    tracker = FieldTracker(fields=("status",))
    name = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(
        'auth.User', related_name='devices', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        has_changed = self.tracker.has_changed("status")
        if has_changed:
            async_to_sync(update_device)(self)
        return ret

    def __str__(self):
        return self.name
