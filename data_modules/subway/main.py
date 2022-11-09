import json;
import os;
import math;
from urllib.request import Request, urlopen;
from google.transit import gtfs_realtime_pb2
from datetime import datetime

def get_config():
    f = open("subway_data.json")
    data = json.load(f)
    return data;

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
    print(f"now = {now_in_mill_sec}" )
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
        print( times )
    except HTTPError as error:
        print(error.status, error.reason)
    except URLError as error:
        print(error.reason)
    except TimeoutError:
        print("Request timed out")




if __name__ == '__main__':
    get_data();