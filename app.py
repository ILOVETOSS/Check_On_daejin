import tkinter as tk
from tkinter import ttk, messagebox
from utils.calculations import calculate_heat_index, get_uv_level, get_pm10_level
from pages.home_page import HomePage
from pages.weather_page import WeatherPage
from pages.checklist_page import ChecklistPage
from pages.result_page import ResultPage
from utils.api import read_temperature, read_humidity

class SafetyMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("안전 모니터링 시스템")
        self.geometry("800x600")
        self.configure(bg="#F5F7FA")

        self.setup_styles()

        # 센서 데이터
        self.data = {
            "temperature": 28.0,
            "humidity": 65.0,
            "uv_index": 7.0,
            "pm10": 45.0,
            "checklist_items": {}
        }

        container = tk.Frame(self, bg="#F5F7FA")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, WeatherPage, ChecklistPage, ResultPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")
        self.update_sensor_data()
        self.check_heat_index()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        for name, color in [("Primary.TButton","#3B82F6"), ("Secondary.TButton","#10B981"), ("Warning.TButton","#F59E0B")]:
            style.configure(name, background=color, foreground="white", font=("맑은 고딕", 12, "bold"), padding=(20,10), borderwidth=0)
            style.map(name, background=[('active', color)])

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def update_sensor_data(self):
        """라즈베리파이 센서 데이터 업데이트"""
        self.data["temperature"] = read_temperature()
        self.data["humidity"] = read_humidity()
        # 1분마다 센서 업데이트
        self.after(60000, self.update_sensor_data)

    def check_heat_index(self):
        heat_index = calculate_heat_index(
            self.data["temperature"], self.data["humidity"]
        )
        if heat_index >= 35:
            self.show_frame("ChecklistPage")
            messagebox.showwarning(
                "⚠️ 체감온도 위험",
                f"체감온도가 {heat_index}°C로 위험합니다!\n체크리스트를 확인해주세요."
            )
        # 5분마다 체크
        self.after(300000, self.check_heat_index)
