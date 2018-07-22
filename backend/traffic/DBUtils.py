# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from smart.models import Trails
from smart.models import BestEndPlace
from smart.models import BestPickUpPlace
from smart.models import FinalGeoHashPickUpPlace
from smart.models import TrailsGeoHash
import csv
import geohash
import MySQLdb


class trailDBUtil():
    @staticmethod
    def save_trail(data):
        trail = Trails(pickup_longitude=data['pickup_longitude'],
                       pickup_latitude=data['pickup_latitude'],
                       dropoff_longitude=data['dropoff_longitude'],
                       dropoff_latitude=data['dropoff_latitude'],
                       pickup_datetime=data['pickup_datetime'],
                       dropoff_datetime=data['dropoff_datetime'])
        trail.save()
    
    @staticmethod
    def get_trail(time_range):
        print()
        print(time_range)
        print()
        trails = Trails.objects.filter(pickup_datetime__gte=(time_range['start_time']), 
                                        dropoff_datetime__lte=(time_range['end_time']))
        res = []
        for trail in trails:
            t_res = {'start_longitude' : trail.pickup_longitude,
                'start_latitude' : trail.pickup_latitude,
                'end_longitude' : trail.dropoff_longitude,
                'end_latitude' : trail.dropoff_latitude}
            res.append(t_res)
        print (len(trails))
        return res


class  BestEndPlaceDBUtil():
    @staticmethod
    def save_place(data):
        place = BestEndPlace(pickup_longitude=data['pickup_longitude'],
                            pickup_latitude=data['pickup_latitude'],
                            dropoff_longitude=data['dropoff_longitude'],
                            dropoff_latitude=data['dropoff_latitude'])
        place.save()
    
    @staticmethod
    def get_best_place(start_place):
        '''
        根据当前上车的位置，找到附近最近的线的起点,再找到这个线对应的起点的最佳终点
        '''
        print('获取最佳目的地...')
        geohash_value = geohash.encode(start_place['pickup_longitude'], start_place['pickup_latitude'], 10)
        db = MySQLdb.connect("localhost", "root", "wxx19941114", "django", charset='utf8' )
        cursor = db.cursor()
        sql = "select * from smart_trailsgeohash where geohash_value like '%s%%'" % geohash_value[:7]
        cursor.execute(sql) 
        db.commit()
        db.close()
        trails = cursor.fetchall()
        res = []
        for trail in trails:
            places = BestEndPlace.objects.filter(pickup_longitude=trail[1],
                                                    pickup_latitude=trail[2])
            for place in places:
                t_res = {'best_end_longitude' : float(place.dropoff_longitude),
                        'best_end_latitude' : float(place.dropoff_latitude)}
                res.append(t_res)
        print ('获取最佳目的地数目', len(res))
        return res

class BestPickUpPlaceDBUtil():
    @staticmethod
    def save_place(data):
        place = BestEndPlace(driver_longitude=data['driver_longitude'],
                            driver_latitude=data['driver_latitude'],
                            pickup_longitude=data['pickup_longitude'],
                            pickup_latitude=data['pickup_latitude'])
        place.save()
    
    @staticmethod
    def get_best_place(driver_place):
        pickup_places = BestPickUpPlace.objects.filter(driver_longitude=driver_place['driver_longitude'],
                                               driver_latitude=driver_place['driver_latitude'])
        res = []
        for place in pickup_places:
            t_res = {'pickup_longitude' : place.pickup_longitude,
                     'pickup_latitude' : place.pickup_latitude}
            res.append(t_res)
        return res



class GeoHashDBUtil():
    '''
    geohash算法搜索附近的点，然后将点按照包含的个数从大到小返回
    SELECT * FROM place WHERE geohash LIKE 'wx4g0%';
    '''
    @staticmethod
    def get_near_palce(data):
        driver_geohash_value = geohash.encode(data['driver_lng'], data['driver_lat'], 10)
        points = FinalGeoHashPickUpPlace.objects.filter(geohash_value__startswith=driver_geohash_value)
        res = []
        for point in points:
            t = {}
            t['pickup_longitude'] = point.pickup_longitude
            t['pickup_latitude'] = point.pickup_latitude
            res.append((t, point.point_num))
        res = sorted(res, key=lambda x: x[1], reverse=True)
        print(len(res))
        return res