import tkinter as tk
from collections import deque
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

        # ===== 카드 프레임 (중앙 집중) =====
        self.card_frame = tk.Frame(self, bg="#f5f5f5")
        self.card_frame.place(relx=0.5, rely=0.35, anchor="center")

        self.cards = []

        # ===== 카드 2줄 배치 =====
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

    # ===== 데이터 갱신 =====
    def update_data(self):
        temp = round(random.uniform(29, 36), 1)
        humidity = random.randint(50, 90)
        feel = round(temp + random.uniform(-1, 1), 1)
        pm10 = random.randint(10, 80)
        uv = random.randint(0, 11)

        self.cards[0].value_label.config(text=f"{temp} °C")
        self.cards[1].value_label.config(text=f"{humidity} %")
        self.cards[2].value_label.config(text=f"{feel} °C")
        self.cards[3].value_label.config(text=f"{pm10} µg/m³")
        self.cards[4].value_label.config(text=f"{uv}")

        # 그래프 데이터 추가
        self.temp_data.append(temp)
        self.humidity_data.append(humidity)
        self.feel_data.append(feel)

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

        self.after(5000, self.update_data)

# ===== 테스트용 실행 =====
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1300x800")
    root.title("환경 데이터 모니터링")
    page = WeatherPage(root)
    page.pack(fill="both", expand=True)
    root.mainloop()
