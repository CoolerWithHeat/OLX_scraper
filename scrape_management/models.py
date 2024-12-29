from django.db import models

class sent_apartments(models.Model):
    apartment_url = models.URLField()

    @classmethod
    def check_if_sent(cls, url_to_check):
        return cls.objects.filter(apartment_url=url_to_check).exists()
    
    def __str__(self):
        return self.apartment_url