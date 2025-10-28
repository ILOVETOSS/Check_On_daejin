import tkinter as tk

BG_COLOR = "#F5F7FA"
CARD_BG = "#3B82F6"
CARD_FG = "white"

class StatusPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        tk.Label(self, text="현재 작업장 상태", font=("맑은 고딕", 24), bg=BG_COLOR).pack(pady=50)

        self.card = tk.Frame(self, bg=CARD_BG, width=300, height=100)
        self.card.pack()
        self.card.pack_propagate(False)
        self.status_label = tk.Label(self.card, text=controller.data["status"], bg=CARD_BG, fg=CARD_FG, font=("맑은 고딕", 18))
        self.status_label.pack(expand=True)

    def on_show(self):
        self.status_label.config(text=self.controller.data["status"])
