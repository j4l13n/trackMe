from django.contrib.gis.db import models
from trackme.apps.authentication.models import User


class Tracking(models.Model):
    """
    Tracking model to save user device data

    Attributes:
        user (str): user's id
        geometry (point): location base info (lon, lat)
        device (str): device id value
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    geometry = models.PointField(srid=4326, null=True, blank=True)
    device = models.CharField(max_length=100, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.device or ''
