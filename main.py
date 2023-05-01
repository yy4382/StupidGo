import tkinter as tk


class GoBasicAttributes:
    def __init__(self, window_size, board_size):
        self.window_size = window_size
        self.board_size = board_size
        self.board_coordinates = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.board_status = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.cell_size = window_size / (board_size + 1)


class GoCore:
    def __init__(self, parent):
        self.parent = parent
        self.basic_attributes = self.parent.basic_attributes
        self.board = self.basic_attributes.board_status
        self.current_player = 1

    def place_stone(self, i, j):
        if self.board[i][j] != 0:
            return False
        else:
            self.board[i][j] = self.current_player
            self.current_player = 3 - self.current_player
            return True


class GoBoard(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.core = parent.core
        self.basic_attributes = parent.basic_attributes
        # the Go board is a board_size * board_size grid
        self.board_size = self.basic_attributes.board_size

        # cell_size is the size of each cell in the board, including the border
        # calculated automatically by window_size and board_size
        self.cell_size = self.basic_attributes.cell_size

        # create the canvas
        self.board = tk.Canvas(self, width=self.basic_attributes.window_size, height=self.basic_attributes.window_size)

        # calculate the coordinates of each cell
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.basic_attributes.board_coordinates[i][j] = (self.cell_size * (i + 1), self.cell_size * (j + 1))

        # draw the board
        self.board.pack()
        self.draw_board()
        self.board.bind("<Button-1>", self.on_board_click)

    def draw_board(self):
        # draw lines
        for i in range(0, self.board_size):
            # draw horizontal lines
            self.board.create_line(self.basic_attributes.board_coordinates[0][i][0],
                                   self.basic_attributes.board_coordinates[0][i][1],
                                   self.basic_attributes.board_coordinates[self.board_size - 1][i][0],
                                   self.basic_attributes.board_coordinates[self.board_size - 1][i][1])
            # draw vertical lines
            self.board.create_line(self.basic_attributes.board_coordinates[i][0][0],
                                   self.basic_attributes.board_coordinates[i][0][1],
                                   self.basic_attributes.board_coordinates[i][self.board_size - 1][0],
                                   self.basic_attributes.board_coordinates[i][self.board_size - 1][1])
            # draw stars
            if i == 3 or i == 9 or i == 15:
                self.board.create_oval(self.basic_attributes.board_coordinates[i][3][0] - self.cell_size / 8,
                                       self.basic_attributes.board_coordinates[i][3][1] - self.cell_size / 8,
                                       self.basic_attributes.board_coordinates[i][3][0] + self.cell_size / 8,
                                       self.basic_attributes.board_coordinates[i][3][1] + self.cell_size / 8,
                                       fill="black")
                self.board.create_oval(self.basic_attributes.board_coordinates[i][9][0] - self.cell_size / 8,
                                       self.basic_attributes.board_coordinates[i][9][1] - self.cell_size / 8,
                                       self.basic_attributes.board_coordinates[i][9][0] + self.cell_size / 8,
                                       self.basic_attributes.board_coordinates[i][9][1] + self.cell_size / 8,
                                       fill="black")
                self.board.create_oval(self.basic_attributes.board_coordinates[i][15][0] - self.cell_size / 8,
                                       self.basic_attributes.board_coordinates[i][15][1] - self.cell_size / 8,
                                       self.basic_attributes.board_coordinates[i][15][0] + self.cell_size / 8,
                                       self.basic_attributes.board_coordinates[i][15][1] + self.cell_size / 8,
                                       fill="black")
            # write the coordinates
            self.board.create_text(self.basic_attributes.board_coordinates[i][0][0],
                                   self.basic_attributes.board_coordinates[i][self.board_size - 1][
                                       1] + self.cell_size / 2,
                                   text=chr(i + ord('a')))
            self.board.create_text(self.basic_attributes.board_coordinates[0][i][0] - self.cell_size / 2,
                                   self.basic_attributes.board_coordinates[0][i][1],
                                   text=str(self.board_size - i))

    def on_board_click(self, event):
        # calculate the coordinates of the clicked cell
        x = event.x
        y = event.y
        i = int((x + self.cell_size / 2) / self.cell_size) - 1
        j = int((y + self.cell_size / 2) / self.cell_size) - 1

        # judge whether the click is valid
        if i < 0 or i >= self.board_size or j < 0 or j >= self.board_size:
            print("invalid click")
            return
        print(f"player:{self.core.current_player} ({i}, {j})")
        
        if self.core.place_stone(i, j):
            self.draw_stone(i, j, self.core.current_player)

    def draw_stone(self, i, j, current_player):
        # 由于current_player在传入之前已经更新，所以要反着来
        if current_player == 2:
            self.board.create_oval(self.basic_attributes.board_coordinates[i][j][0] - self.cell_size / 3,
                                   self.basic_attributes.board_coordinates[i][j][1] - self.cell_size / 3,
                                   self.basic_attributes.board_coordinates[i][j][0] + self.cell_size / 3,
                                   self.basic_attributes.board_coordinates[i][j][1] + self.cell_size / 3,
                                   fill="black")
        elif current_player == 1:
            self.board.create_oval(self.basic_attributes.board_coordinates[i][j][0] - self.cell_size / 3,
                                   self.basic_attributes.board_coordinates[i][j][1] - self.cell_size / 3,
                                   self.basic_attributes.board_coordinates[i][j][0] + self.cell_size / 3,
                                   self.basic_attributes.board_coordinates[i][j][1] + self.cell_size / 3,
                                   fill="white")


class Go(tk.Tk):
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
    go = Go()
    go.mainloop()
