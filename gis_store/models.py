from django.db import models

class Store(models.Model):
    BRAND_CHOICES = [
        ('CIRCLEK', 'Circle K'),
        ('GS25', 'GS25'),
    ]

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.get_brand_display()} - {self.name}"
