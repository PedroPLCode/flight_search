import sys, requests, json

json_filename = 'test_api_response.json'
YOUR_API_KEY = 'XXX'

def main():
    """Main probram body."""
    
    path = get_user_question()

    if path == "ns_ow_from":
        dept_airport, from_date, to_date = get_user_input_from()
        if confirm_data_from(dept_airport, from_date, to_date):
            response = get_api_response_from(dept_airport, from_date, to_date) 
    elif path == "ns_ow_to":
        arr_airport, from_date, to_date = get_user_input_to()
        if confirm_data_to(arr_airport, from_date, to_date):
            response = get_api_response_to(arr_airport, from_date, to_date)

    content = {}
    content = response.json()
    
    show_flights(content)
    

def get_user_question():
    """User decide what question to ask."""
    print("\n-= FLIGHTS SEARCH =-\n\tv2 pedro\n"
          "\nUsing API requests - internet connection required."
          "\nCurrently availeable options to choose:\n")
          
    while True:    
        print("1 - Searching for non stop, one way flights FROM specified airport.\n"
              "2 - Searching for non stop, one way flights TO specified airport.\n"
              "3 - Searching for non stop, 2 ways flights FROM specified airport. NOT READY\n"
              "4 - Searching for non stop, 2 ways flights TO specified airport. NOT READY\n"
              "5 - Searching for connecting, one way flights BETWEEN specified airports. NOT READY\n")
        choose = str(input("What is your choice? Input number or q to quit: "))
        choose = choose.strip().lower()

        if choose == "1":
            path = "ns_ow_from"
            return path
        elif choose == "2":
            path = "ns_ow_to"
            return path
        elif choose == "q" or choose == "quit":
            print("\nOk. Quit.\n")
            sys.exit()
        else:
            print("\nError. Wrong input. Try again.\n")
            continue


def confirm_data_from(dept_airport, from_date, to_date):
    """Shows uper input and waiting to confirm."""
    print("\nReady to search for flights:\n"
          f"Departing from {get_airport_info(dept_airport)}\n"
          f"{from_date} - {to_date}")
    while True:
        print("\nAre you sure?\n" 
        "y - start searching\n"
        "q - quit")
        sure = input("User input: ")
        if sure == 'y':
            return True
        elif sure == 'q':
            print("Ok. Quit.")
            sys.exit()
        else:
            print("Error. Wrong input.")
            continue
        

def confirm_data_to(arr_airport, from_date, to_date):
    """Shows uper input and waiting to confirm."""
    print("\nReady to search for flights:\n"
          f"Arriving to {get_airport_info(arr_airport)}\n"
          f"{from_date} - {to_date}\n")
    while True:
        print("Are you sure?\n" 
        "y - start searching\n"
        "q - quit")
        sure = input("Your answer: ")
        sure = sure.lower().strip()
        if sure == 'y' or sure == 'yes':
            return True
        elif sure == 'q' or sure == 'quit':
            print("Ok. Quit.")
            sys.exit()
        else:
            print("Error. Wrong input. Try again.")
            continue


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
                  f"\n\nDeparture airport: {get_airport_info(content['data'][n]['departure']['airport']['iata'])} "
                  f"{content['data'][n]['departure']['airport']['iata']} "
                  f"{dept_terminal}"
                  f"\nDeparture date: {content['data'][n]['departure']['date']}"
                  f"\nDeparture time: {content['data'][n]['departure']['passengerLocalTime']} Local Time"
                  f"\n\nArrival airport: {get_airport_info(content['data'][n]['arrival']['airport']['iata'])} "
                  f"{content['data'][n]['arrival']['airport']['iata']} "
                  f"{arr_terminal}"
                  f"\nArrival date: {content['data'][n]['arrival']['date']}"
                  f"\nArrival time: {content['data'][n]['arrival']['passengerLocalTime']} Local Time"
                  f"\n\nFlight number: {content['data'][n]['carrierCode']['iata']} "
                  f"{content['data'][n]['flightNumber']}"
                  f"\nAirlines: {get_airline_info(content['data'][n]['carrierCode']['iata'])}"
                  f"\nAircraft type: {get_aircraft_type(content['data'][n]['aircraftType']['iata'])}"
                  )
            flight_nr +=1
        

def get_user_input_from():
    """Gets user input for flight from specified airport."""
    departure_airport = str(input("\nEnter Departure Airport (IATA code): "))
    departure_airport = departure_airport.upper().strip()
    dept_airport = search_airports(departure_airport)
    from_date = str(input("Enter Departure From Date (format YYYY-MM-DD): "))
    from_date = from_date.replace('/', '-')
    from_date = from_date.replace('_', '-')
    from_date = from_date.replace(':', '-')
    from_date = from_date.replace('.', '-')
    from_date = from_date.replace(',', '-')
    to_date = str(input("Enter Departure To Date (format YYYY-MM-DD): "))
    to_date = to_date.replace('/', '-')
    to_date = to_date.replace('_', '-')
    to_date = to_date.replace(':', '-')
    to_date = to_date.replace('.', '-')
    to_date = to_date.replace(',', '-')
    return dept_airport, from_date, to_date


def get_user_input_to():
    """Gets user input for flight to specified airport."""
    arrival_airport = str(input("\nEnter Arrival Airport (IATA code): "))
    arrival_airport = arrival_airport.upper().strip()
    arr_airport = search_airports(arrival_airport)
    from_date = str(input("Enter Arrival From Date (format YYYY-MM-DD): "))
    from_date = from_date.replace('/', '-')
    from_date = from_date.replace('_', '-')
    from_date = from_date.replace(':', '-')
    from_date = from_date.replace('.', '-')
    from_date = from_date.replace(',', '-')
    to_date = str(input("Enter Arrival To Date (format YYYY-MM-DD): "))
    to_date = to_date.replace('/', '-')
    to_date = to_date.replace('_', '-')
    to_date = to_date.replace(':', '-')
    to_date = to_date.replace('.', '-')
    to_date = to_date.replace(',', '-')
    return arr_airport, from_date, to_date


def search_airports(airport_query):
    """Search for IATA airport codes byc free text."""
    url = "https://aerodatabox.p.rapidapi.com/airports/search/term"
    querystring = {"q":f"{airport_query})","limit":"1"}
    headers = {
	    "X-RapidAPI-Key": f"{YOUR_API_KEY}",
	    "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
        }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
    except requests.ConnectionError:
        return airport_query
    
    airport_content = response.json()
    try:
        return airport_content['items'][0]['iata']
    except IndexError:
        return airport_query

    
def get_api_response_from(dept_airport, from_date, to_date): #KeyError REACTION
    """API request. Returns response."""

    url = "https://flight-info-api.p.rapidapi.com/schedules"
    querystring = {"version":"v1",
                   "DepartureDate": f"{from_date}/{to_date}",
    	    	   "DepartureAirport": dept_airport
                   }
    headers = {
	    "X-RapidAPI-Key": f"{YOUR_API_KEY}",
	    "X-RapidAPI-Host": "flight-info-api.p.rapidapi.com",
     }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response
    except requests.ConnectionError:
        print("Fatal Error. Couldn't connect to API.")
        sys.exit()
    

def get_api_response_to(arr_airport, from_date, to_date): #KeyError REACTION
    """API request. Returns response."""

    url = "https://flight-info-api.p.rapidapi.com/schedules"
    querystring = {"version":"v1",
                   "DepartureDate": f"{from_date}/{to_date}",
    	    	   "ArrivalAirport": arr_airport
                   }
    headers = {
	    "X-RapidAPI-Key": f"{YOUR_API_KEY}",
	    "X-RapidAPI-Host": "flight-info-api.p.rapidapi.com",
     }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response
    except requests.ConnectionError:
        print("Fatal Error. Couldn't connect to API.")
        sys.exit()


def get_airline_info(airline_iata):
    """Gets airline name from iata code."""
    url = f"https://aviation-reference-data.p.rapidapi.com/airline/{airline_iata}"

    headers = {
	    "X-RapidAPI-Key": f"{YOUR_API_KEY}",
	    "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
    }
    try:
        response = requests.request("GET", url, headers=headers)
        #print(response.text)
        airline_info = {}
        airline_info = response.json()
        try:
            return airline_info['name']
        except KeyError:
            return airline_iata
    except requests.ConnectionError:
        return airline_iata


def get_aircraft_type(aircraft_iata):
    """Gets aircraft manufacturer and model name from icao code."""
    url = f"https://aviation-reference-data.p.rapidapi.com/icaoType/{aircraft_iata}"
    headers = {
	    "X-RapidAPI-Key": f"{YOUR_API_KEY}",
	    "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
    }
    try:
        response = requests.request("GET", url, headers=headers)
        #print(response.text)
        aircraft_info = {}
        aircraft_info = response.json()
        try:
            return (f"{aircraft_info['manufacturer'].title()} {aircraft_info['modelName']}")
        except KeyError:
            return aircraft_iata
    except requests.ConnectionError:
        return aircraft_iata

def get_airport_info(airport_iata):
    """Gets airport name and country from iata code."""
    url = f"https://aviation-reference-data.p.rapidapi.com/airports/{airport_iata}"
    headers = {
	    "X-RapidAPI-Key": f"{YOUR_API_KEY}",
	    "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
    }
    try:
        response = requests.request("GET", url, headers=headers)
        #print(response.text)
        airport_info = {}
        airport_info = response.json()
        try:
            return (f"{airport_info['name'].title()} {airport_info['alpha2countryCode'].upper()}")
        except KeyError:
            return airport_iata
    except requests.ConnectionError:
        return airport_iata

main()