class Aircraft:
    def __init__(self, callsign, type, capacity, airport=""):
        self.callsign = callsign
        self.type = type
        self.capacity = int(capacity)
        self.airport = airport

def PrintAircraft(aircraft):
    print("Callsign:", aircraft.callsign)
    print("Type:", aircraft.type)
    print("Capacity:", aircraft.capacity)
    print("Airport:", aircraft.airport)

def LoadAircrafts(filename):
    aircrafts = []
    try:
        with open(filename, "r") as F:
            for line in F:
                parts = line.strip().split()
                if len(parts) >= 3:
                    try:
                        callsign = parts[0]
                        ac_type = parts[1]
                        capacity = int(parts[2])
                        airport = parts[3] if len(parts) >= 4 else ""
                        aircrafts.append(Aircraft(callsign, ac_type, capacity, airport))
                    except ValueError:
                        continue
    except FileNotFoundError:
        return []
    return aircrafts

def LoadInitialPositions(aircrafts, filename):
    """Asigna el aeropuerto inicial a cada avión leyendo AircraftInitialPositions_X.txt"""
    try:
        with open(filename, "r") as F:
            for line in F:
                parts = line.strip().split()
                if len(parts) == 3 and parts[0] != "CALLSIGN":
                    callsign, _, airport = parts
                    for ac in aircrafts:
                        if ac.callsign == callsign:
                            ac.airport = airport
    except FileNotFoundError:
        return -1
    return 0

def SaveAircrafts(aircrafts, filename):
    with open(filename, "w") as file:
        file.write("CALLSIGN AC-TYPE SEATS AIRPORT\n")
        for aircraft in aircrafts:
            file.write(f"{aircraft.callsign} {aircraft.type} {aircraft.capacity} {aircraft.airport}\n")

def SaveAircraftPositions(aircrafts, filename):
    """Guarda las ubicaciones de los aviones en el formato oficial CALLSIGN AC-TYPE AIRP"""
    with open(filename, "w") as file:
        file.write("CALLSIGN AC-TYPE AIRP\n")
        for aircraft in aircrafts:
            file.write(f"{aircraft.callsign} {aircraft.type} {aircraft.airport}\n")

def PrintAircrafts(aircrafts):
    for aircraft in aircrafts:
        PrintAircraft(aircraft)
        print("-" * 20)

def AddAircrafts(aircrafts, aircraft):
    aircrafts.append(aircraft)

def RemoveAircrafts(aircrafts, callsign):
    for aircraft in aircrafts:
        if aircraft.callsign == callsign:
            aircrafts.remove(aircraft)
            return 0
    return -1

# test section
if __name__ == "__main__":
    loaded_aircrafts = LoadAircrafts("Aircrafts.txt")
    LoadInitialPositions(loaded_aircrafts, "AircraftInitialPositions_A.txt")
    print("Loaded aircrafts with initial positions:")
    PrintAircrafts(loaded_aircrafts)

    SaveAircraftPositions(loaded_aircrafts, "AircraftPositions_End.txt")
    print("Saved positions to AircraftPositions_End.txt")