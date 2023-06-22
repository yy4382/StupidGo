from GoCore import GoBasicAttributes
from GoBoard import GoBoard
from GoCore import GoCore
import tkinter as tk


class GoControl(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.basic_attributes = GoBasicAttributes(500, 19)
        self.core = GoCore(self)
        self.title("Go")
        self.geometry("1000x500")
        self.geometry(f"{self.basic_attributes.window_size}x{self.basic_attributes.window_size}")
        self.resizable(False, False)
        self.board = GoBoard(self)
        self.board.pack()
        self.end_button = tk.Button(self,text="终局",command=self.core.end_of_game)
        self.end_button.pack()


if __name__ == '__main__':
    go = GoControl()
    go.mainloop()
