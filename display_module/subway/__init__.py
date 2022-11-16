import os;
from urllib.request import Request, urlopen;
from urllib.error import HTTPError, URLError

import json
MaxCount = 3
def load_data():
    data = None;
    mta_data_url = os.getenv("MTA_DATA_URL")
    if ( mta_data_url ): 
        try: 
            with urlopen( Request(mta_data_url), timeout = 10 ) as response:
                last_data = json.loads( response.read().decode("utf-8"))
                subway_data = last_data['subway']
                last_update = last_data['updated_date']
                data = []
                for stopItem in subway_data.items():
                    stop = stopItem[1]
                    data.append({
                        'text': stop['bound_name'],
                        'type': 'title'
                        })
                    i = 0;
                    for timeItem in stop['wait_time']:
                        if( i < MaxCount ):
                            data.append({
                                'text': "now" if timeItem <= 0 else f"{timeItem}min",
                                'type': 'listItem' 
                                })
                        else:
                            break;
                        i += 1;
        except HTTPError as error:
            print(error.status, error.reason)
        except URLError as error:
            print(error.reason)
        except TimeoutError:
            print("Request timed out")
    return data;

if __name__ == '__main__':
    data = load_data();
    print( data )