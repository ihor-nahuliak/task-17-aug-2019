from django.db import models, IntegrityError
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

    def _get_duplicates_queryset(self):
        """Here we form a queryset
        to find not full filled addresses.

        e.g. we match these values as
        not full filled or duplicated:
        +------------------+------------------+
        | old stored value | new value        |
        +------------------+------------------+
        | "Max"            | "Max Mustermann" |
        | "Mustermann"     | "Max Mustermann" |
        | "Max Mustermann" | "Max Mustermann" |
        | ""               | "Max Mustermann" |
        | None             | "Max Mustermann" |
        +------------------+------------------+

        :rtype: models.QuerySet
        """
        name__tags = (self.name or '').split(' ')
        if self.name:
            name__tags.append(self.name)

        street_address__tags = (self.street_address or '').split(' ')
        if self.street_address:
            street_address__tags.append(self.street_address)

        street_address2__tags = (self.street_address_line2 or '').split(' ')
        if self.street_address_line2:
            street_address2__tags.append(self.street_address_line2)

        zip_code__tags = (self.zipcode or '').split(' ')
        if self.zipcode:
            zip_code__tags.append(self.zipcode)

        city__tags = (self.city or '').split(' ')
        if self.city:
            city__tags.append(self.city)

        state__tags = (self.state or '').split(' ')
        if self.state:
            state__tags.append(self.state)

        country__tags = (self.country or '').split(' ')
        if self.country:
            country__tags.append(self.country)

        q = self.__class__.objects.filter(
            models.Q(
                user_id=self.user_id
            ) &
            (
                models.Q(name__in=name__tags) |
                models.Q(name='') |
                models.Q(name__isnull=True)
            ) &
            (
                models.Q(street_address__in=street_address__tags) |
                models.Q(street_address='') |
                models.Q(street_address__isnull=True)
            ) &
            (
                models.Q(street_address_line2__in=street_address2__tags) |
                models.Q(street_address_line2='') |
                models.Q(street_address_line2__isnull=True)
            ) &
            (
                models.Q(zipcode__in=zip_code__tags) |
                models.Q(zipcode='') |
                models.Q(zipcode__isnull=True)
            ) &
            (
                models.Q(city__in=city__tags) |
                models.Q(city='') |
                models.Q(city__isnull=True)
            ) &
            (
                models.Q(state__in=state__tags) |
                models.Q(state='') |
                models.Q(state__isnull=True)
            ) &
            (
                models.Q(country__in=country__tags) |
                models.Q(country='') |
                models.Q(country__isnull=True)
            )
        )
        return q

    def _deduplicate(self):
        q = self._get_duplicates_queryset()
        duplicates = list(q[:2].all())
        if not self.pk and len(duplicates) == 1:
            self.pk = duplicates[0].pk
        elif duplicates:
            raise IntegrityError('address duplicated error')

    def save(self, *args, **kwargs):
        # It puts None values to the full_address,
        # but I didn't change that task logic.
        streetdata = f'{self.street_address}\n{self.street_address_line2}'
        self.full_address = (f'{streetdata}\n{self.zipcode} {self.city} '
                             f'{self.state} {self.country}')
        self._deduplicate()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'app_address'
