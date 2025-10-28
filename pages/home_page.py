import tkinter as tk

BG_COLOR = "#F5F7FA"

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        tk.Label(self, text="안전 모니터링 홈", font=("맑은 고딕", 24), bg=BG_COLOR).pack(pady=50)
