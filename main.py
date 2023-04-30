import tkinter as tk


# 棋盘类
class GoBoard(tk.Frame):
    def __init__(self, parent, window_size, board_size=19):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # the Go board is a board_size * board_size grid
        self.board_size = board_size

        # cell_size is the size of each cell in the board, including the border
        # calculated automatically by window_size and board_size
        self.cell_size = window_size/(board_size + 1)
        self.board = tk.Canvas(self, width=window_size, height=window_size)
        self.board.pack()
        self.draw_board()

    def draw_board(self):
        # draw lines
        for i in range(1, self.board_size + 1):
            # draw horizontal lines
            self.board.create_line(self.cell_size, i * self.cell_size, self.cell_size * self.board_size,
                                   i * self.cell_size)
            # draw vertical lines
            self.board.create_line(i * self.cell_size, self.cell_size, i * self.cell_size,
                                   self.cell_size * self.board_size)


class Go(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Go")
        self.window_size = 500
        self.geometry(f"{self.window_size}x{self.window_size}")
        self.resizable(False, False)
        self.board = GoBoard(self, self.window_size)
        self.board.pack()


go = Go()
go.mainloop()
