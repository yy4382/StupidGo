import pickle


class GoCore:
    def __init__(self, parent):
        self.parent = parent
        self.basic_attributes = self.parent.basic_attributes
        self.board = self.basic_attributes.board_status
        self.history = self.basic_attributes.board_status_history
        self.current_player = 1

    def place_stone(self, i, j):
        # judge if there is already a stone
        if self.board[i][j] != 0:
            return

        # 更新棋盘，然后吃子，如果判断完之后新棋子是死子，则回滚更新
        self.board[i][j] = self.current_player
        removed_stones = self._get_removing_stones(3 - self.current_player)
        for removed_stone in removed_stones:
            self.board[removed_stone[0]][removed_stone[1]] = 0
        (invalid, _) = self._check_kill(i, j)
        if invalid:
            self.board[i][j] = 0
            print(f"Warning for player {self.current_player}: invalid placing in ({i}, {j}) for killing itself")
            return

        self.current_player = 3 - self.current_player

        # 判断是否和之前的棋盘一致，如果一致则回滚更新，不一致则将此情况储存
        board_status_pickle = pickle.dumps(self.board)
        for hi in self.history:
            if hi == board_status_pickle:
                self.board[i][j] = 0
                for removed_stone in removed_stones:
                    self.board[removed_stone[0]][removed_stone[1]] = self.current_player
                self.current_player = 3 - self.current_player
                print(f"Warning for player {self.current_player}: invalid placing in ({i}, {j}) for the same status")
                return
        self.history.append(pickle.dumps(self.board))

        # 此时可以确定此处可以落子，更新gui并打印信息
        self.parent.board.draw_stone(i, j, 3 - self.current_player)
        for removed_stone in removed_stones:
            self.parent.board.remove_stone(removed_stone[0], removed_stone[1])
        print(f"player {3 - self.current_player}: placed a stone in ({i}, {j})")
        if removed_stones:
            print(f"player {self.current_player}'s stone(s) are killed: {removed_stones}")

    def _get_side_stone(self, i, j, stones):
        target_player = self.board[stones[0][0]][stones[0][1]]
        if i > 0 and self.board[i - 1][j] == target_player and (not (i - 1, j) in stones):
            stones.append((i - 1, j))
            self._get_side_stone(i - 1, j, stones)
        if i < self.basic_attributes.board_size - 1 and self.board[i + 1][j] == target_player and (
                not (i + 1, j) in stones):
            stones.append((i + 1, j))
            self._get_side_stone(i + 1, j, stones)
        if j > 0 and self.board[i][j - 1] == target_player and (not (i, j - 1) in stones):
            stones.append((i, j - 1))
            self._get_side_stone(i, j - 1, stones)
        if j < self.basic_attributes.board_size - 1 and self.board[i][j + 1] == target_player and (
                not (i, j + 1) in stones):
            stones.append((i, j + 1))
            self._get_side_stone(i, j + 1, stones)

    def _check_kill(self, i, j):  # 判断 i, j 处的棋子所在整体是否有气，无气返回 False，不依赖 self.current_player
        side_stones = [(i, j)]
        self._get_side_stone(i, j, side_stones)
        for stone in side_stones:
            left = stone[0] > 0 and self.board[stone[0] - 1][stone[1]] == 0
            right = stone[0] < self.basic_attributes.board_size - 1 and self.board[stone[0] + 1][stone[1]] == 0
            up = stone[1] > 0 and self.board[stone[0]][stone[1] - 1] == 0
            down = stone[1] < self.basic_attributes.board_size - 1 and self.board[stone[0]][stone[1] + 1] == 0
            if left or right or up or down:
                return False, side_stones
        return True, side_stones
        # 这一段可以获取这一片棋具体有多少气，不过这里目前只要判断有没有就行，这个说不定之后写ai的时候有用
        # qi_stones = []
        # qi = 0
        # for stone in side_stones:
        #     if stone[0] > 0 and self.board[stone[0] - 1][stone[1]] == 0 and (
        #             not self.board[stone[0] - 1][stone[1]] in qi_stones):
        #         qi_stones.append((stone[0] - 1, stone[1]))
        #         qi += 1
        #     if stone[0] < self.basic_attributes.board_size - 1 and self.board[stone[0] + 1][stone[1]] == 0 and (
        #             not self.board[stone[0] + 1][stone[1]] in qi_stones):
        #         qi_stones.append((stone[0] + 1, stone[1]))
        #         qi += 1
        #     if stone[1] > 0 and self.board[stone[0]][stone[1] - 1] == 0 and (
        #             not self.board[stone[0]][stone[1] - 1] in qi_stones):
        #         qi_stones.append((stone[0], stone[j - 1]))
        #         qi += 1
        #     if stone[1] < self.basic_attributes.board_size - 1 and self.board[stone[0]][stone[1] + 1] == 0 and (
        #             not self.board[stone[0]][stone[1] + 1] in qi_stones):
        #         qi_stones.append((stone[0], stone[j + 1]))
        #         qi += 1

    def _get_removing_stones(self, player):
        checked_stone = []
        total_removed_stones = []
        for i in range(self.basic_attributes.board_size):
            for j in range(self.basic_attributes.board_size):
                if self.board[i][j] == player and (not (i, j) in checked_stone):
                    (bo, st) = self._check_kill(i, j)
                    for item in st:
                        checked_stone.append(item)
                    if bo:
                        for item in st:
                            total_removed_stones.append((item[0], item[1]))
        return total_removed_stones
