# -*- coding: UTF-8 -*-
import csv
import MySQLdb
import pandas as pd
import pickle
from datetime import datetime
import geohash


def insert_into_data(csv_fpath, dbname, cursor):
    '''
    插入数据库脚本
    '''
    with open(csv_fpath, 'r') as f:
        lines = csv.reader(f)
        if dbname == 'BestEndPlaceDB':
            for line in lines:
                try :
                    start_lng = float(line[0][1:-2].split(',')[0].strip())
                    start_lat = float(line[0][1:-2].split(',')[1].strip())
                    end_lng = float(line[1][2:-2].split(',')[0].strip())
                    end_lat = float(line[1][2:-2].split(',')[1].strip())
                    cursor.execute("insert into smart_bestendplace " + 
                    "(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude) values (%s, %s, %s, %s)"
                     % (start_lng, start_lat, end_lng, end_lat))
                except Exception as e:
                    print (start_lng, start_lat, end_lng, end_lat)
                    print ('error: ', e)
        elif dbname == 'trailDB':
            try : 
                df = pd.read_csv(csv_fpath)
                for p_la, p_lo in zip(df['pickup_latitude'], df['pickup_longitude']):
                    params = (p_lo, p_la, geohash.encode(p_lo, p_la, 10))
                    print (params)
                    cursor.execute("insert into smart_trailsgeohash (pickup_longitude, pickup_latitude, geohash_value) values (%s, %s, %s)" , params)
            except Exception as e:
                print ('error: ', e)
        elif dbname == 'BestPickUpPlaceDB':
            try :
                clusters = pickle.load(f)
                for c in clusters:
                    geohash_value = geohash.encode(c['lng'], c['lat'], 10)
                    params = (geohash_value, c['lng'], c['lat'], c['points_num'])
                    print(params)
                    cursor.execute("insert into smart_finalgeohashpickupplace (geohash_value, pickup_longitude, pickup_latitude, point_num) values( %s, %s, %s, %s)", params)
            except Exception as e:
                print ('error: ', e)
    


if __name__=='__main__':
    db = MySQLdb.connect("localhost", "root", "wxx19941114", "django", charset='utf8' )
    cursor = db.cursor()
    # insert_into_data("/Users/shaw/Desktop/girlhackthon/data/best_end_palce.csv", "BestEndPlaceDB", cursor)
    insert_into_data("/Users/shaw/Desktop/girlhackthon/data/trails.csv", "trailDB", cursor)
    # insert_into_data("/Users/shaw/Desktop/girlhackthon/data/cluster.pkl", "BestPickUpPlaceDB", cursor)
    db.commit()
    db.close()