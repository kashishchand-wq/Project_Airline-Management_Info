class Airport:
    def __init__(self, code, longitude, latitude, description=""):
        self.code = code
        self.longitude = longitude
        self.latitude = latitude
        self.description = description


def PrintAirport(airport):
    print("Code:", airport.code)
    print("Longitude:", airport.longitude)
    print("Latitude:", airport.latitude)
    print("Description:", airport.description)


def PrintAirports(airports):
    for airport in airports:
        PrintAirport(airport)


def AddAirport(airports, airport):
    for ap in airports:
        if ap.code == airport.code:
            return -1
    airports.append(airport)
    return 0


def RemoveAirport(airports, code):
    for ap in airports:
        if ap.code == code:
            airports.remove(ap)
            return 0
    return -1


def FindAirport(airports, code):
    for ap in airports:
        if ap.code == code:
            return ap
    return None


def LoadAirports(filename):
    airports = []
    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        for line in lines:
            parts = line.strip().split(maxsplit=2)
            if len(parts) >= 2 and parts[0] != "AIRP":
                coords = parts[1].split(",")
                lon = float(coords[0])
                lat = float(coords[1])
                desc = parts[2] if len(parts) == 3 else ""
                airports.append(Airport(parts[0], lon, lat, desc))
    except FileNotFoundError:
        return []
    return airports


def SaveAirports(airports, filename):
    f = open(filename, "w")
    f.write("AIRP CoordinateLongitude,Latitude Description\n")
    for ap in airports:
        f.write(f"{ap.code} {ap.longitude},{ap.latitude} {ap.description}\n")
    f.close()


# test section
if __name__ == "__main__":
    airports = LoadAirports("Airports.txt")
    PrintAirports(airports)