from django.db import models

# Create your models here.
class Resource(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    description = models.TextField(max_length=1000)
    website = models.CharField(max_length=200)

    def __str__(self):
        return self.name