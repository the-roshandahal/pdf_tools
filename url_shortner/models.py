from django.db import models

# Create your models here.
import shortuuid

class URL(models.Model):
    long_url = models.URLField()
    short_url = models.CharField(max_length=50, unique=True)
    visited = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = shortuuid.uuid()[:3]
        super().save(*args, **kwargs)
