import pickle
from collections import deque
import copy


class GoBasicAttributes:
    def __init__(self, window_size, board_size):
        self.window_size = window_size
        self.board_size = board_size
        self.board_coordinates = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.board_status = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.cell_size = window_size / (board_size + 1)
        self.board_status_history = [pickle.dumps(self.board_status)]


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

        # 判断是否自杀（不更改棋盘）
        self.board[i][j] = self.current_player
        (has_qi, _) = self._get_qi(i, j)
        removed_stones = self._get_removing_stones(3 - self.current_player)
        self.board[i][j] = 0
        if not has_qi and not removed_stones:
            self.board[i][j] = 0
            print(f"Warning for player {self.current_player}: invalid placing for killing itself")
            return

        # 判断是否和之前的棋盘一致（不更改棋盘）
        test_board = copy.deepcopy(self.board)
        test_board[i][j] = self.current_player
        for removed_stone in removed_stones:
            test_board[removed_stone[0]][removed_stone[1]] = 0
        board_status_pickle = pickle.dumps(test_board)
        for hi in self.history:
            if hi == board_status_pickle:
                self.board[i][j] = 0
                print(f"Warning for player {self.current_player}: invalid placing for the same status")
                return

        # 此时可以确定此处可以落子，正式修改棋盘,修改gui
        self.board[i][j] = self.current_player
        self.parent.board.draw_stone(i, j, self.current_player)
        for removed_stone in removed_stones:
            self.board[removed_stone[0]][removed_stone[1]] = 0
            self.parent.board.remove_stone(*removed_stone)

        self.history.append(pickle.dumps(self.board))

        print(f"player {self.current_player}: placed a stone in ({i}, {j})")
        if removed_stones:
            print(f"Killing player {3 - self.current_player}'s stone(s): {removed_stones}")

        self.current_player = 3 - self.current_player

    def _get_side_stone(self, i, j):
        # 获得 i, j 处棋子所在的块
        target_player = self.board[i][j]
        stones = deque()
        visited = set()
        stones.append((i, j))
        visited.add((i, j))
        while stones:
            i, j = stones.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x, y = i + dx, j + dy
                if 0 <= x < self.basic_attributes.board_size and 0 <= y < self.basic_attributes.board_size \
                        and self.board[x][y] == target_player and (x, y) not in visited:
                    stones.append((x, y))
                    visited.add((x, y))
        return list(visited)

    def _get_qi(self, i, j):
        # 判断 i, j 处的棋子所在整体是否有气，不依赖 self.current_player
        side_stones = self._get_side_stone(i, j)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # left, right, up, down
        for stone in side_stones:
            for dx, dy in directions:
                x, y = stone[0] + dx, stone[1] + dy
                if self.basic_attributes.board_size > x >= 0 == self.board[x][y] \
                        and 0 <= y < self.basic_attributes.board_size:
                    return True, side_stones
        return False, side_stones
        # 这一段可以获取这一片棋具体有多少气，不过这里目前只要判断有没有就行，这个说不定之后写ai的时候有用
        # qi_stones = []
        # qi = 0
        # directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # left, right, up, down
        # for stone in side_stones:
        #     for dx, dy in directions:
        #         x, y = stone[0] + dx, stone[1] + dy
        #         if self.basic_attributes.board_size > x >= 0 == self.board[x][
        #             y] and 0 <= y < self.basic_attributes.board_size and ((x, y) not in qi_stones):
        #             qi_stones.append((x, y))
        #             qi += 1

    def _get_removing_stones(self, player):
        # 返回场上所有属于player的无气棋子
        checked_stone = []
        removed_stones = []
        for i in range(self.basic_attributes.board_size):
            for j in range(self.basic_attributes.board_size):
                if self.board[i][j] == player and (not (i, j) in checked_stone):
                    (has_qi, st) = self._get_qi(i, j)
                    checked_stone.extend(st)
                    if not has_qi:
                        removed_stones.extend(st)
        return removed_stones

    def end_of_game(self):
        pass
