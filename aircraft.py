class Aircraft:
    def __init__(self, callsign, type, capacity, airport=""):
        self.callsign = callsign
        self.type = type
        self.capacity = capacity
        self.airport = airport


def PrintAircraft(aircraft):
    print("Callsign:", aircraft.callsign)
    print("Type:", aircraft.type)
    print("Capacity:", aircraft.capacity)
    print("Airport:", aircraft.airport)


def PrintAircrafts(aircrafts):
    for aircraft in aircrafts:
        PrintAircraft(aircraft)


def AddAircrafts(aircrafts, aircraft):
    aircrafts.append(aircraft)


def RemoveAircrafts(aircrafts, callsign):
    for aircraft in aircrafts:
        if aircraft.callsign == callsign:
            aircrafts.remove(aircraft)
            return 0
    return -1


def LoadAircrafts(filename):
    aircrafts = []
    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 3 and parts[2].isdigit():
                airport = parts[3] if len(parts) == 4 else ""
                aircraft = Aircraft(parts[0], parts[1], int(parts[2]), airport)
                aircrafts.append(aircraft)
    except FileNotFoundError:
        return []
    return aircrafts


def LoadInitialPositions(aircrafts, filename):
    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        for line in lines:
            parts = line.strip().split()
            if len(parts) == 3 and parts[0] != "CALLSIGN":
                for ac in aircrafts:
                    if ac.callsign == parts[0]:
                        ac.airport = parts[2]
        return 0
    except FileNotFoundError:
        return -1


def SaveAircrafts(aircrafts, filename):
    f = open(filename, "w")
    f.write("CALLSIGN AC-TYPE SEATS AIRPORT\n")
    for ac in aircrafts:
        f.write(f"{ac.callsign} {ac.type} {ac.capacity} {ac.airport}\n")
    f.close()


def SaveAircraftPositions(aircrafts, filename):
    f = open(filename, "w")
    f.write("CALLSIGN AC-TYPE AIRP\n")
    for ac in aircrafts:
        f.write(f"{ac.callsign} {ac.type} {ac.airport}\n")
    f.close()


# test section
if __name__ == "__main__":
    fleet = LoadAircrafts("Aircrafts.txt")
    LoadInitialPositions(fleet, "AircraftInitialPositions_A.txt")
    PrintAircrafts(fleet)