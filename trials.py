import requests, json

json_filename = 'test_api_response.json'

def search_airports():
    url = "https://aerodatabox.p.rapidapi.com/airports/search/term"
    querystring = {"q":"schiphol","limit":"10"}
    headers = {
	    "X-RapidAPI-Key": "YOUR-API-KEY",
	    "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)

    response = search_airports()
    airport_content = response.json()

    print(airport_content['items'][0]['iata'])
    print(airport_content['items'][0]['name'])
    print(airport_content['items'][0]['location'])
    print(airport_content['items'][0]['countryCode'])


def search_flights(dept_date, arr_date, dept_airport, arr_airport):
    url = "https://flight-info-api.p.rapidapi.com/schedules"
    querystring = {"version":"v1","DepartureDate":f"{dept_date}","ArrivalDate":f"{arr_date}","DepartureAirport":f"{dept_airport}","ArrivalAirport":f"{arr_airport}"}
    headers = {
	    "X-RapidAPI-Key": "YOUR-API-KEY",
	    "X-RapidAPI-Host": "flight-info-api.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    resp_content = response.json()

    print(resp_content)


def show_flights(content): #KeyError REACTION
    """Shows formatted flights informations."""
    flight_nr = 1
    for n in range(0, len(content['data'])):
        if content['data'][n]['departure']['passengerLocalTime'] == content['data'][n-1]['departure']['passengerLocalTime'] or content['data'][n]['arrival']['passengerLocalTime'] == content['data'][n-1]['arrival']['passengerLocalTime']:
            pass
        else:
            if content['data'][n]['departure']['terminal'] != "":
                dept_terminal = f"Terminal {content['data'][n]['departure']['terminal'].title()}"
            else:
                dept_terminal = ""
            if content['data'][n]['arrival']['terminal'] != "":
                arr_terminal = f"Terminal {content['data'][n]['arrival']['terminal'].title()}"
            else:
                arr_terminal = ""

            print(f"\n\n\nFlight {flight_nr}: {content['data'][n]['departure']['passengerLocalTime']} "
                  f"{content['data'][n]['departure']['airport']['iata']} - "
                  f"{content['data'][n]['arrival']['airport']['iata']} "
                  f"{content['data'][n]['arrival']['passengerLocalTime']}"
                  f"{content['data'][n]['departure']['airport']['iata']} "
                  f"{dept_terminal}"
                  f"\nDeparture date: {content['data'][n]['departure']['date']}"
                  f"\nDeparture time: {content['data'][n]['departure']['passengerLocalTime']} Local Time"
                  f"{content['data'][n]['arrival']['airport']['iata']} "
                  f"{arr_terminal}"
                  f"\nArrival date: {content['data'][n]['arrival']['date']}"
                  f"\nArrival time: {content['data'][n]['arrival']['passengerLocalTime']} Local Time"
                  f"\n\nFlight number: {content['data'][n]['carrierCode']['iata']} "
                  f"{content['data'][n]['flightNumber']}"
                  )
            flight_nr +=1

with open(json_filename, 'r') as filename: #
    content = json.load(filename)

show_flights(content)