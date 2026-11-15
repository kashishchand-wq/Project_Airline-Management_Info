import matplotlib.pyplot as plt
from aircraft import *
from flight import *
from airport import *


class Airline:
    def __init__(self, name, fleet, operations, airports=[]):
        self.name = name
        self.fleet = fleet
        self.operations = operations
        self.airports = airports


def PrintAirline(airline):
    print("Name:", airline.name)
    print("Fleet:")
    for aircraft in airline.fleet:
        PrintAircraft(aircraft)
    print("Operations:")
    for flight in airline.operations:
        PrintFlight(flight)


# Algorisme A: màxim 1 vol per avió
def AssignFlightsA(airline):
    ResetAssignments(airline.operations)
    used_aircrafts = []

    for flight in airline.operations:
        for ac in airline.fleet:
            if ac.callsign not in used_aircrafts and ac.capacity >= flight.Passangers and ac.airport == flight.DepartureAirport:
                flight.assigned_aircraft = ac.callsign
                used_aircrafts.append(ac.callsign)
                break

    return GetAssignedFlights(airline.operations), GetUnassignedFlights(airline.operations)


# Algorisme B: màxim 2 vols per avió i mínim 2h entre vols
def AssignFlightsB(airline):
    ResetAssignments(airline.operations)

    counts = []
    airports = []
    free_times = []
    for ac in airline.fleet:
        counts.append(0)
        airports.append(ac.airport)
        free_times.append(0)

    for flight in airline.operations:
        dep_min = TimeToMinutes(flight.DepartureTime)
        arr_min = TimeToMinutes(flight.ArrivalTime)
        if arr_min <= dep_min:
            arr_min += 24 * 60

        for i in range(len(airline.fleet)):
            ac = airline.fleet[i]
            if counts[i] < 2 and ac.capacity >= flight.Passangers and airports[i] == flight.DepartureAirport and dep_min >= free_times[i]:
                flight.assigned_aircraft = ac.callsign
                counts[i] += 1
                airports[i] = flight.ArrivalAirport
                free_times[i] = arr_min + 120
                break

    return GetAssignedFlights(airline.operations), GetUnassignedFlights(airline.operations)


def GetEndOfDayAircrafts(airline):
    end_fleet = []
    for ac in airline.fleet:
        final_airport = ac.airport
        for flight in airline.operations:
            if flight.assigned_aircraft == ac.callsign:
                final_airport = flight.ArrivalAirport
        end_fleet.append(Aircraft(ac.callsign, ac.type, ac.capacity, final_airport))
    return end_fleet


def SaveEndOfDayPositions(airline, filename):
    end_fleet = GetEndOfDayAircrafts(airline)
    SaveAircraftPositions(end_fleet, filename)


def CountFlightsPerHour(flights):
    hours = list(range(24))
    counts = [0] * 24
    for flight in flights:
        departure = TimeToMinutes(flight.DepartureTime)
        arrival = TimeToMinutes(flight.ArrivalTime)
        if arrival <= departure:
            arrival += 24 * 60

        for hour in hours:
            start = hour * 60
            end = start + 60
            if departure < end and arrival > start:
                counts[hour] += 1
    return counts


def PlotFlights(airline):
    hours = list(range(24))
    flights_per_hour = CountFlightsPerHour(airline.operations)

    plt.bar(hours, flights_per_hour)
    plt.xlabel("Hour of the day")
    plt.ylabel("Number of flights in the air")
    plt.title("Flights in the Air per Hour")
    plt.xticks(hours, [f"{h:02d}:00" for h in hours], rotation=45)
    plt.show()


def PlotFlightsComparison(airline, ax=None):
    saved = []
    for fl in airline.operations:
        saved.append(fl.assigned_aircraft)

    total_counts = CountFlightsPerHour(airline.operations)

    assigned_A, _ = AssignFlightsA(airline)
    counts_A = CountFlightsPerHour(assigned_A)

    assigned_B, _ = AssignFlightsB(airline)
    counts_B = CountFlightsPerHour(assigned_B)

    for i in range(len(airline.operations)):
        airline.operations[i].assigned_aircraft = saved[i]

    hours = list(range(24))
    show_now = (ax is None)
    if show_now:
        fig, ax = plt.subplots()

    ax.bar([h - 0.25 for h in hours], total_counts, width=0.25, label="Scheduled")
    ax.bar(hours, counts_A, width=0.25, label="Algorithm A")
    ax.bar([h + 0.25 for h in hours], counts_B, width=0.25, label="Algorithm B")

    ax.set_xlabel("Hour of the day")
    ax.set_ylabel("Flights in the air")
    ax.set_title("Flights Comparison")
    ax.set_xticks(hours)
    ax.set_xticklabels([f"{h:02d}:00" for h in hours], rotation=45)
    ax.legend()

    if show_now:
        plt.show()


def PlotAircraftRoutes(airline, callsign="ALL", ax=None):
    show_now = (ax is None)
    if show_now:
        fig, ax = plt.subplots()

    lons = []
    lats = []
    for ap in airline.airports:
        lons.append(ap.longitude)
        lats.append(ap.latitude)
        ax.text(ap.longitude, ap.latitude, ap.code)

    ax.scatter(lons, lats, color="gray", label="Airports")

    for flight in airline.operations:
        if flight.assigned_aircraft is not None:
            if callsign == "ALL" or flight.assigned_aircraft == callsign:
                dep = FindAirport(airline.airports, flight.DepartureAirport)
                arr = FindAirport(airline.airports, flight.ArrivalAirport)
                if dep is not None and arr is not None:
                    ax.plot([dep.longitude, arr.longitude], [dep.latitude, arr.latitude], marker="o", label=flight.ID)

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Routes: " + callsign)
    ax.legend()

    if show_now:
        plt.show()


# test section
if __name__ == "__main__":
    fleet = LoadAircrafts("Aircrafts.txt")
    LoadInitialPositions(fleet, "AircraftInitialPositions_A.txt")
    operations = LoadFlights("Operations.txt")
    airports = LoadAirports("Airports.txt")

    airline = Airline("Vueling", fleet, operations, airports)

    assigned_A, unassigned_A = AssignFlightsA(airline)
    print("Algorisme A -> Assignats:", len(assigned_A), "No assignats:", len(unassigned_A))

    assigned_B, unassigned_B = AssignFlightsB(airline)
    print("Algorisme B -> Assignats:", len(assigned_B), "No assignats:", len(unassigned_B))

    PlotFlightsComparison(airline)
    PlotAircraftRoutes(airline, "OY-PSC")