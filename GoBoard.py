import tkinter as tk


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
            if (i == 3 or i == 9 or i == 15) and self.basic_attributes.board_size is 19:
                self.board.create_oval(self.basic_attributes.board_coordinates[i][3][0] - self.cell_size / 10,
                                       self.basic_attributes.board_coordinates[i][3][1] - self.cell_size / 10,
                                       self.basic_attributes.board_coordinates[i][3][0] + self.cell_size / 10,
                                       self.basic_attributes.board_coordinates[i][3][1] + self.cell_size / 10,
                                       fill="black")
                self.board.create_oval(self.basic_attributes.board_coordinates[i][9][0] - self.cell_size / 10,
                                       self.basic_attributes.board_coordinates[i][9][1] - self.cell_size / 10,
                                       self.basic_attributes.board_coordinates[i][9][0] + self.cell_size / 10,
                                       self.basic_attributes.board_coordinates[i][9][1] + self.cell_size / 10,
                                       fill="black")
                self.board.create_oval(self.basic_attributes.board_coordinates[i][15][0] - self.cell_size / 10,
                                       self.basic_attributes.board_coordinates[i][15][1] - self.cell_size / 10,
                                       self.basic_attributes.board_coordinates[i][15][0] + self.cell_size / 10,
                                       self.basic_attributes.board_coordinates[i][15][1] + self.cell_size / 10,
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

        # judge whether the click is in the board
        if i < 0 or i >= self.board_size or j < 0 or j >= self.board_size:
            print("invalid click: outside the board")
            return

        # tell core to handle the coordinate
        self.core.handle_click_board(i, j)

    def draw_stone(self, i, j, current_player):
        color = "black" if current_player == 1 else "white"
        self.board.create_oval(self.basic_attributes.board_coordinates[i][j][0] - self.cell_size / 3,
                               self.basic_attributes.board_coordinates[i][j][1] - self.cell_size / 3,
                               self.basic_attributes.board_coordinates[i][j][0] + self.cell_size / 3,
                               self.basic_attributes.board_coordinates[i][j][1] + self.cell_size / 3,
                               fill=color, tags=f"{i},{j}")

    def remove_stone(self, i, j):
        self.board.delete(f"{i},{j}")
