import tkinter as tk
from tkinter import ttk

BG = "#F5F7FA"

class ChecklistPage(tk.Frame):
    ITEMS = ["물 마시기", "그늘에서 휴식", "안전모 착용", "냉각 조끼 착용", "동료와 소통", "응급약품 확인"]

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        tk.Label(self, text="✅ 안전 체크리스트", font=("맑은 고딕", 24), bg=BG).pack(pady=20)
        tk.Label(self, text="⚠️ 체감온도가 높습니다! 아래 안전 수칙을 확인하세요", font=("맑은 고딕", 14), bg=BG).pack(pady=10)

        self.vars = {}
        for item in self.ITEMS:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self, text=item, variable=var, font=("맑은 고딕", 14), bg=BG)
            chk.pack(anchor="w", padx=40, pady=5)
            self.vars[item] = var

    def on_show(self):
        # 체크리스트 데이터 반영
        checklist = self.controller.data.get("checklist_items", {})
        for k, v in checklist.items():
            if k in self.vars:
                self.vars[k].set(v)
