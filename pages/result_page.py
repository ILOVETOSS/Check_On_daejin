import tkinter as tk

BG_COLOR = "#F5F7FA"

class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        tk.Label(self, text="체크리스트 결과", font=("맑은 고딕", 24), bg=BG_COLOR).pack(pady=20)
        self.result_label = tk.Label(self, text="", font=("맑은 고딕", 18), bg=BG_COLOR)
        self.result_label.pack(pady=20)

    def on_show(self):
        checklist = self.controller.data.get("checklist_items", {})
        completed = [k for k, v in checklist.items() if v]
        pending = [k for k, v in checklist.items() if not v]
        self.result_label.config(
            text=f"✅ 완료: {', '.join(completed) if completed else '없음'}\n"
                 f"❌ 미완료: {', '.join(pending) if pending else '없음'}"
        )
