from datetime import datetime

with open('sl_api_key.txt') as f:
    api_key = f.read()

def strs_to_datetime(date_str, time_str):
    return datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M:%S')

strs_to_datetime('2021-01-15', '13:30:00')

import requests

def get_travel_time_between(origin_lat, origin_long, dest_lat, dest_long,
                            verbose = False):

    params = {
        'key': api_key,
        
        'originCoordLat': origin_lat,
        'originCoordLong': origin_long,
        'destCoordLat': dest_lat,
        'destCoordLong': dest_long,
        
        'maxChange':11,
        'date': '2023-01-18',
        'time': '09:00',
        'searchForArrival': 1, 
        'numF': 0,             
        'numB': 0              
    }

    response = requests.get('http://api.sl.se/api2/TravelplannerV3_1/trip.json',
                            params=params)

   

    
    if not response.status_code == 200:
        if verbose:
            print('ERROR ({}) in retrieving time between ({}, {}) and ({}, '
                  '{})!'.format(response.status_code,
                                origin_lat,
                                origin_long,
                                dest_lat,
                                dest_long)
                  )
        return -1

    json_data = response.json()

    first_segment = json_data['Trip'][0]['LegList']['Leg'][0]
    last_segment  = json_data['Trip'][0]['LegList']['Leg'][-1]

    start_time = strs_to_datetime(first_segment['Origin']['date'],
                                  first_segment['Origin']['time'])

    end_time = strs_to_datetime(last_segment['Destination']['date'],
                                last_segment['Destination']['time'])

    return (end_time - start_time).total_seconds() / 60


kth_lat  = 59.21515
kth_long = 18.32201

central_lat  = 59.325665364 
central_long = 18.056499774

print(get_travel_time_between(kth_lat, kth_long, central_lat, central_long))