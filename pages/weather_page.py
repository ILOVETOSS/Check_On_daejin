import tkinter as tk
from utils.calculations import get_uv_level, get_pm10_level, calculate_heat_index

BG_COLOR = "#F5F7FA"

class WeatherPage(tk.Frame):
    def __init__(self, parent, controller, dev_mode=False): #데브모드
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.dev_mode = dev_mode

        # 타이틀
        tk.Label(self, text="환경 데이터", font=("맑은 고딕", 24), bg=BG_COLOR).pack(pady=20)

        # 데이터 레이블
        self.temp_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg=BG_COLOR)
        self.temp_label.pack(pady=5)
        self.hum_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg=BG_COLOR)
        self.hum_label.pack(pady=5)
        self.heat_label = tk.Label(self, text="", font=("맑은 고딕", 18, "bold"), bg=BG_COLOR, fg="red")
        self.heat_label.pack(pady=5)  # 체감온도
        self.uv_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg=BG_COLOR)
        self.uv_label.pack(pady=5)
        self.pm_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg=BG_COLOR)
        self.pm_label.pack(pady=5)

        # 개발자 모드: 슬라이더 추가
        if self.dev_mode:
            tk.Label(self, text="온도 테스트 (°C)", bg=BG_COLOR).pack(pady=(20,0))
            self.temp_slider = tk.Scale(self, from_=20, to=45, orient="horizontal", command=self.update_dev)
            self.temp_slider.set(28)
            self.temp_slider.pack(pady=5)

            tk.Label(self, text="습도 테스트 (%)", bg=BG_COLOR).pack(pady=(10,0))
            self.hum_slider = tk.Scale(self, from_=20, to=100, orient="horizontal", command=self.update_dev)
            self.hum_slider.set(65)
            self.hum_slider.pack(pady=5)

    def on_show(self):
        if self.dev_mode:
            self.update_dev()
        else:
            data = self.controller.data
            self.temp_label.config(text=f"온도: {data['temperature']}°C")
            self.hum_label.config(text=f"습도: {data['humidity']}%")
            heat_index = calculate_heat_index(data['temperature'], data['humidity'])
            self.heat_label.config(text=f"체감온도: {heat_index:.1f}°C")
            if heat_index >= 35:
                self.controller.show_frame("ChecklistPage")
            uv_text, uv_color = get_uv_level(data['uv_index'])
            self.uv_label.config(text=f"UV 지수: {data['uv_index']} ({uv_text})", fg=uv_color)
            pm_text, pm_color = get_pm10_level(data['pm10'])
            self.pm_label.config(text=f"PM10: {data['pm10']} ({pm_text})", fg=pm_color)

    def update_dev(self, event=None):
        """개발자 모드에서 슬라이더 값으로 체감온도 계산 및 체크리스트 자동 전환"""
        temp = self.temp_slider.get()
        hum = self.hum_slider.get()
        self.temp_label.config(text=f"온도: {temp}°C")
        self.hum_label.config(text=f"습도: {hum}%")
        heat_index = calculate_heat_index(temp, hum)
        self.heat_label.config(text=f"체감온도: {heat_index:.1f}°C")
        if heat_index >= 35:
            self.controller.show_frame("ChecklistPage")
