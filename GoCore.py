import copy
import pickle
from collections import deque
from tkinter import messagebox


class GoBasicAttributes:
    def __init__(self, window_size, board_size):
        self.window_size = window_size
        self.board_size = board_size
        self.board_coordinates = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.board_status = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.cell_size = window_size / (board_size + 1)
        self.board_status_history = [pickle.dumps(self.board_status)]
        self.removing_dead_mode = False

    def c_to_w(self, coordinates):
        if type(coordinates) is tuple:
            return chr(coordinates[0] + ord('a')) + str(self.board_size - coordinates[1])
        elif type(coordinates) is list:
            word = []
            for c in coordinates:
                word.append(chr(c[0] + ord('a')) + str(self.board_size - c[1]))
            return ', '.join(word)
        else:
            return ""


class GoCore:
    def __init__(self, parent):
        self.parent = parent
        self.attributes = self.parent.basic_attributes
        self.board = self.attributes.board_status
        self.history = self.attributes.board_status_history
        self.current_player = 1

    def handle_click_board(self, i, j):
        if self.attributes.removing_dead_mode and self.board[i][j] != 0:
            removing_stones = self._get_side_stone(i, j, True)
            for removed_stone in removing_stones:
                self.board[removed_stone[0]][removed_stone[1]] = 0
                self.parent.board.remove_stone(*removed_stone)
            print(f"死子 {self.attributes.c_to_w(removing_stones)} 已被提去")
        elif self.attributes.removing_dead_mode:
            print("此处无子")
        else:
            self._place_stone(i, j)

    def _place_stone(self, i, j):
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
            print(f"{'黑' if self.current_player == 1 else '白'}棋棋手无效落子：不可自杀")
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
                print(f"{'黑' if self.current_player == 1 else '白'}棋棋手无效落子：不可全局同形")
                return

        # 此时可以确定此处可以落子，正式修改棋盘,修改gui
        self.board[i][j] = self.current_player
        self.parent.board.draw_stone(i, j, self.current_player)
        for removed_stone in removed_stones:
            self.board[removed_stone[0]][removed_stone[1]] = 0
            self.parent.board.remove_stone(*removed_stone)

        self.history.append(pickle.dumps(self.board))

        print()
        print(f"{'黑' if self.current_player == 1 else '白'}棋落在 {self.attributes.c_to_w((i, j))}")
        if removed_stones:
            print(f"{'黑' if 3 - self.current_player == 1 else '白'}棋 {self.attributes.c_to_w(removed_stones)} 被吃")

        self.current_player = 3 - self.current_player
        self.parent.toggle_timer()

    def _get_side_stone(self, i, j, include_blank=False):
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
                if 0 <= x < self.attributes.board_size and 0 <= y < self.attributes.board_size:
                    if include_blank:
                        valid = self.board[x][y] == target_player or self.board[x][y] == 0
                    else:
                        valid = self.board[x][y] == target_player
                    if valid and (x, y) not in visited:
                        stones.append((x, y))
                        visited.add((x, y))
        if not include_blank:
            return list(visited)
        else:
            return [x for x in visited if self.board[x[0]][x[1]] == target_player]

    def _get_qi(self, i, j):
        # 判断 i, j 处的棋子所在整体是否有气，不依赖 self.current_player
        side_stones = self._get_side_stone(i, j)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for stone in side_stones:
            for dx, dy in directions:
                x, y = stone[0] + dx, stone[1] + dy
                if self.attributes.board_size > x >= 0 == self.board[x][y] \
                        and 0 <= y < self.attributes.board_size:
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
        for i in range(self.attributes.board_size):
            for j in range(self.attributes.board_size):
                if self.board[i][j] == player and (not (i, j) in checked_stone):
                    (has_qi, st) = self._get_qi(i, j)
                    checked_stone.extend(st)
                    if not has_qi:
                        removed_stones.extend(st)
        return removed_stones

    def _remove_dead_stones(self):
        for removed_stone in self._get_removing_stones(1) + self._get_removing_stones(2):
            self.board[removed_stone[0]][removed_stone[1]] = 0
            self.parent.board.remove_stone(*removed_stone)
        self.attributes.removing_dead_mode = True
        messagebox.showinfo("提示",
                            "已自动提去一部分死子（不可能再形成两眼的棋子），请手动左击剩余的死子以提去（点一个可以去一整块），完成后点击”提完了“按钮")
        self.parent.end_btn.configure(text='提完了')

    def _get_space_ownership(self, i, j):
        side_space = self._get_side_stone(i, j)
        touch1 = False
        touch2 = False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for space in side_space:
            for dx, dy in directions:
                x, y = space[0] + dx, space[1] + dy
                if self.attributes.board_size > x >= 0 and 0 <= y < self.attributes.board_size:
                    if self.board[x][y] == 1:
                        touch1 = True
                    elif self.board[x][y] == 2:
                        touch2 = True

        result_dict = {(True, False): 1, (False, True): 2, (True, True): 0, (False, False): -1}
        return result_dict[(touch1, touch2)], side_space

    def _judge_win(self):
        checked_stones = []
        zi_of_black = 0
        for i in range(self.attributes.board_size):
            for j in range(self.attributes.board_size):
                if self.board[i][j] == 1:
                    zi_of_black += 1
                if self.board[i][j] == 0 and (i, j) not in checked_stones:
                    ownership, side_space = self._get_space_ownership(i, j)
                    checked_stones.extend(side_space)
                    if ownership == 1:
                        zi_of_black += len(side_space)
                    elif ownership == 0:
                        messagebox.showerror("错误", "单官未走完/死子未提尽, 请继续提死子")
                        self._remove_dead_stones()
                        return
                    elif ownership == -1:
                        messagebox.showerror("错误", "棋盘为空")
                        return
        self.parent.end_of_game()
        black_win = zi_of_black - 184.25
        messagebox.showinfo("结果", f"{'黑' if black_win > 0 else '白'}棋赢{abs(black_win)}子")

    def on_end_btn_clicked(self):
        if self.attributes.removing_dead_mode:
            self.attributes.removing_dead_mode = False
            self._judge_win()


        else:
            self._remove_dead_stones()
