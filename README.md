## 环境搭建：
使用python3
pip3 install virtualenv
source venv3/bin/activate

运行服务：
python manage.py runserver


## 接口格式：
1.展示功能： /trails
  a.时间段路线展示
  输入
  {
    "start_time" : "2018-08-10 09:00:00",
    "end_time" : "2018-08-10 09:30:00"
  }
 输出
  [
    {
      "id": 1,
      "start": {
        "lat": 37.772,
        "lng": -122.214
      },
      "end": {
        "lat": 21.291, 
        "lng": -157.821
      }
    }
  ]

 
  b.用户位置热力图


2.分析／推荐
  a.路线推荐 /bestendplace
  输入
    {
    "pickup_longitude" : "-73.96633148",
    "pickup_latitude" : "40.76160049"
    }
  输出
    [
      {
          "best_end_longitude": "-73.9699173",
          "best_end_latitude": "40.75218964"
      },{
        
      }
    ]

  b.接客地点推荐 /geohashsearch
  输入
    {
    "driver_lng" : -73.9934177398682,
    "driver_lat" : 40.7294926643372
  }
  输出
    [
      [
          {
              "pickup_longitude": "-73.9934177398682",
              "pickup_latitude": "40.7294926643372"
          },
  
      ]
  ]


## 数据结构：
1.路线表
2.终点推荐表
3.司机接客地点表


python manage.py makemigrations
python manage.py migrate 


## 创新点：
  目的地推荐：大数据全局统计
  接客地点推荐：使用DBSCAN聚类算法找出中心簇数：以及每个簇的点数，然后在这个簇表使用geohash中搜索离当前司机最近的簇,存下来
