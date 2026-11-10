class Aircraft:
   def __init__(self, callsign, type, capacity):
       self.callsign = callsign
       self.type = type
       self.capacity = capacity

def PrintAircraft (aircraft):
    print("Callsign: ", aircraft.callsign)
    print("Type: ", aircraft.type)
    print("Capacity: ", aircraft.capacity)

def LoadAircrafts (filename):
    aircrafts = []
    try:
        with open(filename, "r") as F:
            for line in F:
                parts = line.strip().split()
                if len(parts) == 3:
                    callsign = parts[0]
                    type = parts[1]
                    capacity = int(parts[2])

                    aircraft = Aircraft(callsign, type, capacity)
                    aircrafts.append(aircraft)
    except FileNotFoundError:
        return []
    return aircrafts

def SaveAircrafts (aircrafts, filename):
    with open(filename, "w") as file:
        for aircraft in aircrafts:
            file.write(f"{aircraft.callsign} {aircraft.type} {aircraft.capacity}\n")

def PrintAircrafts (aircrafts):
    for aircraft in aircrafts:
        PrintAircraft(aircraft)

def AddAircrafts (aircrafts, aircraft):
    aircrafts.append(aircraft)

def RemoveAircrafts (aircrafts, callsign):
    for aircraft in aircrafts:
        if aircraft.callsign == callsign:
            aircrafts.remove(aircraft)
            return 0
    return -1

# test section
if __name__ == "__main__":
    # Create some aircrafts
    aircraft1 = Aircraft("AAAA", "A220-100", 135)
    aircraft2 = Aircraft("BBBB", "A230-100", 200)
    aircrafts = [aircraft1, aircraft2]

    # Test PrintAircrafts
    print("Initial aircrafts:")
    PrintAircrafts(aircrafts)

    # Test SaveAircrafts
    SaveAircrafts(aircrafts, "aircrafts-new.txt")
    print("\nAircrafts saved to file.")

    # Test LoadAircrafts
    loaded_aircrafts = LoadAircrafts("Aircrafts.txt")
    print("\nLoaded aircrafts:")
    PrintAircrafts(loaded_aircrafts)

    # Test AddAircraft
    aircraft3 = Aircraft("CCCC", "A320-200", 180)
    AddAircrafts(loaded_aircrafts, aircraft3)
    print("\nAfter adding an aircraft:")
    PrintAircrafts(loaded_aircrafts)

    # Test RemoveAircraft
    result = RemoveAircrafts(loaded_aircrafts, "BBBB")
    print("\nAfter removing aircraft BBBB:")
    PrintAircrafts(loaded_aircrafts)
    print("Remove result:", result)

    # Test removing a non-existing aircraft
    result = RemoveAircrafts(loaded_aircrafts, "XXXX")
    print("Remove non-existing aircraft result:", result)
