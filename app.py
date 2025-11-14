import tkinter as tk
from tkinter import ttk, messagebox
from pages.home_page import HomePage
from pages.weather_page import WeatherPage
from pages.checklist_page import ChecklistPage
from utils.calculations import calculate_heat_index
from sensor_reader import read_temperature, read_humidity, stop_sensor_reader
import os
import atexit

BG = "#F5F7FA"

class SafetyMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Check-On")
        self.geometry("800x600")
        self.configure(bg=BG)

        self.setup_styles()

        # 센서 값 저장
        self.data = {
            "temperature": None,
            "humidity": None,
            "uv_index": 7.0,
            "pm10": 45.0,
            "checklist_items": {}
        }

        # 메인 프레임
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

        # 네비게이션 바
        self.create_navbar()

        # 첫 화면
        self.show_frame("HomePage")

        # 주기적 업데이트 (200ms)
        self.update_sensor_data()
        # 체감온도 체크 (5분)
        self.check_heat_index()

        # 앱 종료 시 센서 리더 정리
        atexit.register(stop_sensor_reader)

    # =============================
    # 스타일
    # =============================
    def setup_styles(self):
        style = ttk.Style()
        # 일부 환경에서 clam이 없을 수 있으니 try/except
        try:
            style.theme_use('clam')
        except Exception:
            pass
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
    # 네비게이션 바
    # =============================
    def create_navbar(self):
        nav_frame = tk.Frame(self, bg="#FFFFFF", height=70)
        nav_frame.pack(side="bottom", fill="x")
        nav_frame.pack_propagate(False)

        self.nav_icons = {}
        icons = [
            ("weather", "assets/weather.png"),
            ("home", "assets/home.png"),
            ("checklist", "assets/checklist.png")
        ]

        for name, img_path in icons:
            icon_path = os.path.join(os.path.dirname(__file__), img_path)
            # 파일이 없으면 예외 방지
            try:
                icon = tk.PhotoImage(file=icon_path).subsample(10, 10)
            except Exception:
                icon = None

            btn_frame = tk.Frame(nav_frame, bg="#FFFFFF")
            btn_frame.pack(side="left", expand=True, fill="both", padx=10, pady=8)

            btn = tk.Button(
                btn_frame,
                image=icon,
                text=name.capitalize() if icon is None else "",
                compound="top",
                bg="#FFFFFF",
                bd=0,
                activebackground="#E5E7EB",
                command=lambda n=name: self.show_frame(f"{n.capitalize()}Page")
            )
            btn.pack(expand=True)

            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#E5E7EB"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#FFFFFF"))

            self.nav_icons[name] = icon

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

            # None 체크 후 업데이트 (값 누락 시 기존값 유지)
            if temp is not None:
                self.data["temperature"] = temp
            if humid is not None:
                self.data["humidity"] = humid

            # 정보 로그 (둘다 존재할 때만 출력)
            if self.data["temperature"] is not None and self.data["humidity"] is not None:
                print(f"[INFO] 센서 업데이트 → 온도: {self.data['temperature']:.1f}°C  "
                      f"습도: {self.data['humidity']:.1f}%")

        except Exception as e:
            print(f"[ERROR] 센서 데이터 읽기 실패: {e}")

        # 200ms 주기: 터미널과 UI 동기화 개선
        self.after(500, self.update_sensor_data)

    # =============================
    # 체감온도 체크
    # =============================
    def check_heat_index(self):
        try:
            if (
                self.data["temperature"] is None or
                self.data["humidity"] is None
            ):
                # 아직 데이터 없음 -> 다음 주기까지 대기
                self.after(300000, self.check_heat_index)
                return

            heat_index = calculate_heat_index(
                self.data["temperature"],
                self.data["humidity"]
            )

            if heat_index >= 35:
                self.show_frame("ChecklistPage")
                messagebox.showwarning(
                    "⚠️ 체감온도 위험",
                    f"체감온도가 {heat_index:.1f}°C입니다!\n체크리스트를 확인하세요."
                )
        except Exception as e:
            print(f"[ERROR] 체감온도 계산 실패: {e}")

        # 5분마다 체크
        self.after(300000, self.check_heat_index)


if __name__ == "__main__":
    app = SafetyMonitorApp()
    app.mainloop()
