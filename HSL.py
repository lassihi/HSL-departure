key = "" #Add your digitransit API key here

import sys
import json
import requests
from datetime import datetime, timedelta

def query(stopId, departures):
    graphql_query ='''{
      stop(id: "'''+stopId+'''") {
        name
        vehicleMode
        stoptimesWithoutPatterns(numberOfDepartures: '''+departures+''') {
          realtimeDeparture
          scheduledDeparture
          realtime
          trip {
            routeShortName
            tripHeadsign
            route {
              alerts {
                alertHeaderText
                alertUrl
              }
            }
          }
        }
      }
    }'''
    return graphql_query 

def seconds_since_midnight_to_time(seconds):
    if seconds < 86400:
        timeStr = f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}"
    else:
        secondsNextDay = seconds - 86400
        timeStr = f"{secondsNextDay // 3600:02d}:{(secondsNextDay % 3600) // 60:02d}"

    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    secondsSinceMidnight = (now - midnight).seconds
    minutesUntil = (seconds - secondsSinceMidnight) // 60
    
    if minutesUntil < -1:
        minutesUntil = (86400 - secondsSinceMidnight + seconds) // 60
    if minutesUntil >= 1440:
        minutesUntil = minutesUntil - 1440

    minutesUntil = str(int(minutesUntil))
    return f"{timeStr:6}~{minutesUntil:3}"

if __name__=="__main__":
    try:
        if len(sys.argv) < 3:
            print("Not enough arguments.")
            exit()
    
        stopId = str(sys.argv[1])
        departures = str(sys.argv[2])
        graphql_query = query(stopId, departures)
        url = "https://api.digitransit.fi/routing/v2/hsl/gtfs/v1?digitransit-subscription-key="+key
        req = requests.post(url, headers = {"Content-Type": "application/json"}, json = {"query": graphql_query})
        response = req.text
        stopData = json.loads(response)['data']['stop']
        stopTimes = stopData['stoptimesWithoutPatterns']
        print(f"{stopData['name']} {stopData['vehicleMode']} stop:\n")

        for ride in stopTimes:
            alerts = 0
            alertText = ""
            for alert in ride['trip']['route']['alerts']:
                alerts += 1
                if alerts == 1:
                    alertText = f"{alerts} alert on route"
                else:
                    alertText = f"{alerts} alerts on route"
                    
            routeShortName = ride['trip']['routeShortName']
            routeHeadsign = ride['trip']['tripHeadsign']            
            realtime = bool(ride['realtime'])
            
            if realtime:
                departureTimeSecs = ride['realtimeDeparture']
                departureTime = seconds_since_midnight_to_time(departureTimeSecs)
                print(f"{routeShortName:7}{routeHeadsign:21} {departureTime} | realtime  | {alertText}")
            else:
                departureTimeSecs = ride['scheduledDeparture']    
                departureTime = seconds_since_midnight_to_time(departureTimeSecs)
                print(f"{routeShortName:7}{routeHeadsign:21} {departureTime} | scheduled | {alertText}")

        print("\nSee alerts: https://www.hsl.fi/en/travelling/services-now")
    except:
        print("Something went wrong. Make sure API key and stop id are valid.")
