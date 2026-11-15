class Flight:
    def __init__(self, ID, DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, Passangers, assigned_aircraft=None):
        self.ID = ID
        self.DepartureAirport = DepartureAirport
        self.ArrivalAirport = ArrivalAirport
        self.DepartureTime = DepartureTime.strip()
        self.ArrivalTime = ArrivalTime.strip()
        self.Passangers = int(Passangers)
        self.assigned_aircraft = assigned_aircraft  # None si no está asignado, o callsign del avión

def PrintFlight(flight):
    print("ID:", flight.ID)
    print("DepartureAirport:", flight.DepartureAirport)
    print("ArrivalAirport:", flight.ArrivalAirport)
    print("DepartureTime:", flight.DepartureTime)
    print("ArrivalTime:", flight.ArrivalTime)
    print("Passangers:", flight.Passangers)
    estado = flight.assigned_aircraft if flight.assigned_aircraft else "Unassigned"
    print("Assigned Aircraft:", estado)

def TimeToMinutes(time):
    try:
        h, m = time.strip().split(":")
        hours, minutes = int(h), int(m)
        if 0 <= hours < 24 and 0 <= minutes < 60:
            return hours * 60 + minutes
        return -1
    except ValueError:
        return -1

def FlightDuration(flight):
    departure = TimeToMinutes(flight.DepartureTime)
    arrival = TimeToMinutes(flight.ArrivalTime)
    if departure == -1 or arrival == -1:
        return -1
    duration = arrival - departure
    if duration < 0:
        duration += 24 * 60
    return duration

def LoadFlights(filename):
    flights = []
    try:
        with open(filename, "r") as file:
            for line in file:
                data = line.strip().split()
                if len(data) != 6 or data[0] == "ID":
                    continue

                # Detección automática del orden de columnas (Operations.txt vs flights.txt)
                if ":" in data[1]:
                    flight_id, departure_time, arrival_time, departure_airport, arrival_airport, pax_str = data
                else:
                    flight_id, departure_airport, arrival_airport, departure_time, arrival_time, pax_str = data

                try:
                    passengers = int(pax_str)
                except ValueError:
                    continue

                dep_min = TimeToMinutes(departure_time)
                arr_min = TimeToMinutes(arrival_time)
                if dep_min == -1 or arr_min == -1 or passengers < 0:
                    continue

                flight = Flight(flight_id, departure_airport, arrival_airport, departure_time, arrival_time, passengers)
                flights.append(flight)
    except FileNotFoundError:
        return []
    return flights

def SaveFlights(flights, filename):
    with open(filename, "w") as file:
        file.write("ID TIMD TIMA DEPT ARRV PASS\n")
        for flight in flights:
            file.write(f"{flight.ID} {flight.DepartureTime} {flight.ArrivalTime} {flight.DepartureAirport} {flight.ArrivalAirport} {flight.Passangers}\n")

def PrintFlights(flights):
    for flight in flights:
        PrintFlight(flight)
        print("-" * 20)

def AddFlights(flights, flight):
    flights.append(flight)

def RemoveFlights(flights, flight_id):
    for flight in flights:
        if flight.ID == flight_id:
            flights.remove(flight)
            return 0
    return -1

def ResetAssignments(flights):
    """Reinicia la asignación de todos los vuelos a None"""
    for flight in flights:
        flight.assigned_aircraft = None

def GetAssignedFlights(flights):
    return [f for f in flights if f.assigned_aircraft is not None]

def GetUnassignedFlights(flights):
    return [f for f in flights if f.assigned_aircraft is None]

# test section
if __name__ == "__main__":
    loaded_flights = LoadFlights("Operations.txt")
    print(f"Loaded {len(loaded_flights)} flights from Operations.txt")

    if loaded_flights:
        # Simular asignación y reinicio
        loaded_flights[0].assigned_aircraft = "OY-PSA"
        print("\nFirst flight after manual assignment:")
        PrintFlight(loaded_flights[0])

        print("\nAssigned count:", len(GetAssignedFlights(loaded_flights)))
        print("Unassigned count:", len(GetUnassignedFlights(loaded_flights)))

        ResetAssignments(loaded_flights)
        print("\nAfter ResetAssignments:")
        PrintFlight(loaded_flights[0])