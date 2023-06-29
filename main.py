from GoCore import GoBasicAttributes
from GoBoard import GoBoard
from GoCore import GoCore
import tkinter as tk
import sys
from tkinter import messagebox
import tkinter.font

window_size = 500
board_size = 19
time_lim = 120  # 包干制的比赛计时，以分钟为单位


class GoTimer:
    def __init__(self, parent, time_limit, tag):
        self.parent = parent
        self.time_limit = time_limit
        self.remaining_time = time_limit
        self.tag = tag
        default_font = tkinter.font.nametofont("TkDefaultFont")
        self.label = tk.Label(parent, text=self.format_time(time_limit), font=(default_font.actual()['family'], 30),
                              anchor="w")
        self.cur_update_id = None

    def format_time(self, seconds):
        name = {1: "\n黑棋计时：    ", 2: "白棋计时：    "}
        mins, secs = divmod(seconds, 60)
        return name[self.tag] + f"{mins:02d}:{secs:02d}"

    def update(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.label.config(text=self.format_time(self.remaining_time))
            self.cur_update_id = self.parent.after(1000, self.update)
        else:
            name = {1: "黑棋超时负，白棋胜", 2: "白棋超时负，黑棋胜"}
            messagebox.showinfo("时间耗尽", name[self.tag])
            self.parent.end_of_game()

    def pause(self):
        self.parent.after_cancel(self.cur_update_id)
        self.cur_update_id = None

    def start(self):
        self.update()


class GoControl(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.basic_attributes = GoBasicAttributes(window_size, board_size)
        self.core = GoCore(self)
        self.title("Go")
        self.resizable(False, False)
        self.board = GoBoard(self)
        current_row = 0

        self.board.grid(row=current_row, column=0, columnspan=3)
        current_row += 1

        # draw buttons
        self.end_label = tk.Label(self,
                                  text="\n注意：按照中国规则的要求，须在确认终局前把单官收完，否则自动胜负判定可能报错或者给出错误结果",
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

        self.black_timer = GoTimer(self, time_lim * 60, 1)
        self.white_timer = GoTimer(self, time_lim * 60, 2)
        self.black_timer.label.grid(row=current_row, column=0, columnspan=3, sticky="w")
        current_row += 1
        self.white_timer.label.grid(row=current_row, column=0, columnspan=3, sticky="w")
        self.black_timer.start()

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

    def toggle_timer(self):
        if self.black_timer.cur_update_id is not None:
            self.black_timer.pause()
            self.white_timer.start()
        else:
            self.black_timer.start()
            self.white_timer.pause()


if __name__ == '__main__':
    go = GoControl()
    go.mainloop()
