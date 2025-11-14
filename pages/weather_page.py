import tkinter as tk
from collections import deque
from sensor_reader import read_temperature, read_humidity
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from matplotlib import rcParams

# 한글 깨짐 방지
rcParams['font.family'] = 'Malgun Gothic'
rcParams['axes.unicode_minus'] = False

class WeatherPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#f5f5f5")
        self.controller = controller

        # ===== 카드 데이터 =====
        self.cards_info = [
            {"title": "온도", "value": "-- °C"},
            {"title": "습도", "value": "-- %"},
            {"title": "체감온도", "value": "-- °C"},
            {"title": "PM10", "value": "-- µg/m³"},
            {"title": "UV 지수", "value": "--"}
        ]

        # ===== 카드 프레임 =====
        self.card_frame = tk.Frame(self, bg="#f5f5f5")
        self.card_frame.place(relx=0.5, rely=0.35, anchor="center")

        self.cards = []
        top_frame = tk.Frame(self.card_frame, bg="#f5f5f5")
        top_frame.pack(pady=15)
        bottom_frame = tk.Frame(self.card_frame, bg="#f5f5f5")
        bottom_frame.pack(pady=15)

        for i, info in enumerate(self.cards_info):
            if i < 3:
                card = self.create_card(top_frame, info, width=300, height=250)
            else:
                card = self.create_card(bottom_frame, info, width=300, height=250)
            self.cards.append(card)

        # ===== 최근 1시간 그래프 =====
        self.temp_data = deque(maxlen=720)
        self.humidity_data = deque(maxlen=720)
        self.feel_data = deque(maxlen=720)

        self.fig, self.ax = plt.subplots(figsize=(12,2))
        self.fig.patch.set_facecolor('#f5f5f5')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.85, anchor="center", relwidth=0.95, relheight=0.2)

        # ===== 센서 기반 데이터 갱신 시작 =====
        self.update_data()

    # ===== 카드 생성 =====
    def create_card(self, parent, info, width=200, height=200):
        card = tk.Frame(parent, bg="white", width=width, height=height, highlightbackground="#CCCCCC", highlightthickness=3)
        card.pack(side="left", padx=20, pady=10, expand=True, fill="both")

        title = tk.Label(card, text=info["title"], bg="white", fg="#333333", font=("Arial", 18, "bold"))
        title.pack(pady=(40,15))

        value = tk.Label(card, text=info["value"], bg="white", fg="#333333", font=("Arial", 36, "bold"))
        value.pack(pady=(15,40))

        card.value_label = value
        return card

    # ===== 데이터 갱신 (온습도 + PM10 + UV) =====
    def update_data(self):
        # ---- Arduino 센서 데이터 읽기 ----
        temp = read_temperature()
        humidity = read_humidity()

        # 센서 값이 None이면 기존값 유지
        if temp is None:
            temp = self.temp_data[-1] if self.temp_data else 0.0
        if humidity is None:
            humidity = self.humidity_data[-1] if self.humidity_data else 0.0

        # ---- 체감온도 계산 ----
        feel = round(temp + 0.33 * humidity - 4, 1)

        # ---- PM10, UV 지수 가져오기 (앱 데이터 연동) ----
        pm10 = self.controller.data.get("pm10", "--")
        uv = self.controller.data.get("uv_index", "--")

        # ---- 카드 업데이트 ----
        self.cards[0].value_label.config(text=f"{temp:.1f} °C")
        self.cards[1].value_label.config(text=f"{humidity:.1f} %")
        self.cards[2].value_label.config(text=f"{feel:.1f} °C")
        self.cards[3].value_label.config(text=f"{pm10} µg/m³")
        self.cards[4].value_label.config(text=f"{uv}")

        # ---- 그래프 데이터 추가 ----
        self.temp_data.append(temp)
        self.humidity_data.append(humidity)
        self.feel_data.append(feel)

        # ---- 그래프 갱신 ----
        self.ax.clear()
        self.ax.plot(list(self.temp_data), label="온도", color="orange")
        self.ax.plot(list(self.feel_data), label="체감온도", color="red")
        self.ax.plot(list(self.humidity_data), label="습도", color="blue")
        self.ax.set_title("최근 1시간 환경 데이터 변화", fontsize=12)
        self.ax.set_xlabel("시간 (5초 단위)", fontsize=10)
        self.ax.set_ylabel("값", fontsize=10)
        self.ax.legend(loc="upper right", fontsize=9)
        self.ax.set_ylim(0, max(max(self.temp_data + self.feel_data + self.humidity_data), 100)+5)
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.canvas.draw()

        # ---- 5초마다 갱신 ----
        self.after(5000, self.update_data)
