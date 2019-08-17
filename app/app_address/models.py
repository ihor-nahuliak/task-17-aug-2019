from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UserAddress(models.Model):
    user = models.ForeignKey(
        User, related_name='addresses',
        on_delete=models.CASCADE)
    name = models.CharField(
        max_length=255)
    street_address = models.CharField(
        max_length=255)
    street_address_line2 = models.CharField(
        max_length=255, blank=True, null=True)
    zipcode = models.CharField(
        max_length=12, blank=True, null=True)
    city = models.CharField(
        max_length=64)
    state = models.CharField(
        max_length=64, blank=True, null=True)
    country = models.CharField(
        max_length=2)
    full_address = models.TextField(
        blank=True)

    class Meta:
        app_label = 'app_address'
