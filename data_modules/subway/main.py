import json;
import os;
import math;
import boto3;
from urllib.request import Request, urlopen;
from google.transit import gtfs_realtime_pb2
from datetime import datetime


BUCKET_NAME=os.getenv("BUCKET_NAME")
KEY_NAME="data.json"
rel_data = os.path.dirname( __file__ )

def get_config():
    f = open(os.path.join( rel_data, "subway_data.json"))
    data = json.load(f)
    return data;

def update_data():
    times = get_data();
    updated_date = datetime.timestamp(datetime.now())
    data = {
        'updated_date': updated_date,
        'subway': times
    }
    save_data( data )



def save_data( data ):
    s3 = boto3.client('s3')
    try:
        s3.put_object(
             ACL='public-read',
             Body=json.dumps(data, ensure_ascii=False),
             Bucket=BUCKET_NAME,
             Key=KEY_NAME
        )
    except Exception as e: 
        print( e )

def get_data():
    config = get_config();
    endpoint = config['endpoint'];
    API_KEY = os.getenv("MTA_API_KEY")
    stations = []
    times = {}
    for station in config["stations"]:
        stations_id = station["stop_id"]
        stations.append( stations_id )
        times[stations_id] = {
            "wait_time": [],
            "bound_name": station["bound_name"] 
        }
    # list ( map( lambda item: item["stop_id"], config["stations"]))
    print( stations )
    headers = {
        'x-api-key': API_KEY
    }

    now_in_mill_sec = datetime.timestamp(datetime.now())
    try: 
        with urlopen( Request(endpoint, headers=headers), timeout = 10 ) as response: 
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.read())
            for entity in feed.entity:
              if entity.HasField('trip_update'):
                for stop in entity.trip_update.stop_time_update:
                    if stop.HasField('arrival'):
                        if stop.stop_id in stations:
                            dt_object = math.floor( ( stop.arrival.time - now_in_mill_sec ) / 60 )
                            times[stop.stop_id]["wait_time"].append(dt_object)
    except HTTPError as error:
        print(error.status, error.reason)
    except URLError as error:
        print(error.reason)
    except TimeoutError:
        print("Request timed out")

    return times;


if __name__ == '__main__':
    times = get_data();
    save_data( times )