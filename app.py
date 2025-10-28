import tkinter as tk
from pages.home_page import HomePage
from pages.weather_page import WeatherPage
from pages.checklist_page import ChecklistPage
from utils.calculations import calculate_heat_index
from utils.api import read_temperature, read_humidity

BG_COLOR = "#F5F7FA"

class SafetyMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("안전 모니터링 시스템")
        self.geometry("800x600")
        self.configure(bg=BG_COLOR)

        # 센서 데이터
        self.data = {
            "temperature": 28.0,
            "humidity": 65.0,
            "uv_index": 7.0,
            "pm10": 45.0,
            "checklist_items": {}
        }

        # 전체 grid 설정
        self.rowconfigure(0, weight=1)  # 페이지 영역
        self.rowconfigure(1, weight=0)  # 네비게이션 바
        self.columnconfigure(0, weight=1)

        # 페이지 컨테이너
        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        # 페이지 프레임 생성
        self.frames = {}
        for F in (HomePage, WeatherPage, ChecklistPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # 하단 네비게이션 바
        nav_frame = tk.Frame(self, bg="#E5E7EB", height=60)
        nav_frame.grid(row=1, column=0, sticky="ew")
        nav_frame.columnconfigure((0,1,2), weight=1)

        # 홈을 중앙에 배치
        buttons = [
            ("환경", "WeatherPage"),
            ("홈", "HomePage"),
            ("체크리스트", "ChecklistPage")
        ]

        for i, (text, page) in enumerate(buttons):
            btn = tk.Button(nav_frame, text=text, command=lambda p=page: self.show_frame(p))
            btn.grid(row=0, column=i, sticky="nsew")
            btn.configure(bg="#3B82F6", fg="white", font=("맑은 고딕", 12, "bold"), bd=0)

        self.show_frame("HomePage")
        self.update_sensor_data()
        self.check_heat_index()

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
        heat_index = calculate_heat_index(
        self.data["temperature"], self.data["humidity"]
        )
        if heat_index >= 35:
            self.show_frame("ChecklistPage")
            tk.messagebox.showwarning(
                "⚠️ 체감온도 위험",
                f"체감온도가 {heat_index:.1f}°C로 위험합니다!\n체크리스트를 확인해주세요."
                )
        self.after(300000, self.check_heat_index) #123123

