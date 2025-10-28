import tkinter as tk
from tkinter import ttk, messagebox
from pages.home_page import HomePage
from pages.weather_page import WeatherPage
from pages.checklist_page import ChecklistPage
from utils.calculations import calculate_heat_index
from utils.api import read_temperature, read_humidity
import os

BG = "#F5F7FA"

class SafetyMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("안전 모니터링 시스템")
        self.geometry("800x600")
        self.configure(bg=BG)

        self.setup_styles()

        self.data = {
            "temperature": 28.0,
            "humidity": 65.0,
            "uv_index": 7.0,
            "pm10": 45.0,
            "checklist_items": {}
        }

        container = tk.Frame(self, bg=BG)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, WeatherPage, ChecklistPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Navigation Bar
        nav_frame = tk.Frame(self, bg="#FFFFFF", height=30)
        nav_frame.pack(side="bottom", fill="x")

        self.nav_icons = {}
        for name, img_path in [("weather","assets/weather.png"),
                               ("home","assets/home.png"),
                               ("checklist","assets/checklist.png")]:
            icon = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), img_path)).subsample(2,2)
            btn = tk.Button(nav_frame, image=icon, bg="#FFFFFF", bd=0,
                            command=lambda n=name: self.show_frame(f"{n.capitalize()}Page"))
            btn.pack(side="left", expand=True, fill="x")
            self.nav_icons[name] = icon  # 레퍼런스 유지

        self.show_frame("HomePage")
        self.update_sensor_data()
        self.check_heat_index()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        for name, color in [("Primary.TButton","#3B82F6"), ("Secondary.TButton","#10B981")]:
            style.configure(name, background=color, foreground="white",
                            font=("맑은 고딕", 12, "bold"), padding=(20,10), borderwidth=0)
            style.map(name, background=[('active', color)])

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def update_sensor_data(self):
        self.data["temperature"] = read_temperature()
        self.data["humidity"] = read_humidity()
        self.after(60000, self.update_sensor_data)

    def check_heat_index(self):
        heat_index = calculate_heat_index(self.data["temperature"], self.data["humidity"])
        if heat_index >= 35:
            self.show_frame("ChecklistPage")
            messagebox.showwarning(
                "⚠️ 체감온도 위험",
                f"체감온도가 {heat_index}°C로 위험합니다!\n체크리스트를 확인해주세요."
            )
        self.after(300000, self.check_heat_index)
