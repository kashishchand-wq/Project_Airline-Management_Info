import tkinter as tk
from tkinter import messagebox, filedialog

from aircraft import Aircraft, LoadAircrafts, SaveAircrafts, LoadInitialPositions, AddAircrafts, RemoveAircrafts
from flight import Flight, LoadFlights, SaveFlights, AddFlights, RemoveFlights
from airport import Airport, LoadAirports, SaveAirports, AddAirport, RemoveAirport
from airline import Airline, AssignFlightsA, AssignFlightsB, SaveEndOfDayPositions, PlotFlightsComparison, PlotAircraftRoutes


class AirlineInterface:
    def __init__(self, window):
        self.window = window
        self.window.title("Gestió d'Aerolínies - Versió 2")
        self.window.geometry("850x650")

        self.airline = Airline("Vueling", [], [], [])

        # Títol
        tk.Label(window, text="Aerolínia: " + self.airline.name, font=("Arial", 16, "bold")).pack(pady=8)

        # --- FILA 1: CÀRREGA I DESAMENT DE FITXERS ---
        frame_files = tk.Frame(window)
        frame_files.pack(pady=4)

        tk.Button(frame_files, text="Carregar Aircrafts", command=self.load_aircrafts).pack(side="left", padx=4)
        tk.Button(frame_files, text="Posicions Inicials", command=self.load_positions).pack(side="left", padx=4)
        tk.Button(frame_files, text="Carregar Airports", command=self.load_airports).pack(side="left", padx=4)
        tk.Button(frame_files, text="Carregar Operations", command=self.load_flights).pack(side="left", padx=4)
        tk.Button(frame_files, text="Desar Airports", command=self.save_airports).pack(side="left", padx=4)

        # --- FILA 2: ALGORISMES D'ASSIGNACIÓ I FINAL DEL DIA ---
        frame_algos = tk.Frame(window)
        frame_algos.pack(pady=4)

        tk.Button(frame_algos, text="Assignar Algorisme A (1 vol)", command=self.run_algo_a).pack(side="left", padx=5)
        tk.Button(frame_algos, text="Assignar Algorisme B (2 vols)", command=self.run_algo_b).pack(side="left", padx=5)
        tk.Button(frame_algos, text="Desar Posicions Final Dia", command=self.save_end_positions).pack(side="left", padx=5)

        # --- FILA 3: GRÀFICS DE MATPLOTLIB ---
        frame_plots = tk.Frame(window)
        frame_plots.pack(pady=4)

        tk.Button(frame_plots, text="Gràfic Comparatiu (A vs B)", command=self.show_comparison).pack(side="left", padx=5)

        tk.Label(frame_plots, text="Avió (o ALL):").pack(side="left", padx=5)
        self.ent_callsign = tk.Entry(frame_plots, width=10)
        self.ent_callsign.insert(0, "ALL")
        self.ent_callsign.pack(side="left", padx=2)

        tk.Button(frame_plots, text="Mapa de Rutes", command=self.show_routes).pack(side="left", padx=5)

        # --- FILA 4: AFEGIR / ELIMINAR AEROPORTS ---
        frame_ap = tk.Frame(window)
        frame_ap.pack(pady=6)

        tk.Label(frame_ap, text="Aeroport -> ICAO:").pack(side="left")
        self.ent_ap_code = tk.Entry(frame_ap, width=6)
        self.ent_ap_code.pack(side="left", padx=2)

        tk.Label(frame_ap, text="Lon:").pack(side="left")
        self.ent_ap_lon = tk.Entry(frame_ap, width=8)
        self.ent_ap_lon.pack(side="left", padx=2)

        tk.Label(frame_ap, text="Lat:").pack(side="left")
        self.ent_ap_lat = tk.Entry(frame_ap, width=8)
        self.ent_ap_lat.pack(side="left", padx=2)

        tk.Label(frame_ap, text="Nom:").pack(side="left")
        self.ent_ap_desc = tk.Entry(frame_ap, width=14)
        self.ent_ap_desc.pack(side="left", padx=2)

        tk.Button(frame_ap, text="+ Afegir", command=self.add_airport).pack(side="left", padx=3)
        tk.Button(frame_ap, text="- Eliminar ICAO", command=self.remove_airport).pack(side="left", padx=3)

        # --- CAIXA DE TEXT PRINCIPAL ---
        self.text_info = tk.Text(window, width=95, height=25)
        self.text_info.pack(padx=10, pady=10)

        self.show_all_data()

    def show_all_data(self):
        self.text_info.delete("1.0", tk.END)

        # 1. Mostrar Flota
        self.text_info.insert(tk.END, "--- FLEET (AVIONS) ---\n")
        for ac in self.airline.fleet:
            self.text_info.insert(tk.END, f"{ac.callsign} | {ac.type} | Capacitat: {ac.capacity} | Aeroport: {ac.airport}\n")

        # 2. Mostrar Aeroports
        self.text_info.insert(tk.END, "\n--- AIRPORTS (AEROPORTS) ---\n")
        for ap in self.airline.airports:
            self.text_info.insert(tk.END, f"{ap.code} | Lon: {ap.longitude}, Lat: {ap.latitude} | {ap.description}\n")

        # 3. Mostrar Vols (Assignats i No Assignats)
        self.text_info.insert(tk.END, "\n--- ASSIGNED FLIGHTS (VOLS ASSIGNATS) ---\n")
        for fl in self.airline.operations:
            if fl.assigned_aircraft is not None:
                self.text_info.insert(tk.END, f"Vol {fl.ID}: {fl.DepartureAirport} -> {fl.ArrivalAirport} ({fl.DepartureTime}-{fl.ArrivalTime}) | Pass: {fl.Passangers} | AVIÓ: {fl.assigned_aircraft}\n")

        self.text_info.insert(tk.END, "\n--- UNASSIGNED FLIGHTS (VOLS NO ASSIGNATS) ---\n")
        for fl in self.airline.operations:
            if fl.assigned_aircraft is None:
                self.text_info.insert(tk.END, f"Vol {fl.ID}: {fl.DepartureAirport} -> {fl.ArrivalAirport} ({fl.DepartureTime}-{fl.ArrivalTime}) | Pass: {fl.Passangers} | SENSE ASSIGNAR\n")

    # Funcions de càrrega i desament
    def load_aircrafts(self):
        fn = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if fn != "":
            self.airline.fleet = LoadAircrafts(fn)
            self.show_all_data()

    def load_positions(self):
        fn = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if fn != "":
            LoadInitialPositions(self.airline.fleet, fn)
            self.show_all_data()

    def load_airports(self):
        fn = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if fn != "":
            self.airline.airports = LoadAirports(fn)
            self.show_all_data()

    def save_airports(self):
        fn = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if fn != "":
            SaveAirports(self.airline.airports, fn)
            messagebox.showinfo("Desat", "Aeroports desats correctament.")

    def load_flights(self):
        fn = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if fn != "":
            self.airline.operations = LoadFlights(fn)
            self.show_all_data()

    # Gestió d'aeroports
    def add_airport(self):
        code = self.ent_ap_code.get().strip()
        lon = self.ent_ap_lon.get().strip()
        lat = self.ent_ap_lat.get().strip()
        desc = self.ent_ap_desc.get().strip()
        if code != "" and lon != "" and lat != "":
            AddAirport(self.airline.airports, Airport(code, float(lon), float(lat), desc))
            self.show_all_data()
        else:
            messagebox.showerror("Error", "Omple ICAO, Longitud i Latitud.")

    def remove_airport(self):
        code = self.ent_ap_code.get().strip()
        if RemoveAirport(self.airline.airports, code) == 0:
            self.show_all_data()
        else:
            messagebox.showerror("Error", "No s'ha trobat l'aeroport.")

    # Execució dels algorismes A i B
    def run_algo_a(self):
        assigned, unassigned = AssignFlightsA(self.airline)
        self.show_all_data()
        messagebox.showinfo("Algorisme A", f"Assignats: {len(assigned)}\nNo assignats: {len(unassigned)}")

    def run_algo_b(self):
        assigned, unassigned = AssignFlightsB(self.airline)
        self.show_all_data()
        messagebox.showinfo("Algorisme B", f"Assignats: {len(assigned)}\nNo assignats: {len(unassigned)}")

    def save_end_positions(self):
        fn = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if fn != "":
            SaveEndOfDayPositions(self.airline, fn)
            messagebox.showinfo("Desat", "Posicions de final del dia desades.")

    # Gràfics estàndard de Matplotlib
    def show_comparison(self):
        PlotFlightsComparison(self.airline)

    def show_routes(self):
        callsign = self.ent_callsign.get().strip()
        if callsign == "":
            callsign = "ALL"
        PlotAircraftRoutes(self.airline, callsign)


if __name__ == "__main__":
    root = tk.Tk()
    app = AirlineInterface(root)
    root.mainloop()