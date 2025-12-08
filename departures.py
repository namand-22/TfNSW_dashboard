import requests
import datetime

api_key = "wHYh-AIObxYyTV0PCY3R0huV0nOXG1pCmAAWm8GZxXk"
base_url = "https://api.transport.nsw.gov.au/v1"
departure_url = "/tp/departure_mon"
full_url = base_url + departure_url

timezone_offset = 39600  # UTC to AEST

def check_departures(station_id):
    upcoming_departures = []

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

    try:
        response = requests.get(full_url, headers=headers, params=api_parameters)
        data = response.json()
    except Exception as e:
        return {"error": f"Failed to fetch data: {str(e)}"}

    stop_events = data.get("stopEvents")
    if not stop_events:
        return {"error": f"Station ID {station_id} is invalid, please enter a valid Station ID."}

    for stop_event in stop_events:
        platform_number = stop_event["location"]["properties"].get("platformName", "")
        if platform_number in ["Platform 1", "Platform 2", "Platform 3", "Platform 4"]:
            final_destination = stop_event["transportation"]["destination"]["name"]
            departure_time = stop_event["departureTimeEstimated"]
            train_line = stop_event["transportation"]["disassembledName"]

            try:
                datetime_format_departure_time = datetime.datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%SZ")
                seconds_till_departure = (datetime_format_departure_time.timestamp() - current_datetime.timestamp() + timezone_offset)
                minutes_till_departure = round(seconds_till_departure / 60)

                if minutes_till_departure >= 0:
                    departure_info = {
                        "platform": platform_number,
                        "destination": final_destination,
                        "departing_in": minutes_till_departure,
                        "train_line": train_line
                    }
                    upcoming_departures.append(departure_info)
            except Exception:
                continue

    return upcoming_departures

if __name__ == "__main__":
    print(check_departures(station_id=206710))