import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F5F7FA")
        self.controller = controller
        tk.Label(self, text="안전 모니터링 홈", font=("맑은 고딕", 24), bg="#F5F7FA").pack(pady=50)

    def on_show(self):
        pass
