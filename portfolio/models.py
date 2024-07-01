from django.db import models

# Create your models here.

class reval_file(models.Model):
    item = models.CharField(max_length=100,null=True)
    quarter=models.CharField(max_length=100,null=True)
    pn = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=100,null=True)
    qty = models.CharField(max_length=100,null=True)
    usd = models.CharField(max_length=100,null=True)
    scrap = models.FloatField(null=True)
    unit_freight =  models.FloatField(null=True)
    unit_price =  models.FloatField(null=True)
    ext_price = models.FloatField(null=True)
    remark = models.CharField(max_length=100,null=True)
    unit_price = models.CharField(max_length=100,null=True)