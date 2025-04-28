from django.db import models

# Create your models here.
class St_company(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.code

class St_data(models.Model):
    code = models.ForeignKey(St_company, on_delete=models.DO_NOTHING, null=True, blank=True)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Fixed typo here
    qty = models.IntegerField(default=0)

    def __str__(self):
        return self.date