class Airport:
    def __init__(self, code, longitude, latitude, description=""):
        self.code = code
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.description = description

def PrintAirport(airport):
    print("ICAO Code:", airport.code)
    print("Longitude:", airport.longitude)
    print("Latitude:", airport.latitude)
    print("Description:", airport.description)

def PrintAirports(airports):
    for airport in airports:
        PrintAirport(airport)
        print("-" * 20)

def LoadAirports(filename):
    airports = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(maxsplit=2)
                if len(parts) >= 2 and parts[0] != "AIRP":
                    try:
                        code = parts[0]
                        lon_str, lat_str = parts[1].split(",")
                        lon = float(lon_str)
                        lat = float(lat_str)
                        desc = parts[2] if len(parts) == 3 else ""
                        airports.append(Airport(code, lon, lat, desc))
                    except ValueError:
                        continue
    except FileNotFoundError:
        return []
    return airports

def SaveAirports(airports, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("AIRP CoordinateLongitude,Latitude Description\n")
        for ap in airports:
            f.write(f"{ap.code} {ap.longitude},{ap.latitude} {ap.description}\n")

def AddAirport(airports, airport):
    # Evitar duplicados por código ICAO
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

# test section
if __name__ == "__main__":
    airports = LoadAirports("Airports.txt")
    print(f"Loaded {len(airports)} airports:")
    PrintAirports(airports[:3])

    new_ap = Airport("LEBL", 2.07846, 41.2971, "Barcelona-El Prat Airport")
    AddAirport(airports, new_ap)
    print("Added LEBL:", FindAirport(airports, "LEBL").description)

    SaveAirports(airports, "Airports_test.txt")
    RemoveAirport(airports, "LEBL")
    print("After removing LEBL, found:", FindAirport(airports, "LEBL"))