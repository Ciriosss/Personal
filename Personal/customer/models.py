from django.db import models
from django.contrib.auth.models import User


class ActivityType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

class Sector(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.sector

class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    activity = models.CharField(max_length=255,blank=True,null=True)