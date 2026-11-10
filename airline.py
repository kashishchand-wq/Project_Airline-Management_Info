class Airline:
   def __init__(self, name, fleet, operations):
       self.name = name
       self.fleet = fleet
       self.operations = operations

def PrintAirline (airline):
    print("Name: ", airline.name)
    print("Fleet: ")
    for aircraft in airline.fleet:
        PrintAircraft(aircraft)
    print("Operations: ")
    for flight in airline.operations:
        PrintFlight(flight)

import matplotlib.pyplot as plt

def PlotFlights (airline):
    hours = list(range(24))
    flights_per_hour = [0] * 24
    for flight in airline.flights:
        departure = TimeToMinutes(flight.DepartureTime)
        arrival = TimeToMinutes(flight.ArrivalTime)

        # Handle flights arriving on the next day
        if arrival <= departure:
            arrival += 24 * 60

        for hour in hours:
            start = hour * 60
            end = start + 60

            # Check whether the flight overlaps this hour
            if departure < end and arrival > start:
                flights_per_hour[hour] += 1

    plt.bar(hours, flights_per_hour)
    plt.xlabel("Hour of the day")
    plt.ylabel("Number of flights in the air")
    plt.title("Flights in the Air per Hour")
    plt.xticks(hours, [f"{hour:02d}:00" for hour in hours], rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

# test section
if __name__ == "__main__":
    from aircraft import *
    from flight import *

    #Test PrintAirline
    aircrafts = []
    aircrafts.append(Aircraft("AAAA", "A220-100", 135))
    aircrafts.append(Aircraft("BBBB", "A230-100", 200))

    flights = []
    flights.append(Flight("A11", "LEBL", "EGLL", "12: 30", "14: 30", 120))
    flights.append(Flight("A12", "EGLL", "LEBL", "16: 30", "18: 30", 150))

    airline = Airline("Vueling", aircrafts, flights)
    PrintAirline(airline)

    # Test PlotFlights
    flight1 = Flight("FL001", "LEBL", "LEPA", "08:30", "10:15", 120)
    flight2 = Flight("FL002", "LEPA", "LEMD", "09:00", "11:30", 150)
    flight3 = Flight("FL003", "LEMD", "LEBL", "23:00", "01:00", 100)

    airline.flights = [flight1, flight2, flight3]
    PlotFlights(airline)
