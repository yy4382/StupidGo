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
            self.update_status()
            return True

    def get_side_stone(self, i, j, target_player, stones):
        if i > 0 and self.board[i - 1][j] == target_player and (not (i - 1, j) in stones):
            stones.append((i - 1, j))
            self.get_side_stone(i - 1, j, target_player, stones)
        if i < self.basic_attributes.board_size - 1 and self.board[i + 1][j] == target_player and (
                not (i + 1, j) in stones):
            stones.append((i + 1, j))
            self.get_side_stone(i + 1, j, target_player, stones)
        if j > 0 and self.board[i][j - 1] == target_player and (not (i, j - 1) in stones):
            stones.append((i, j - 1))
            self.get_side_stone(i, j - 1, target_player, stones)
        if j < self.basic_attributes.board_size - 1 and self.board[i][j + 1] == target_player and (
                not (i, j + 1) in stones):
            stones.append((i, j + 1))
            self.get_side_stone(i, j + 1, target_player, stones)

    def check_kill(self, i, j):
        side_stones = [(i, j)]
        self.get_side_stone(i, j, self.current_player, side_stones)
        for stone in side_stones:
            left = stone[0] > 0 and self.board[stone[0] - 1][stone[1]] == 0
            right = stone[0] < self.basic_attributes.board_size - 1 and self.board[stone[0] + 1][stone[1]] == 0
            up = stone[1] > 0 and self.board[stone[0]][stone[1] - 1] == 0
            down = stone[1] < self.basic_attributes.board_size - 1 and self.board[stone[0]][stone[1] + 1] == 0
            if left or right or up or down:
                return False, side_stones
        return True, side_stones
        """这一段可以获取这一片棋具体有多少气，不过这里目前只要判断有没有就行，这个说不定之后写ai的时候有用
        qi_stones = []
        qi = 0
        for stone in side_stones:
            if stone[0] > 0 and self.board[stone[0] - 1][stone[1]] == 0 and (
                    not self.board[stone[0] - 1][stone[1]] in qi_stones):
                qi_stones.append((stone[0] - 1, stone[1]))
                qi += 1
            if stone[0] < self.basic_attributes.board_size - 1 and self.board[stone[0] + 1][stone[1]] == 0 and (
                    not self.board[stone[0] + 1][stone[1]] in qi_stones):
                qi_stones.append((stone[0] + 1, stone[1]))
                qi += 1
            if stone[1] > 0 and self.board[stone[0]][stone[1] - 1] == 0 and (
                    not self.board[stone[0]][stone[1] - 1] in qi_stones):
                qi_stones.append((stone[0], stone[j - 1]))
                qi += 1
            if stone[1] < self.basic_attributes.board_size - 1 and self.board[stone[0]][stone[1] + 1] == 0 and (
                    not self.board[stone[0]][stone[1] + 1] in qi_stones):
                qi_stones.append((stone[0], stone[j + 1]))
                qi += 1
        """

    def update_status(self):
        checked_stone = []
        for i in range(self.basic_attributes.board_size):
            for j in range(self.basic_attributes.board_size):
                if self.board[i][j] == self.current_player and (not (i, j) in checked_stone):
                    (bo, st) = self.check_kill(i, j)
                    for item in st:
                        checked_stone.append(item)
                    if bo:
                        print(f"kill {st}")
                        for item in st:
                            self.parent.board.remove_stone(item[0], item[1])


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

        # judge whether the click is valid
        if i < 0 or i >= self.board_size or j < 0 or j >= self.board_size:
            print("invalid click")
            return
        print(f"player{self.core.current_player}: ({i}, {j})")

        if self.core.place_stone(i, j):
            self.draw_stone(i, j, self.core.current_player)

    def draw_stone(self, i, j, current_player):
        # 由于current_player在传入之前已经更新，所以要反着来
        if current_player == 2:
            self.board.create_oval(self.basic_attributes.board_coordinates[i][j][0] - self.cell_size / 3,
                                   self.basic_attributes.board_coordinates[i][j][1] - self.cell_size / 3,
                                   self.basic_attributes.board_coordinates[i][j][0] + self.cell_size / 3,
                                   self.basic_attributes.board_coordinates[i][j][1] + self.cell_size / 3,
                                   fill="black", tags=f"{i},{j}")
        elif current_player == 1:
            self.board.create_oval(self.basic_attributes.board_coordinates[i][j][0] - self.cell_size / 3,
                                   self.basic_attributes.board_coordinates[i][j][1] - self.cell_size / 3,
                                   self.basic_attributes.board_coordinates[i][j][0] + self.cell_size / 3,
                                   self.basic_attributes.board_coordinates[i][j][1] + self.cell_size / 3,
                                   fill="white", tags=f"{i},{j}")

    def remove_stone(self, i, j):
        self.board.delete(f"{i},{j}")


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
