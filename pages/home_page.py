import tkinter as tk
from tkinter import ttk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F5F7FA")
        self.controller = controller
        label = tk.Label(self, text="안전 모니터링 홈", font=("맑은 고딕", 24), bg="#F5F7FA")
        label.pack(pady=50)

        btn_weather = ttk.Button(self, text="환경 데이터 확인", style="Primary.TButton",
                                 command=lambda: controller.show_frame("WeatherPage"))
        btn_weather.pack(pady=10)

        btn_checklist = ttk.Button(self, text="체크리스트 확인", style="Secondary.TButton",
                                   command=lambda: controller.show_frame("ChecklistPage"))
        btn_checklist.pack(pady=10)
