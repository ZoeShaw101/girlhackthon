from django.shortcuts import render
from django.http import HttpResponse
import json
import time
from DBUtils import trailDBUtil
from DBUtils import BestEndPlaceDBUtil
from DBUtils import BestPickUpPlaceDBUtil
from DBUtils import GeoHashDBUtil

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.

def trails(request):
    if request.method == 'POST':
        time_range = {}
        # time_range['start_time'] = json.loads(request.body)["start_time"]
        # time_range['end_time'] = json.loads(request.body)["end_time"]
        time_range['start_time'] = request.POST.get("start_time")
        time_range['end_time'] = request.POST.get("end_time")
        time_trails = trailDBUtil.get_trail(time_range)
        res = []
        cur_id = 1
        for trail in time_trails:
            t_res = {}
            t_res['id'] = cur_id 
            t_res['start'] = {}
            t_res['end'] = {}
            t_res['start']['lat'] = float(trail['start_latitude'])
            t_res['start']['lng'] = float(trail['start_longitude'])
            t_res['end']['lat'] = float(trail['end_latitude'])
            t_res['end']['lng'] = float(trail['end_longitude'])
            res.append(t_res)
            cur_id += 1
        return HttpResponse(json.dumps(res), content_type="application/json")

def bestEndPalce(request):
    if request.method == 'POST':
        # start_positon = json.loads(request.body)
        # start_positon['pickup_longitude'] = float(start_positon['pickup_longitude'])
        # start_positon['pickup_latitude'] = float(start_positon['pickup_latitude'])
        start_positon = {}
        start_positon['pickup_longitude'] = float(request.POST.get('pickup_longitude'))
        start_positon['pickup_latitude'] = float(request.POST.get('pickup_latitude'))
        best_end_place = BestEndPlaceDBUtil.get_best_place(start_positon)
        res = []
        for palce in best_end_place:
            t_res = {}
            t_res['lat'] = palce['best_end_latitude']
            t_res['lng'] = palce['best_end_longitude']
            res.append(t_res)
        return HttpResponse(json.dumps(res), content_type="application/json")

def bestPickUpPlace(request):
    if request.method == 'POST':
        driver_positon = json.loads(request.body)
        driver_positon['driver_longitude'] = float(driver_positon['driver_longitude'])
        driver_positon['driver_latitude'] = float(driver_positon['driver_latitude'])
        best_pickup_place = BestPickUpPlaceDBUtil.get_best_place(driver_positon)
        return HttpResponse(json.dumps(best_pickup_place), content_type="application/json")

def GeoHashSearch(request):
    if request.method == 'POST':
        driver_positon = json.loads(request.body)
        best_pickup_place = GeoHashDBUtil.get_near_palce(driver_positon)
        return HttpResponse(json.dumps(best_pickup_place), content_type="application/json")
    