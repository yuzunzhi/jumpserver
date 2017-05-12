from django.db import models
from time import strftime

# Create your models here.
class Domain_List(models.Model):
    def __str__(self):
        return self.zone

    zone = models.CharField(max_length=255, null=False, primary_key=True)

class Records(models.Model):
    def __str__(self):
        return self.host

    zone = models.CharField(max_length=255, null=True, default="NULL")
    host = models.CharField(max_length=255, null=True, default="NULL")
    type = models.CharField(max_length=10, null=True, default="NULL")
    data = models.CharField(max_length=255, null=False, default="NULL")
    ttl = models.IntegerField(null=True)
    mx_priority = models.IntegerField(null=True)
    refresh = models.IntegerField(null=True)
    retry = models.IntegerField(null=True)
    expire = models.IntegerField(null=True)
    minimum = models.IntegerField(null=True)
    serial = models.BigIntegerField(null=True)
    resp_person = models.CharField(max_length=64, null=True)
    primary_ns = models.CharField(max_length=64, null=True)