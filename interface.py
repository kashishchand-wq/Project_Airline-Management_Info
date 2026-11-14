import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==========================================
# MÓDULOS DE CLASES Y LÓGICA DE DATOS
# ==========================================

class Aircraft:
    def __init__(self, callsign, type, capacity):
        self.callsign = callsign
        self.type = type
        self.capacity = int(capacity)

def LoadAircrafts(filename):
    aircrafts = []
    try:
        with open(filename, "r") as F:
            for line in F:
                parts = line.strip().split()
                if len(parts) == 3 and parts[2].isdigit():
                    aircrafts.append(Aircraft(parts[0], parts[1], int(parts[2])))
    except FileNotFoundError:
        return []
    return aircrafts

def SaveAircrafts(aircrafts, filename):
    with open(filename, "w") as file:
        for aircraft in aircrafts:
            file.write(f"{aircraft.callsign} {aircraft.type} {aircraft.capacity}\n")

def AddAircrafts(aircrafts, aircraft):
    aircrafts.append(aircraft)

def RemoveAircrafts(aircrafts, callsign):
    for i, aircraft in enumerate(aircrafts):
        if aircraft.callsign == callsign:
            del aircrafts[i]
            return 0
    return -1

class Flight:
    def __init__(self, ID, DepartureAirport, ArrivalAirport, DepartureTime, ArrivalTime, Passangers):
        self.ID = ID
        self.DepartureAirport = DepartureAirport
        self.ArrivalAirport = ArrivalAirport
        self.DepartureTime = DepartureTime.strip()
        self.ArrivalTime = ArrivalTime.strip()
        self.Passangers = int(Passangers)

def TimeToMinutes(time_str):
    try:
        h, m = time_str.strip().split(":")
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
                if len(data) != 6:
                    continue

                # Autodetección de formato (operations.txt vs flights.txt)
                if ":" in data[1]:
                    flight_id, dep_time, arr_time, dep_air, arr_air, pass_str = data
                else:
                    flight_id, dep_air, arr_air, dep_time, arr_time, pass_str = data

                if not pass_str.isdigit():
                    continue

                dep_min = TimeToMinutes(dep_time)
                arr_min = TimeToMinutes(arr_time)
                if dep_min == -1 or arr_min == -1:
                    continue

                flights.append(Flight(flight_id, dep_air, arr_air, dep_time, arr_time, int(pass_str)))
    except FileNotFoundError:
        return []
    return flights

def SaveFlights(flights, filename):
    with open(filename, "w") as file:
        for flight in flights:
            file.write(
                f"{flight.ID} {flight.DepartureAirport} {flight.ArrivalAirport} {flight.DepartureTime} {flight.ArrivalTime} {flight.Passangers}\n")

def AddFlights(flights, flight):
    flights.append(flight)

def RemoveFlights(flights, flight_id):
    for i, flight in enumerate(flights):
        if flight.ID == flight_id:
            del flights[i]
            return 0
    return -1

class Airline:
    def __init__(self, name, fleet, operations):
        self.name = name
        self.fleet = fleet
        self.operations = operations

# ==========================================
# INTERFAZ GRÁFICA ESTILIZADA (TEMA CLARO)
# ==========================================

class AirlineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Airline Manager Pro")
        self.geometry("980x700")

        self.airline = Airline("Vueling", [], [])

        # Paleta de colores claros y limpios
        self.bg_main = "#f3f4f6"  # Gris muy claro de fondo
        self.card_bg = "#ffffff"  # Blanco puro para tarjetas
        self.accent_color = "#2563eb"  # Azul profesional
        self.fg_dark = "#1f2937"  # Texto principal (Gris oscuro)
        self.fg_muted = "#6b7280"  # Texto secundario (Gris medio)
        self.danger_color = "#dc2626"  # Rojo para eliminar
        self.input_bg = "#f9fafb"  # Fondo de cajas de texto
        self.border_color = "#e5e7eb"  # Color de bordes ligeros

        self.configure(bg=self.bg_main)
        self._apply_custom_styles()

        # Cabecera principal
        header_frame = tk.Frame(self, bg=self.card_bg, pady=15, padx=25, highlightbackground=self.border_color,
                                highlightthickness=1)
        header_frame.pack(fill="x")

        title_label = tk.Label(
            header_frame,
            text="✈ Airline Management System",
            font=("Segoe UI", 18, "bold"),
            bg=self.card_bg,
            fg=self.accent_color
        )
        title_label.pack(side="left")

        subtitle_label = tk.Label(
            header_frame,
            text="Panel de Control de Flota y Operaciones",
            font=("Segoe UI", 10),
            bg=self.card_bg,
            fg=self.fg_muted
        )
        subtitle_label.pack(side="right", pady=5)

        # Contenedor de pestañas
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_aircrafts = tk.Frame(notebook, bg=self.bg_main, padx=15, pady=15)
        self.tab_flights = tk.Frame(notebook, bg=self.bg_main, padx=15, pady=15)
        self.tab_plot = tk.Frame(notebook, bg=self.bg_main, padx=15, pady=15)

        notebook.add(self.tab_aircrafts, text="  🛩 Flota (Aircrafts)  ")
        notebook.add(self.tab_flights, text="  🛫 Operaciones (Flights)  ")
        notebook.add(self.tab_plot, text="  📊 Análisis de Vuelos  ")

        self._build_aircraft_tab()
        self._build_flight_tab()
        self._build_plot_tab()

    def _apply_custom_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Pestañas
        style.configure("TNotebook", background=self.bg_main, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background="#e5e7eb",
            foreground=self.fg_dark,
            padding=[15, 8],
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.accent_color)],
            foreground=[("selected", "#ffffff")]
        )

        # Tabla Treeview
        style.configure(
            "Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground=self.fg_dark,
            rowheight=30,
            font=("Segoe UI", 9),
            borderwidth=1,
            relief="solid"
        )
        style.configure(
            "Treeview.Heading",
            background="#f3f4f6",
            foreground=self.fg_dark,
            font=("Segoe UI", 9, "bold"),
            relief="flat"
        )
        style.map("Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", "#1e40af")])

    # ---------------------------------------------------------
    # PESTAÑA AIRCRAFTS
    # ---------------------------------------------------------
    
    def _build_aircraft_tab(self):
        card_form = tk.Frame(self.tab_aircrafts, bg=self.card_bg, padx=15, pady=15,
                             highlightbackground=self.border_color, highlightthickness=1)
        card_form.pack(fill="x", pady=(0, 15))

        tk.Label(card_form, text="Añadir Nuevo Avión", font=("Segoe UI", 11, "bold"), bg=self.card_bg,
                 fg=self.fg_dark).grid(row=0, column=0, columnspan=7, sticky="w", pady=(0, 10))

        tk.Label(card_form, text="Callsign", font=("Segoe UI", 9, "bold"), bg=self.card_bg, fg=self.fg_muted).grid(
            row=1, column=0, sticky="w")
        self.ent_ac_callsign = tk.Entry(card_form, bg=self.input_bg, fg=self.fg_dark, relief="solid", bd=1,
                                        font=("Segoe UI", 10))
        self.ent_ac_callsign.grid(row=2, column=0, padx=(0, 10), pady=5, ipady=4)

        tk.Label(card_form, text="Tipo", font=("Segoe UI", 9, "bold"), bg=self.card_bg, fg=self.fg_muted).grid(row=1,
                                                                                                               column=1,
                                                                                                               sticky="w")
        self.ent_ac_type = tk.Entry(card_form, bg=self.input_bg, fg=self.fg_dark, relief="solid", bd=1,
                                    font=("Segoe UI", 10))
        self.ent_ac_type.grid(row=2, column=1, padx=(0, 10), pady=5, ipady=4)

        tk.Label(card_form, text="Capacidad", font=("Segoe UI", 9, "bold"), bg=self.card_bg, fg=self.fg_muted).grid(
            row=1, column=2, sticky="w")
        self.ent_ac_cap = tk.Entry(card_form, bg=self.input_bg, fg=self.fg_dark, relief="solid", bd=1,
                                   font=("Segoe UI", 10))
        self.ent_ac_cap.grid(row=2, column=2, padx=(0, 10), pady=5, ipady=4)

        btn_add = tk.Button(card_form, text="+ Añadir Avión", command=self._add_aircraft, bg=self.accent_color,
                            fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", padx=15, pady=4)
        btn_add.grid(row=2, column=3, padx=10, pady=5)

        # Tabla
        self.tree_ac = ttk.Treeview(self.tab_aircrafts, columns=("Callsign", "Type", "Capacity"), show="headings")
        self.tree_ac.heading("Callsign", text="CALLSIGN")
        self.tree_ac.heading("Type", text="TIPO DE AVIÓN")
        self.tree_ac.heading("Capacity", text="CAPACIDAD DE PASAJEROS")
        self.tree_ac.pack(fill="both", expand=True)

        # Botones de Acción
        actions_frame = tk.Frame(self.tab_aircrafts, bg=self.bg_main, pady=10)
        actions_frame.pack(fill="x")

        tk.Button(actions_frame, text="📁 Cargar aircrafts.txt", command=self._load_aircrafts, bg=self.card_bg,
                  fg=self.fg_dark, font=("Segoe UI", 9, "bold"), relief="solid", bd=1, cursor="hand2", padx=10,
                  pady=5).pack(side="left", padx=(0, 10))
        tk.Button(actions_frame, text="💾 Guardar Fichero", command=self._save_aircrafts, bg=self.card_bg,
                  fg=self.fg_dark, font=("Segoe UI", 9, "bold"), relief="solid", bd=1, cursor="hand2", padx=10,
                  pady=5).pack(side="left")
        tk.Button(actions_frame, text="🗑 Eliminar Selección", command=self._remove_aircraft, bg=self.danger_color,
                  fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", padx=10, pady=5).pack(
            side="right")

    def _update_aircraft_table(self):
        for item in self.tree_ac.get_children():
            self.tree_ac.delete(item)
        for ac in self.airline.fleet:
            self.tree_ac.insert("", "end", values=(ac.callsign, ac.type, ac.capacity))

    def _add_aircraft(self):
        cs = self.ent_ac_callsign.get().strip()
        tp = self.ent_ac_type.get().strip()
        cap = self.ent_ac_cap.get().strip()
        if cs and tp and cap.isdigit():
            AddAircrafts(self.airline.fleet, Aircraft(cs, tp, int(cap)))
            self._update_aircraft_table()
            self.ent_ac_callsign.delete(0, tk.END)
            self.ent_ac_type.delete(0, tk.END)
            self.ent_ac_cap.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Comprueba los datos ingresados.")

    def _remove_aircraft(self):
        selected = self.tree_ac.selection()
        if selected:
            callsign = self.tree_ac.item(selected[0])["values"][0]
            RemoveAircrafts(self.airline.fleet, str(callsign))
            self._update_aircraft_table()

    def _load_aircrafts(self):
        fn = filedialog.askopenfilename(title="Cargar aircrafts.txt", filetypes=[("Text files", "*.txt")])
        if fn:
            self.airline.fleet = LoadAircrafts(fn)
            self._update_aircraft_table()

    def _save_aircrafts(self):
        fn = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if fn:
            SaveAircrafts(self.airline.fleet, fn)
            messagebox.showinfo("Éxito", "Lista de aviones guardada.")

    # ---------------------------------------------------------
    # PESTAÑA FLIGHTS
    # ---------------------------------------------------------
    
    def _build_flight_tab(self):
        card_form = tk.Frame(self.tab_flights, bg=self.card_bg, padx=15, pady=15, highlightbackground=self.border_color,
                             highlightthickness=1)
        card_form.pack(fill="x", pady=(0, 15))

        tk.Label(card_form, text="Programar Vuelo", font=("Segoe UI", 11, "bold"), bg=self.card_bg,
                 fg=self.fg_dark).grid(row=0, column=0, columnspan=7, sticky="w", pady=(0, 10))

        labels = ["ID Vuelo", "Origen", "Destino", "Hora Dep.", "Hora Arr.", "Pasajeros"]
        for idx, text in enumerate(labels):
            tk.Label(card_form, text=text, font=("Segoe UI", 8, "bold"), bg=self.card_bg, fg=self.fg_muted).grid(row=1,
                                                                                                                 column=idx,
                                                                                                                 sticky="w")

        self.ent_fl_id = tk.Entry(card_form, bg=self.input_bg, fg=self.fg_dark, relief="solid", bd=1, width=8,
                                  font=("Segoe UI", 10))
        self.ent_fl_dep = tk.Entry(card_form, bg=self.input_bg, fg=self.fg_dark, relief="solid", bd=1, width=8,
                                   font=("Segoe UI", 10))
        self.ent_fl_arr = tk.Entry(card_form, bg=self.input_bg, fg=self.fg_dark, relief="solid", bd=1, width=8,
                                   font=("Segoe UI", 10))
        self.ent_fl_deptime = tk.Entry(card_form, bg=self.input_bg, fg=self.fg_dark, relief="solid", bd=1, width=8,
                                       font=("Segoe UI", 10))
        self.ent_fl_arrtime = tk.Entry(card_form, bg=self.input_bg, fg=self.fg_dark, relief="solid", bd=1, width=8,
                                       font=("Segoe UI", 10))
        self.ent_fl_pax = tk.Entry(card_form, bg=self.input_bg, fg=self.fg_dark, relief="solid", bd=1, width=8,
                                   font=("Segoe UI", 10))

        entries = [self.ent_fl_id, self.ent_fl_dep, self.ent_fl_arr, self.ent_fl_deptime, self.ent_fl_arrtime,
                   self.ent_fl_pax]
        for idx, ent in enumerate(entries):
            ent.grid(row=2, column=idx, padx=(0, 8), pady=5, ipady=4)

        btn_add = tk.Button(card_form, text="+ Añadir", command=self._add_flight, bg=self.accent_color, fg="#ffffff",
                            font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", padx=15, pady=4)
        btn_add.grid(row=2, column=6, padx=5, pady=5)

        cols = ("ID", "DepAir", "ArrAir", "DepTime", "ArrTime", "Passengers", "Duration")
        self.tree_fl = ttk.Treeview(self.tab_flights, columns=cols, show="headings")
        headings = ["ID VUELO", "ORIGEN", "DESTINO", "SALIDA", "LLEGADA", "PASAJEROS", "DURACIÓN"]
        for c, h in zip(cols, headings):
            self.tree_fl.heading(c, text=h)
            self.tree_fl.column(c, width=100, anchor="center")
        self.tree_fl.pack(fill="both", expand=True)

        actions_frame = tk.Frame(self.tab_flights, bg=self.bg_main, pady=10)
        actions_frame.pack(fill="x")

        tk.Button(actions_frame, text="📁 Cargar flights.txt", command=self._load_flights, bg=self.card_bg,
                  fg=self.fg_dark, font=("Segoe UI", 9, "bold"), relief="solid", bd=1, cursor="hand2", padx=10,
                  pady=5).pack(side="left", padx=(0, 8))
        tk.Button(actions_frame, text="📁 Cargar operations.txt", command=self._load_operations, bg=self.card_bg,
                  fg=self.fg_dark, font=("Segoe UI", 9, "bold"), relief="solid", bd=1, cursor="hand2", padx=10,
                  pady=5).pack(side="left", padx=(0, 8))
        tk.Button(actions_frame, text="💾 Guardar Fichero", command=self._save_flights, bg=self.card_bg, fg=self.fg_dark,
                  font=("Segoe UI", 9, "bold"), relief="solid", bd=1, cursor="hand2", padx=10, pady=5).pack(side="left")
        tk.Button(actions_frame, text="🗑 Eliminar Selección", command=self._remove_flight, bg=self.danger_color,
                  fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", padx=10, pady=5).pack(
            side="right")

    def _update_flight_table(self):
        for item in self.tree_fl.get_children():
            self.tree_fl.delete(item)
        for fl in self.airline.operations:
            dur = FlightDuration(fl)
            dur_str = f"{dur} min" if dur != -1 else "Error"
            self.tree_fl.insert("", "end",
                                values=(fl.ID, fl.DepartureAirport, fl.ArrivalAirport, fl.DepartureTime, fl.ArrivalTime,
                                        fl.Passangers, dur_str))

    def _add_flight(self):
        fl_id = self.ent_fl_id.get().strip()
        dep = self.ent_fl_dep.get().strip()
        arr = self.ent_fl_arr.get().strip()
        dtime = self.ent_fl_deptime.get().strip()
        atime = self.ent_fl_arrtime.get().strip()
        pax = self.ent_fl_pax.get().strip()

        if TimeToMinutes(dtime) != -1 and TimeToMinutes(atime) != -1 and pax.isdigit():
            AddFlights(self.airline.operations, Flight(fl_id, dep, arr, dtime, atime, int(pax)))
            self._update_flight_table()
            for ent in [self.ent_fl_id, self.ent_fl_dep, self.ent_fl_arr, self.ent_fl_deptime, self.ent_fl_arrtime,
                        self.ent_fl_pax]:
                ent.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Revisa el formato de la hora (HH:MM) o los pasajeros.")

    def _remove_flight(self):
        selected = self.tree_fl.selection()
        if selected:
            fl_id = self.tree_fl.item(selected[0])["values"][0]
            RemoveFlights(self.airline.operations, str(fl_id))
            self._update_flight_table()

    def _load_flights(self):
        fn = filedialog.askopenfilename(title="Cargar flights.txt", filetypes=[("Text files", "*.txt")])
        if fn:
            self.airline.operations = LoadFlights(fn)
            self._update_flight_table()

    def _load_operations(self):
        fn = filedialog.askopenfilename(title="Cargar operations.txt", filetypes=[("Text files", "*.txt")])
        if fn:
            self.airline.operations = LoadFlights(fn)
            self._update_flight_table()

    def _save_flights(self):
        fn = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if fn:
            SaveFlights(self.airline.operations, fn)
            messagebox.showinfo("Éxito", "Lista de operaciones guardada.")

    # ---------------------------------------------------------
    # PESTAÑA PLOT / GRÁFICO
    # ---------------------------------------------------------
    
    def _build_plot_tab(self):
        control_frame = tk.Frame(self.tab_plot, bg=self.card_bg, padx=15, pady=12,
                                 highlightbackground=self.border_color, highlightthickness=1)
        control_frame.pack(fill="x", pady=(0, 15))

        tk.Button(control_frame, text="⚡ Generar / Actualizar Gráfico", command=self._plot_flights,
                  bg=self.accent_color, fg="#ffffff", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                  padx=15, pady=6).pack(side="left")

        self.plot_container = tk.Frame(self.tab_plot, bg=self.card_bg, highlightbackground=self.border_color,
                                       highlightthickness=1)
        self.plot_container.pack(fill="both", expand=True)

    def _plot_flights(self):
        for widget in self.plot_container.winfo_children():
            widget.destroy()

        hours = list(range(24))
        flights_per_hour = [0] * 24

        for flight in self.airline.operations:
            departure = TimeToMinutes(flight.DepartureTime)
            arrival = TimeToMinutes(flight.ArrivalTime)
            if departure == -1 or arrival == -1:
                continue
            if arrival <= departure:
                arrival += 24 * 60

            for hour in hours:
                start = hour * 60
                end = start + 60
                if departure < end and arrival > start:
                    flights_per_hour[hour] += 1

        # Gráfico adaptado al tema claro
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        fig.patch.set_facecolor("#ffffff")
        ax.set_facecolor("#f9fafb")

        ax.bar(hours, flights_per_hour, color="#2563eb", edgecolor="#1d4ed8", alpha=0.85)
        ax.set_xlabel("Hora del día", color=self.fg_muted, fontsize=10, fontweight="bold")
        ax.set_ylabel("Vuelos simultáneos en el aire", color=self.fg_muted, fontsize=10, fontweight="bold")
        ax.set_title(f"Tráfico Aéreo en Tiempo Real - {self.airline.name}", color=self.fg_dark, fontsize=12, pad=12,
                     fontweight="bold")

        ax.tick_params(colors=self.fg_dark)
        ax.spines['bottom'].set_color(self.border_color)
        ax.spines['top'].set_color(self.border_color)
        ax.spines['right'].set_color(self.border_color)
        ax.spines['left'].set_color(self.border_color)

        ax.set_xticks(hours)
        ax.set_xticklabels([f"{hour:02d}:00" for hour in hours], rotation=45)
        ax.grid(axis="y", linestyle="--", alpha=0.5, color="#e5e7eb")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == "__main__":
    app = AirlineApp()
    app.mainloop()
