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
        self.title("Check-On")
        self.geometry("800x600")
        self.configure(bg=BG)

        self.setup_styles()

        # 기본 데이터
        self.data = {
            "temperature": 28.0,
            "humidity": 65.0,
            "uv_index": 7.0,
            "pm10": 45.0,
            "checklist_items": {}
        }

        # 메인 컨테이너
        container = tk.Frame(self, bg=BG)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # 페이지 등록
        self.frames = {}
        for F in (HomePage, WeatherPage, ChecklistPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # 하단 네비게이션 바
        self.create_navbar()

        # 첫 화면
        self.show_frame("HomePage")

        # 주기적 업데이트
        self.update_sensor_data()
        self.check_heat_index()

    # =============================
    # 스타일 설정
    # =============================
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        for name, color in [
            ("Primary.TButton", "#3B82F6"),
            ("Secondary.TButton", "#10B981")
        ]:
            style.configure(
                name,
                background=color,
                foreground="white",
                font=("맑은 고딕", 12, "bold"),
                padding=(20, 10),
                borderwidth=0
            )
            style.map(name, background=[('active', color)])

    # =============================
    # 네비게이션 바 생성
    # =============================
    def create_navbar(self):
        nav_frame = tk.Frame(self, bg="#FFFFFF", height=70)
        nav_frame.pack(side="bottom", fill="x")
        nav_frame.pack_propagate(False)  # 높이 고정

        # 아이콘 버튼 추가
        self.nav_icons = {}
        icons = [
            ("weather", "assets/weather.png"),
            ("home", "assets/home.png"),
            ("checklist", "assets/checklist.png")
        ]

        for name, img_path in icons:
            icon_path = os.path.join(os.path.dirname(__file__), img_path)
            icon = tk.PhotoImage(file=icon_path).subsample(10, 10)  # 510px → 48px 크기

            btn_frame = tk.Frame(nav_frame, bg="#FFFFFF")
            btn_frame.pack(side="left", expand=True, fill="both", padx=10, pady=8)

            btn = tk.Button(
                btn_frame,
                image=icon,
                bg="#FFFFFF",
                bd=0,
                activebackground="#E5E7EB",
                command=lambda n=name: self.show_frame(f"{n.capitalize()}Page")
            )
            btn.pack(expand=True)

            # hover 효과
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#E5E7EB"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#FFFFFF"))

            self.nav_icons[name] = icon  # 이미지 참조 유지

    # =============================
    # 페이지 전환
    # =============================
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

    # =============================
    # 센서 데이터 주기적 업데이트
    # =============================
    def update_sensor_data(self):
        try:
            temp = read_temperature()
            humid = read_humidity()
            if temp is not None:
                self.data["temperature"] = temp
            if humid is not None:
                self.data["humidity"] = humid
        except Exception as e:
            print(f"[ERROR] 센서 데이터 읽기 실패: {e}")

        self.after(60000, self.update_sensor_data)  # 1분마다

    # =============================
    # 체감온도 체크
    # =============================
    def check_heat_index(self):
        try:
            heat_index = calculate_heat_index(
                self.data["temperature"],
                self.data["humidity"]
            )
            if heat_index >= 35:
                self.show_frame("ChecklistPage")
                messagebox.showwarning(
                    "⚠️ 체감온도 위험",
                    f"체감온도가 {heat_index:.1f}°C로 위험합니다!\n체크리스트를 확인해주세요."
                )
        except Exception as e:
            print(f"[ERROR] 체감온도 계산 실패: {e}")

        self.after(300000, self.check_heat_index)  # 5분마다


if __name__ == "__main__":
    app = SafetyMonitorApp()
    app.mainloop()
