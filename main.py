import requests
import datetime

api_key = "wHYh-AIObxYyTV0PCY3R0huV0nOXG1pCmAAWm8GZxXk"
base_url = "https://api.transport.nsw.gov.au/v1"
departure_url = "/tp/departure_mon"
full_url = base_url + departure_url

# utc is 11 hrs behind aest
timezone_offset = 39600
    
# current date and time
current_datetime = datetime.datetime.now()
current_date = current_datetime.strftime("%Y%m%d")
current_time = int(current_datetime.strftime("%H%M"))


def check_departures():
    api_parameters = {
        "outputFormat": "rapidJSON",
        "coordOutputFormat": "EPSG:4326",
        "mode": "direct",
        "type_dm": "stop",
        "name_dm": "2154392",  # Hills Showground stop ID
        "depArrMacro": "dep",
        "itdDate": current_date,
        "itdTime": current_time,
        "TfNSWDM": "true"
    }

    headers = {
        "Authorization": "apikey " + api_key
    }

    response = requests.get(full_url, headers=headers, params=api_parameters)
    data = response.json()
    stop_events = data["stopEvents"]

    for stop_event in stop_events[:20]:
        platform_number = stop_event["location"]["properties"]["platformName"]
        
        if platform_number == "Platform 1" or platform_number == "Platform 2":
            final_destination = stop_event["transportation"]["destination"]["name"]
            departure_time = stop_event["departureTimePlanned"]
            
            datetime_format_departure_time = datetime.datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%SZ")    

            seconds_till_departure = (datetime_format_departure_time.timestamp() - current_datetime.timestamp() + timezone_offset)
            minutes_till_departure = round(seconds_till_departure / 60)

            print(f"The next train to arrive on {platform_number} ", end="") 
            print(f"goes to {final_destination}, ", end="") 
            print(f"departing in {minutes_till_departure} minutes")