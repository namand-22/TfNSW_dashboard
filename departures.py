import requests
import datetime

# accessing the API
api_key = "wHYh-AIObxYyTV0PCY3R0huV0nOXG1pCmAAWm8GZxXk"
base_url = "https://api.transport.nsw.gov.au/v1"
departure_url = "/tp/departure_mon"
full_url = base_url + departure_url

    

# utc is 11 hrs behind aest
timezone_offset = 39600

def check_departures(station_id):
    # empty retrun variable to be added to 
    upcoming_departures = []
    
    # current date and time
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%Y%m%d")
    current_time = int(current_datetime.strftime("%H%M"))
    

    api_parameters = {
        "outputFormat": "rapidJSON",
        "coordOutputFormat": "EPSG:4326",
        "mode": "direct",
        "type_dm": "stop",
        "name_dm": str(station_id),
        "depArrMacro": "dep",
        "itdDate": current_date,
        "itdTime": current_time,
        "TfNSWDM": "true"
    }

    headers = {
        "Authorization": "apikey " + api_key
    }

    # requesting data
    response = requests.get(full_url, headers=headers, params=api_parameters)
    data = response.json()
    stop_events = data["stopEvents"]

    # checks for upcoming departures from Hills Showground
    for stop_event in stop_events:
        platform_number = stop_event["location"]["properties"]["platformName"]
        
        # if upcoming departures are from the metro, not bus
        if platform_number == "Platform 1" or platform_number == "Platform 2" or platform_number == "Platform 3" or platform_number == "Platform 4":
            final_destination = stop_event["transportation"]["destination"]["name"]
            departure_time = stop_event["departureTimeEstimated"]
            train_line = stop_event["transportation"]["disassembledName"]
            
            datetime_format_departure_time = datetime.datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%SZ")    

            # calculate the difference in current time and time till departure
            seconds_till_departure = (datetime_format_departure_time.timestamp() - current_datetime.timestamp() + timezone_offset)
            minutes_till_departure = round(seconds_till_departure / 60)
            
            if minutes_till_departure >= 0:
                departure_info = {"platform": platform_number, "destination": final_destination, "departing_in": minutes_till_departure, "train_line": train_line}
                upcoming_departures.append(departure_info)
    
    return upcoming_departures

if __name__ == "__main__":
    check_departures(station_id=206710) # station_id is for Hills Showground