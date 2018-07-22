from django.db import models

# Create your models here.

class Trails(models.Model):
    pickup_longitude = models.CharField(max_length=20)
    pickup_latitude = models.CharField(max_length=20)
    dropoff_longitude = models.CharField(max_length=20)
    dropoff_latitude = models.CharField(max_length=20)
    pickup_datetime = models.DateTimeField()
    dropoff_datetime = models.DateTimeField()


class BestEndPlace(models.Model):
    pickup_longitude = models.CharField(max_length=20)
    pickup_latitude = models.CharField(max_length=20)
    dropoff_longitude = models.CharField(max_length=20)
    dropoff_latitude = models.CharField(max_length=20) 


class BestPickUpPlace(models.Model):
    driver_longitude = models.CharField(max_length=20)
    driver_latitude = models.CharField(max_length=20)
    pickup_longitude = models.CharField(max_length=20)
    pickup_latitude = models.CharField(max_length=20)

class GeoHashPickUpPlace(models.Model):
    pickup_longitude = models.CharField(max_length=20)
    pickup_latitude = models.CharField(max_length=20)
    point_num = models.IntegerField()

class NewGeoHashPickUpPlace(models.Model):
    geohash_value = models.CharField(max_length=10)
    point_num = models.IntegerField()

class FinalGeoHashPickUpPlace(models.Model):
    pickup_longitude = models.CharField(max_length=20)
    pickup_latitude = models.CharField(max_length=20)
    geohash_value = models.CharField(max_length=10)
    point_num = models.IntegerField()

class TrailsGeoHash(models.Model):
    pickup_longitude = models.CharField(max_length=20)
    pickup_latitude = models.CharField(max_length=20)
    geohash_value = models.CharField(max_length=10)
    