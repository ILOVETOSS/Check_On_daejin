import tkinter as tk
from tkinter import ttk

BG_COLOR = "#F5F7FA"

class ChecklistPage(tk.Frame):
    ITEMS = ["물 충분히 섭취", "그늘에서 휴식", "모자 착용", "자외선 차단제", "환기 확인"]

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        tk.Label(self, text="체크리스트", font=("맑은 고딕", 28, "bold"), bg=BG_COLOR).pack(pady=30)
        self.vars = {}
        for item in self.ITEMS:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self, text=item, variable=var)
            chk.pack(anchor="w", padx=60, pady=15)  # 여백 늘리기
            chk.config(style="Checklist.TCheckbutton")  # 스타일 적용
            self.vars[item] = var

        # 체크박스 스타일
        style = ttk.Style()
        style.configure("Checklist.TCheckbutton", font=("맑은 고딕", 18))
    
    def on_show(self):
        for k, v in self.vars.items():
            v.set(self.controller.data["checklist_items"].get(k, False))
