from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Trip(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True , blank = True)
    trip_user = models.CharField( max_length=50)
    trip_from = models.CharField( max_length=50)
    trip_to = models.CharField( max_length=50)
    trip_distance = models.IntegerField()
    trip_charge = models.IntegerField()
    trip_intermediate_stops = models.TextField()
    trip_description = models.TextField()