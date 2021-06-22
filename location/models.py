from django.db import models


class Location(models.Model):
    LEVELS = (
        (0, 'Nation'),
        (1, 'Region'),
        (2, 'Council')
    )
    location_name = models.CharField(max_length=100, default='')
    location_code = models.CharField(max_length=100, default='')
    location_hfr_code = models.CharField(max_length=100, default='')
    location_level = models.PositiveIntegerField(choices=LEVELS, default=0)
    location_reference = models.CharField(max_length=150)

    class Meta:
        pass

    def __str__(self):
        return self.location_name
