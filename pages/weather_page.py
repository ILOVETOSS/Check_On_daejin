import tkinter as tk
from tkinter import ttk
from utils.calculations import calculate_heat_index

class WeatherPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F5F7FA")
        self.controller = controller

        tk.Label(self, text="환경 데이터", font=("맑은 고딕", 24), bg="#F5F7FA").pack(pady=20)

        self.temp_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg="#F5F7FA")
        self.temp_label.pack(pady=5)
        self.hum_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg="#F5F7FA")
        self.hum_label.pack(pady=5)
        self.heat_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg="#F5F7FA")
        self.heat_label.pack(pady=5)

    def on_show(self):
        data = self.controller.data
        self.temp_label.config(text=f"온도: {data['temperature']}°C")
        self.hum_label.config(text=f"습도: {data['humidity']}%")
        heat_index = calculate_heat_index(data['temperature'], data['humidity'])
        self.heat_label.config(text=f"체감온도: {heat_index}°C")

        # 체감온도 일정 이상이면 자동 체크리스트 전환
        if heat_index >= 35:
            self.controller.show_frame("ChecklistPage")
