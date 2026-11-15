class Flight:
    def __init__(self, ID, DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, Passangers, assigned_aircraft=None):
        self.ID = ID
        self.DepartureAirport = DepartureAirport
        self.ArrivalAirport = ArrivalAirport
        self.DepartureTime = DepartureTime
        self.ArrivalTime = ArrivalTime
        self.Passangers = Passangers
        self.assigned_aircraft = assigned_aircraft


def PrintFlight(flight):
    print("ID:", flight.ID)
    print("DepartureAirport:", flight.DepartureAirport)
    print("ArrivalAirport:", flight.ArrivalAirport)
    print("DepartureTime:", flight.DepartureTime)
    print("ArrivalTime:", flight.ArrivalTime)
    print("Passangers:", flight.Passangers)
    print("Assigned Aircraft:", flight.assigned_aircraft)


def PrintFlights(flights):
    for flight in flights:
        PrintFlight(flight)


def AddFlights(flights, flight):
    flights.append(flight)


def RemoveFlights(flights, flight_id):
    for flight in flights:
        if flight.ID == flight_id:
            flights.remove(flight)
            return 0
    return -1


def TimeToMinutes(time):
    parts = time.strip().split(":")
    if len(parts) != 2:
        return -1
    if not parts[0].isdigit() or not parts[1].isdigit():
        return -1
    hours = int(parts[0])
    minutes = int(parts[1])
    if 0 <= hours < 24 and 0 <= minutes < 60:
        return hours * 60 + minutes
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
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        for line in lines:
            data = line.strip().split()
            if len(data) == 6 and data[0] != "ID":
                if ":" in data[1]:
                    flight = Flight(data[0], data[3], data[4], data[1], data[2], int(data[5]))
                else:
                    flight = Flight(data[0], data[1], data[2], data[3], data[4], int(data[5]))
                flights.append(flight)
    except FileNotFoundError:
        return []
    return flights


def SaveFlights(flights, filename):
    f = open(filename, "w")
    f.write("ID TIMD TIMA DEPT ARRV PASS\n")
    for fl in flights:
        f.write(f"{fl.ID} {fl.DepartureTime} {fl.ArrivalTime} {fl.DepartureAirport} {fl.ArrivalAirport} {fl.Passangers}\n")
    f.close()


def ResetAssignments(flights):
    for flight in flights:
        flight.assigned_aircraft = None


def GetAssignedFlights(flights):
    assigned = []
    for flight in flights:
        if flight.assigned_aircraft is not None:
            assigned.append(flight)
    return assigned


def GetUnassignedFlights(flights):
    unassigned = []
    for flight in flights:
        if flight.assigned_aircraft is None:
            unassigned.append(flight)
    return unassigned


# test section
if __name__ == "__main__":
    flights = LoadFlights("Operations.txt")
    PrintFlights(flights)