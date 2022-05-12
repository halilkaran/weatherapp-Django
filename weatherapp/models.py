from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name
