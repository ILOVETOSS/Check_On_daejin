import tkinter as tk
from tkinter import ttk

class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F5F7FA")
        self.controller = controller
        tk.Label(self, text="결과 페이지", font=("맑은 고딕", 24), bg="#F5F7FA").pack(pady=20)
        self.result_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg="#F5F7FA")
        self.result_label.pack(pady=20)

        ttk.Button(self, text="홈으로", style="Primary.TButton",
                   command=lambda: controller.show_frame("HomePage")).pack(pady=20)

    def on_show(self):
        checklist = self.controller.data.get("checklist_items", {})
        completed = [k for k, v in checklist.items() if v]
        pending = [k for k, v in checklist.items() if not v]
        self.result_label.config(
            text=f"✅ 완료: {', '.join(completed)}\n❌ 미완료: {', '.join(pending)}"
        )
