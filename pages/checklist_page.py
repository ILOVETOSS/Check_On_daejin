import tkinter as tk
from tkinter import ttk

class ChecklistPage(tk.Frame):
    ITEMS = ["물 충분히 섭취", "그늘에서 휴식", "모자 착용", "자외선 차단제", "환기 확인"]

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F5F7FA")
        self.controller = controller
        tk.Label(self, text="체크리스트", font=("맑은 고딕", 24), bg="#F5F7FA").pack(pady=20)
        self.vars = {}
        for item in self.ITEMS:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self, text=item, variable=var)
            chk.pack(anchor="w", padx=40, pady=5)
            self.vars[item] = var

        ttk.Button(self, text="홈으로", style="Primary.TButton",
                   command=self.save_and_back).pack(pady=20)

    def save_and_back(self):
        for k, v in self.vars.items():
            self.controller.data["checklist_items"][k] = v.get()
        self.controller.show_frame("HomePage")
