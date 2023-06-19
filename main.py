from GoBasicAttributes import GoBasicAttributes
from GoBoard import GoBoard
from GoCore import GoCore
import tkinter as tk


class GoControl(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.basic_attributes = GoBasicAttributes(500, 19)
        self.core = GoCore(self)
        self.title("Go")
        self.geometry(f"{self.basic_attributes.window_size}x{self.basic_attributes.window_size}")
        self.resizable(False, False)
        self.board = GoBoard(self)
        self.board.pack()

if __name__ == '__main__':
    go = GoControl()
    go.mainloop()
