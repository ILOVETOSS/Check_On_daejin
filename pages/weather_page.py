import tkinter as tk
from tkinter import ttk
from utils.calculations import get_uv_level, get_pm10_level

class WeatherPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F5F7FA")
        self.controller = controller

        tk.Label(self, text="환경 데이터", font=("맑은 고딕", 24), bg="#F5F7FA").pack(pady=20)
        self.temp_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg="#F5F7FA")
        self.temp_label.pack(pady=5)
        self.hum_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg="#F5F7FA")
        self.hum_label.pack(pady=5)
        self.uv_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg="#F5F7FA")
        self.uv_label.pack(pady=5)
        self.pm_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg="#F5F7FA")
        self.pm_label.pack(pady=5)

        ttk.Button(self, text="홈으로", style="Primary.TButton",
                   command=lambda: controller.show_frame("HomePage")).pack(pady=20)

    def on_show(self):
        data = self.controller.data
        self.temp_label.config(text=f"온도: {data['temperature']}°C")
        self.hum_label.config(text=f"습도: {data['humidity']}%")
        uv_text, uv_color = get_uv_level(data['uv_index'])
        self.uv_label.config(text=f"UV 지수: {data['uv_index']} ({uv_text})", fg=uv_color)
        pm_text, pm_color = get_pm10_level(data['pm10'])
        self.pm_label.config(text=f"PM10: {data['pm10']} ({pm_text})", fg=pm_color)
