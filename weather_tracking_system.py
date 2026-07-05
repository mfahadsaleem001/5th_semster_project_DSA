import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = "696fdb0**************************"

class weather:
    def __init__(self, city, date, humidity, temp, wind):
        self.city = city
        self.date = date
        self.humidity = humidity
        self.temp = temp
        self.wind = wind

class weather_system:
    def __init__(self):
        self.record = []
        self.map = {}

    def add_record(self, city):
        url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"

        try:
            response = requests.get(url)
            data = response.json()

            if "error" in data:
                return "City Not Found!"

            date = data["location"]["localtime"]
            humidity = data["current"]["humidity"]
            temp = data["current"]["temp_c"]
            wind = data["current"]["wind_kph"]

            w = weather(city, date, humidity, temp, wind)

            self.record.append(w)
            self.map[city.lower()] = w

            return "Record Added Successfully!"

        except:
            return "Unable To Fetch Weather!"

    def search_record(self, city):
        if city.lower() in self.map:
            w = self.map[city.lower()]

            return (
                f"City : {w.city}\n"
                f"Date : {w.date}\n"
                f"Temperature : {w.temp} °C\n"
                f"Humidity : {w.humidity}%\n"
                f"Wind : {w.wind} km/h"
            )
        return "Record Not Found!"

    def display_all_records(self):
        if not self.record:
            return "No Records Available!"

        result = ""

        for w in self.record:

            result += (
                f"City : {w.city}\n"
                f"Date : {w.date}\n"
                f"Temperature : {w.temp} °C\n"
                f"Humidity : {w.humidity}%\n"
                f"Wind : {w.wind} km/h\n"
                "-----------------------------\n"
            )

        return result

    def delete_record(self, city):
        if city.lower() in self.map:
            w = self.map[city.lower()]
            self.record.remove(w)
            del self.map[city.lower()]
            return "Record Deleted Successfully!"

        return "Record Not Found!"

    def maximum_temperature(self):
        if not self.record:
            return "No Records Available!"
        return f"Maximum Temperature: {max(w.temp for w in self.record)}"

    def minimum_temperature(self):
        if not self.record:
            return "No Records Available!"
        return f"Minimum Temperature: {min(w.temp for w in self.record)}"

    def average_temperature(self):
        if not self.record:
            return "No Records Available!"
        avg = sum(w.temp for w in self.record) / len(self.record)
        return f"Average Temperature: {avg:.2f}"

ws = weather_system()

def add_record_ui():
    city = city_entry.get()
    if city == "":
        messagebox.showerror("Error", "Please Enter City Name")
        return

    msg = ws.add_record(city)

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, msg)

def show_output(text):
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, text)

root = tk.Tk()
root.title("Weather Tracking System")
root.geometry("550x500")
root.configure(bg="#edecf2")

tk.Label(
    root,
    text="Weather Tracking System",
    font=("Arial", 18, "bold"),
    bg="#ecf0f1",
    fg="#2c3e50"
).pack(pady=10)

def create_label(text):
    return tk.Label(
        root,
        text=text,
        bg="#ecf0f1",
        font=("Times New Roman", 10, "bold")
    )

create_label("City Name").pack()
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=3)

btn_style = {
    "font": ("Times New Roman", 11, "bold"),
    "width": 28,
    "bg": "#2c3e50",
    "fg": "white",
    "activebackground": "#34495e",
    "activeforeground": "white",
    "bd": 0,
    "cursor": "hand2"
}

tk.Button(
    root,
    text="Add Record",
    command=add_record_ui,
    **btn_style
).pack(pady=4)

tk.Button(
    root,
    text="Search Record",
    command=lambda: show_output(ws.search_record(city_entry.get())),
    **btn_style
).pack(pady=4)

tk.Button(
    root,
    text="Display All Records",
    command=lambda: show_output(ws.display_all_records()),
    **btn_style
).pack(pady=4)

tk.Button(
    root,
    text="Delete Record",
    command=lambda: show_output(ws.delete_record(city_entry.get())),
    **btn_style
).pack(pady=4)

tk.Button(
    root,
    text="Maximum Temperature",
    command=lambda: show_output(ws.maximum_temperature()),
    bg="#27ae60",
    fg="white",
    font=("Arial", 11, "bold"),
    width=28,
    bd=0
).pack(pady=4)

tk.Button(
    root,
    text="Minimum Temperature",
    command=lambda: show_output(ws.minimum_temperature()),
    bg="#e67e22",
    fg="white",
    font=("Arial", 11, "bold"),
    width=28,
    bd=0
).pack(pady=4)

tk.Button(
    root,
    text="Average Temperature",
    command=lambda: show_output(ws.average_temperature()),
    bg="#8e44ad",
    fg="white",
    font=("Arial", 11, "bold"),
    width=28,
    bd=0
).pack(pady=4)


output_box = tk.Text(
    root,
    height=10,
    width=60,
    font=("Consolas", 10)
)

output_box.pack(pady=10)

root.mainloop()
