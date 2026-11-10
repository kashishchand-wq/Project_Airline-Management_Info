class Flight:
    def __init__(self,ID,DepartureAirport,ArrivalAirport,DepartureTime,ArrivalTime,Passangers):
        self.ID = ID
        self.DepartureAirport = DepartureAirport
        self.ArrivalAirport = ArrivalAirport
        self.DepartureTime = DepartureTime
        self.ArrivalTime = ArrivalTime
        self.Passangers = Passangers

def PrintFlight (flight):
    print("ID: ", flight.ID)
    print("DepartureAirport: ", flight.DepartureAirport)
    print("ArrivalAirport: ", flight.ArrivalAirport)
    print("DepartureTime: ", flight.DepartureTime)
    print("ArrivalTime: ", flight.ArrivalTime)
    print("Passangers: ", flight.Passangers)

def TimeToMinutes (time):
# Converts and returns time hh:mm to minuts counted from 00:00
    try:
        h, m = time.strip().split(":")
        hours, minutes = int(h), int(m)
        if 0 <= hours < 24 and 0 <= minutes < 60:
            return hours * 60 + minutes
        return -1
    except ValueError:
        return -1

def FlightDuration (flight):
# Returns the duration in minutes
    departure = TimeToMinutes(flight.DepartureTime)
    arrival = TimeToMinutes(flight.ArrivalTime)
    if departure == -1 or arrival == -1:
        return -1
    duration = arrival - departure
    if duration < 0:
        duration += 24 * 60
    return duration

def LoadFlights (filename):
    flights = []
    try:
        with open(filename, "r") as file:
            for line in file:
                data = line.split()

                # Each flight must have 6 fields
                if len(data) != 6:
                    continue
                flight_id = data[0]
                departure_airport = data[1]
                arrival_airport = data[2]
                departure_time = data[3]
                arrival_time = data[4]
                try:
                    passengers = int(data[5])
                except ValueError:
                    continue

                # Comprobar horas usando el retorno de TimeToMinutes (-1 indica error)
                dep_min = TimeToMinutes(departure_time)
                arr_min = TimeToMinutes(arrival_time)
                if dep_min == -1 or arr_min == -1 or passengers < 0:
                    continue

                flight = Flight(flight_id,departure_airport,arrival_airport,departure_time,arrival_time,passengers)
                flights.append(flight)
    except FileNotFoundError:
        return []
    return flights

def SaveFlights (flights, filename):
    with open(filename, "w") as file:
        for flight in flights:
            file.write(f"{flight.ID} {flight.DepartureAirport} {flight.ArrivalAirport} {flight.DepartureTime} {flight.ArrivalTime} {flight.Passangers}\n")

def PrintFlights (flights):
    for flight in flights:
        PrintFlight(flight)

def AddFlights (flights, flight):
    flights.append(flight)

def RemoveFlights (flights, flight_id):
    for flight in flights:
        if flight.ID == flight_id:
            flights.remove(flight)
            return 0
    return -1

# test section
if __name__ == "__main__":
    flight = Flight("A11", "LEBL", "EGLL", "12:30", "14:30", 135)
    PrintFlight(flight)
    print(FlightDuration(flight))

    # Create test flights
    flight1 = Flight("FL001", "LEBL", "LEPA", "10:30", "11:15", 120)
    flight2 = Flight("FL002", "LEPA", "LEMD", "12:00", "13:10", 150)
    flights = [flight1, flight2]

    # Test PrintFlights
    print("Initial flights:")
    PrintFlights(flights)

    # Test SaveFlights
    SaveFlights(flights, "flights.txt")
    print("\nFlights saved to file.")

    # Test LoadFlights
    loaded_flights = LoadFlights("flights.txt")
    print("\nLoaded flights:")
    PrintFlights(loaded_flights)

    # Test AddFlight
    flight3 = Flight("FL003", "LEMD", "LEBL", "15:00", "16:10", 180)
    AddFlights(loaded_flights, flight3)

    print("\nAfter adding a flight:")
    PrintFlights(loaded_flights)

    # Test RemoveFlight
    result = RemoveFlights(loaded_flights, "FL002")

    print("\nAfter removing FL002:")
    PrintFlights(loaded_flights)
    print("Remove result:", result)

    # Test removing a flight that does not exist
    result = RemoveFlights(loaded_flights, "FL999")
    print("Remove non-existing flight result:", result)

    # Test FlightDuration
    print("\nDuration of FL001:", FlightDuration(flight1), "minutes")
