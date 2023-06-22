from GoCore import GoBasicAttributes
from GoBoard import GoBoard
from GoCore import GoCore
import tkinter as tk
import sys
from tkinter import messagebox

board_size = 500
board_style = 19


class GoControl(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.basic_attributes = GoBasicAttributes(board_size, board_style)
        self.core = GoCore(self)
        self.title("Go")
        # self.geometry(f"{self.basic_attributes.window_size}x{self.basic_attributes.window_size + 100}")
        self.resizable(False, False)
        self.board = GoBoard(self)
        current_row = 0

        self.board.grid(row=current_row, column=0, columnspan=3)
        current_row += 1

        self.end_label = tk.Label(self,
                                  text="\n注意：按照中国规则的要求，须在确认终局前把单官收完，否则自动判定胜负无法正常工作",
                                  anchor='w')
        self.end_label.grid(row=current_row, column=0, columnspan=3, sticky='w')
        current_row += 1
        self.end_btn = tk.Button(self, text="确认终局", command=self.core.on_end_btn_clicked)
        self.end_btn.grid(row=current_row, column=0)
        self.black_fail_btn = tk.Button(self, text="黑棋认负", command=self.on_black_fail_btn_clicked)
        self.black_fail_btn.grid(row=current_row, column=1)
        self.white_fail_btn = tk.Button(self, text="白棋认负", command=self.on_white_fail_btn_clicked)
        self.white_fail_btn.grid(row=current_row, column=2)
        current_row += 1

        self.log_label = tk.Label(self, text="\n提示与日志：", anchor="w")
        self.log_label.grid(row=current_row, column=0, columnspan=3, sticky="w")
        current_row += 1
        self.log_box = tk.Text(self, state='disabled', height=8)
        self.log_box.grid(row=current_row, column=0, columnspan=3)
        current_row += 1

        sys.stdout.write = self.update_log_box

    def update_log_box(self, s):
        self.log_box.configure(state='normal')
        self.log_box.insert(tk.END, s)
        self.log_box.configure(state='disabled')
        self.log_box.see(tk.END)

    def end_of_game(self):
        self.board.board.unbind("<Button-1>")
        self.end_btn.config(state=tk.DISABLED)
        self.black_fail_btn.config(state=tk.DISABLED)
        self.white_fail_btn.config(state=tk.DISABLED)

    def on_black_fail_btn_clicked(self):
        messagebox.showinfo("认负结果", "白棋赢")
        self.end_of_game()
    def on_white_fail_btn_clicked(self):
        messagebox.showinfo("认负结果", "黑棋赢")
        self.end_of_game()


if __name__ == '__main__':
    go = GoControl()
    go.mainloop()
