import random

class GameState:
    def __init__(self):
        self.board = [
            ['bu', 'bu', 'bu', 'bu', 'bk', 'bu', 'bu', 'bu', 'bu'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', 'bu', '.', '.', '.', '.', '.', 'bu', '.'],
            ['bu', '.', 'bu', '.', 'bu', '.', 'bu', '.', 'bu'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['ru', '.', 'ru', '.', 'ru', '.', 'ru', '.', 'ru'],
            ['.', 'ru', '.', '.', '.', '.', '.', 'ru', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['ru', 'ru', 'ru', 'ru', 'rk', 'ru', 'ru', 'ru', 'ru']
        ]
        self.pos_board = [
            ['br', 'bn', 'bb', 'ba', '.', 'ba', 'bb', 'bn', 'br'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', 'bc', '.', '.', '.', '.', '.', 'bc', '.'],
            ['bp', '.', 'bp', '.', 'bp', '.', 'bp', '.', 'bp'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['rp', '.', 'rp', '.', 'rp', '.', 'rp', '.', 'rp'],
            ['.', 'rc', '.', '.', '.', '.', '.', 'rc', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['rr', 'rn', 'rb', 'ra', '.', 'ra', 'rb', 'rn', 'rr']
        ]
        self.red_pieces = ['rp', 'rr', 'rp', 'rc', 'rp', 'rn', 'rp', 'rb', 'rp', 'ra', 'rr', 'rc', 'rn', 'rb', 'ra']
        self.black_pieces = ['bp', 'br', 'bp', 'bc', 'bp', 'bn', 'bp', 'bb', 'bp', 'ba', 'br', 'bc', 'bn', 'bb', 'ba']
        self.move_functions = {'p': self.get_pawn_moves, 'c': self.get_cannon_moves, 'r': self.get_chariot_moves, 'n': self.get_horse_moves,
                               'b': self.get_elephant_moves, 'a': self.get_advisor_moves, 'k': self.get_king_moves, 'u': self.get_undefined_piece_moves}
        self.red_to_move = True
        self.move_log = []
        self.red_king_location = (9, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.check = False
        # self.pos = None
        # self.pos_list = [(None)]
        # self.pos_counter_r = 0
        # self.pos_counter_b = 0
        self.valid_move = None
        random.shuffle(self.red_pieces)
        random.shuffle(self.black_pieces)

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '.'
        if move.piece_moved[1] == 'u':
            self.board[move.end_row][move.end_col] = self.red_pieces[-1] if self.red_to_move else self.black_pieces[-1]
        else:
            self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.red_to_move = not self.red_to_move
        if move.piece_moved == 'rk':
            self.red_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bk':
            self.black_king_location = (move.end_row, move.end_col)

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            # if self.pos_list and self.pos not in self.pos_list[:-1]:
            #     self.pos_list.pop()
            # else:
            #     self.pos_list = [(None)]
            # if self.pos_counter_r and self.pos in self.pos_list and self.red_to_move:
            #     self.pos_counter_r -= 1
            # if self.pos_counter_b and self.pos in self.pos_list and not self.red_to_move:
            #     self.pos_counter_b -= 1
            # self.pos = None
            self.red_to_move = not self.red_to_move
            if move.piece_moved == 'rk':
                self.red_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bk':
                self.black_king_location = (move.start_row, move.start_col)

    def is_repetition(self, count):
        counter_r = 0
        counter_r1 = 0
        counter_b = 0
        counter_b1 = 0
        if len(self.move_log) < 5:
            return False
        if len(self.move_log) >= 5:
            for i in range(0, len(self.move_log) - 4, 4):
                if self.move_log[i].move_id == self.move_log[i+4].move_id:
                    counter_r += 1
                else:
                    counter_r = 0
        if len(self.move_log) >= 7:
            for i in range(2, len(self.move_log) - 4, 4):
                if self.move_log[i].move_id == self.move_log[i+4].move_id:
                    counter_r1 += 1
                else:
                    counter_r1 = 0
        if len(self.move_log) >= 6:
            for i in range(1, len(self.move_log) - 4, 4):
                if self.move_log[i].move_id == self.move_log[i+4].move_id:
                    counter_b += 1
                else:
                    counter_b = 0
        if len(self.move_log) >= 8:
            for i in range(3, len(self.move_log) - 4, 4):
                if self.move_log[i].move_id == self.move_log[i+4].move_id:
                    counter_b1 += 1
                else:
                    counter_b1 = 0
        if self.red_to_move:
            return counter_r == count or counter_r1 == count
        else:
            return counter_b == count or counter_b1 == count

    def get_valid_moves(self):
        moves = self.get_all_possible_moves()
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.red_to_move = not self.red_to_move
            if self.in_check():
                moves.remove(moves[i])
            if self.is_repetition(3):
                moves.remove(moves[i])
            self.red_to_move = not self.red_to_move
            self.undo_move()
        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        # if self.check and not self.checkmate:
        #     print('Check!')
        # if self.checkmate:
        #     print('Checkmate!')
        # if self.stalemate:
        #     print('Stalemate!')
        return moves

    def in_check(self):
        if self.red_to_move:
            return self.point_under_attack(self.red_king_location[0], self.red_king_location[1])
        else:
            return self.point_under_attack(self.black_king_location[0], self.black_king_location[1])

    def point_under_attack(self, r, c):
        pieces = []
        self.red_to_move = not self.red_to_move
        opp_moves = self.get_all_possible_moves()
        self.red_to_move = not self.red_to_move
        for move in opp_moves:
            if self.red_king_location[1] == self.black_king_location[1]:
                for i in range(self.black_king_location[0] + 1, self.red_king_location[0]):
                    if self.board[i][self.red_king_location[1]] != '.':
                        pieces.append(self.board[i][self.red_king_location[1]])
                if len(pieces) == 0:
                    return True
            if move.end_row == r and move.end_col == c:
                self.check = True
                return True
        self.check = False
        return False

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'r' and self.red_to_move) or (turn == 'b' and not self.red_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.red_to_move:
            if (r <= 9) and (r > 4):
                moves.append(Move((r, c), (r - 1, c), self.board))
            if (r <= 4) and (r > 0):
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r <= 4:
                    if c - 1 >= 0:
                        moves.append(Move((r, c), (r, c - 1), self.board))
                    if c + 1 <= 8:
                        moves.append(Move((r, c), (r, c + 1), self.board))
            if r == 0:
                if c - 1 >= 0:
                    moves.append(Move((r, c), (r, c - 1), self.board))
                if c + 1 <= 8:
                    moves.append(Move((r, c), (r, c + 1), self.board))
        if not self.red_to_move:
            if (r >= 0) and (r < 5):
                moves.append(Move((r, c), (r + 1, c), self.board))
            if (r >= 5) and (r < 9):
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r >= 5:
                    if c - 1 >= 0:
                        moves.append(Move((r, c), (r, c - 1), self.board))
                    if c + 1 <= 8:
                        moves.append(Move((r, c), (r, c + 1), self.board))
            if r == 9:
                if c - 1 >= 0:
                    moves.append(Move((r, c), (r, c - 1), self.board))
                if c + 1 <= 8:
                    moves.append(Move((r, c), (r, c + 1), self.board))

    def get_cannon_moves(self, r, c, moves):
        enemy_color = 'b' if self.red_to_move else 'r'
        # black cannon
        if not self.red_to_move:
            m = r
            while (m - 1 >= 0):
                if self.board[m - 1][c] == '.':
                    moves.append(Move((r, c), (m - 1, c), self.board))
                else:
                    k = m - 2
                    while (k > 0 and self.board[k][c] == '.'):
                        k = k - 1
                    if k >= 0 and self.board[k][c][0] == enemy_color:
                        moves.append(Move((r, c), (k, c), self.board))
                    break
                m = m - 1
            m = c
            while (m - 1 >= 0):
                if self.board[r][m - 1] == '.':
                    moves.append(Move((r, c), (r, m - 1), self.board))
                else:
                    k = m - 2
                    while (k > 0 and self.board[r][k] == '.'):
                        k = k - 1
                    if k >= 0 and self.board[r][k][0] == enemy_color:
                        moves.append(Move((r, c), (r, k), self.board))
                    break
                m = m - 1
            m = c
            while (m + 1 <= 8):
                if self.board[r][m + 1] == '.':
                    moves.append(Move((r, c), (r, m + 1), self.board))
                else:
                    k = m + 2
                    while (k < 8 and self.board[r][k] == '.'):
                        k = k + 1
                    if k <= 8 and self.board[r][k][0] == enemy_color:
                        moves.append(Move((r, c), (r, k), self.board))
                    break
                m = m + 1
            m = r
            while (m + 1 <= 9):
                if self.board[m + 1][c] == '.':
                    moves.append(Move((r, c), (m + 1, c), self.board))
                else:
                    k = m + 2
                    while (k < 9 and self.board[k][c] == '.'):
                        k = k + 1
                    if k <= 9 and self.board[k][c][0] == enemy_color:
                        moves.append(Move((r, c), (k, c), self.board))
                    break
                m = m + 1
        # red cannon
        else:
            m = r
            while (m - 1 >= 0):
                if self.board[m - 1][c] == '.':
                    moves.append(Move((r, c), (m - 1, c), self.board))
                else:
                    k = m - 2
                    while (k > 0 and self.board[k][c] == '.'):
                        k = k - 1
                    if k >= 0 and self.board[k][c][0] == enemy_color:
                        moves.append(Move((r, c), (k, c), self.board))
                    break
                m = m - 1
            m = c
            while (m - 1 >= 0):
                if self.board[r][m - 1] == '.':
                    moves.append(Move((r, c), (r, m - 1), self.board))
                else:
                    k = m - 2
                    while (k > 0 and self.board[r][k] == '.'):
                        k = k - 1
                    if k >= 0 and self.board[r][k][0] == enemy_color:
                        moves.append(Move((r, c), (r, k), self.board))
                    break
                m = m - 1
            m = c
            while (m + 1 <= 8):
                if self.board[r][m + 1] == '.':
                    moves.append(Move((r, c), (r, m + 1), self.board))
                else:
                    k = m + 2
                    while (k < 8 and self.board[r][k] == '.'):
                        k = k + 1
                    if k <= 8 and self.board[r][k][0] == enemy_color:
                        moves.append(Move((r, c), (r, k), self.board))
                    break
                m = m + 1
            m = r
            while (m + 1 <= 9):
                if self.board[m + 1][c] == '.':
                    moves.append(Move((r, c), (m + 1, c), self.board))
                else:
                    k = m + 2
                    while (k < 9 and self.board[k][c] == '.'):
                        k = k + 1
                    if k <= 9 and self.board[k][c][0] == enemy_color:
                        moves.append(Move((r, c), (k, c), self.board))
                    break
                m = m + 1

    def get_chariot_moves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.red_to_move else 'r'
        for d in directions:
            for i in range(1, 10):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 10 and 0 <= end_col < 9:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_horse_moves(self, r, c, moves):
        ally_color = 'r' if self.red_to_move else 'b'
        if not self.red_to_move:
            if r - 1 > 0 and self.board[r - 1][c] == '.':
                if c - 1 >= 0 and self.board[r - 2][c - 1][0] != ally_color:
                    moves.append(Move((r, c), (r - 2, c - 1), self.board))
                if c + 1 <= 8 and self.board[r - 2][c + 1][0] != ally_color:
                    moves.append(Move((r, c), (r - 2, c + 1), self.board))
            if c - 1 > 0 and self.board[r][c - 1] == '.':
                if r - 1 >= 0 and self.board[r - 1][c - 2][0] != ally_color:
                    moves.append(Move((r, c), (r - 1, c - 2), self.board))
                if r + 1 <= 9 and self.board[r + 1][c - 2][0] != ally_color:
                    moves.append(Move((r, c), (r + 1, c - 2), self.board))
            if c + 1 < 8 and self.board[r][c + 1] == '.':
                if r - 1 >= 0 and self.board[r - 1][c + 2][0] != ally_color:
                    moves.append(Move((r, c), (r - 1, c + 2), self.board))
                if r + 1 <= 9 and self.board[r + 1][c + 2][0] != ally_color:
                    moves.append(Move((r, c), (r + 1, c + 2), self.board))
            if r + 1 < 9 and self.board[r + 1][c] == '.':
                if c - 1 >= 0 and self.board[r + 2][c - 1][0] != ally_color:
                    moves.append(Move((r, c), (r + 2, c - 1), self.board))
                if c + 1 <= 8 and self.board[r + 2][c + 1][0] != ally_color:
                    moves.append(Move((r, c), (r + 2, c + 1), self.board))
        else:
            if r - 1 > 0 and self.board[r - 1][c] == '.':
                if c - 1 >= 0 and self.board[r - 2][c - 1][0] != ally_color:
                    moves.append(Move((r, c), (r - 2, c - 1), self.board))
                if c + 1 <= 8 and self.board[r - 2][c + 1][0] != ally_color:
                    moves.append(Move((r, c), (r - 2, c + 1), self.board))
            if c - 1 > 0 and self.board[r][c - 1] == '.':
                if r - 1 >= 0 and self.board[r - 1][c - 2][0] != ally_color:
                    moves.append(Move((r, c), (r - 1, c - 2), self.board))
                if r + 1 <= 9 and self.board[r + 1][c - 2][0] != ally_color:
                    moves.append(Move((r, c), (r + 1, c - 2), self.board))
            if c + 1 < 8 and self.board[r][c + 1] == '.':
                if r - 1 >= 0 and self.board[r - 1][c + 2][0] != ally_color:
                    moves.append(Move((r, c), (r - 1, c + 2), self.board))
                if r + 1 <= 9 and self.board[r + 1][c + 2][0] != ally_color:
                    moves.append(Move((r, c), (r + 1, c + 2), self.board))
            if r + 1 < 9 and self.board[r + 1][c] == '.':
                if c - 1 >= 0 and self.board[r + 2][c - 1][0] != ally_color:
                    moves.append(Move((r, c), (r + 2, c - 1), self.board))
                if c + 1 <= 8 and self.board[r + 2][c + 1][0] != ally_color:
                    moves.append(Move((r, c), (r + 2, c + 1), self.board))

    def get_elephant_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.red_to_move else 'r'
        for d in directions:
            end_row = r + d[0] * 2
            end_col = c + d[1] * 2
            if self.red_to_move:
                if 0 <= end_row <= 9 and 0 <= end_col <= 8:
                    end_piece = self.board[end_row][end_col]
                    cross_point = self.board[r + d[0]][c + d[1]]
                    if end_piece == '.' and cross_point == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color and cross_point == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
            else:
                if 0 <= end_row <= 9 and 0 <= end_col <= 8:
                    end_piece = self.board[end_row][end_col]
                    cross_point = self.board[r + d[0]][c + d[1]]
                    if end_piece == '.' and cross_point == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color and cross_point == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break

    def get_advisor_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        ally_color = 'r' if self.red_to_move else 'b'
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if self.red_to_move:
                if self.board[r][c] == 'ru':
                    if 7 <= end_row <= 9 and 3 <= end_col <= 5:
                        end_piece = self.board[end_row][end_col]
                        if end_piece[0] != ally_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                if self.board[r][c] == 'ra':
                    if 0 <= end_row <= 9 and 0 <= end_col <= 8:
                        end_piece = self.board[end_row][end_col]
                        if end_piece[0] != ally_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
            else:
                if self.board[r][c] == 'bu':
                    if 0 <= end_row <= 2 and 3 <= end_col <= 5:
                        end_piece = self.board[end_row][end_col]
                        if end_piece[0] != ally_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                if self.board[r][c] == 'ba':
                    if 0 <= end_row <= 9 and 0 <= end_col <= 8:
                        end_piece = self.board[end_row][end_col]
                        if end_piece[0] != ally_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_king_moves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        ally_color = 'r' if self.red_to_move else 'b'
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if self.red_to_move:
                if 7 <= end_row <= 9 and 3 <= end_col <= 5:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
            else:
                if 0 <= end_row <= 2 and 3 <= end_col <= 5:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_undefined_piece_moves(self, r, c, moves):
        if len(self.pos_board[r][c]) == 2:
            self.move_functions[self.pos_board[r][c][1]](r, c, moves)


class Move:
    ranks_to_rows = {'0': 9, '1': 8, '2': 7, '3': 6, '4': 5, '5': 4, '6': 3, '7': 2, '8': 1, '9': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {'9': 0, '8': 1, '7': 2, '6': 3, '5': 4, '4': 5, '3': 6, '2': 7, '1': 8}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_pos, end_pos, board):
        self.start_row = start_pos[0]
        self.start_col = start_pos[1]
        self.end_row = end_pos[0]
        self.end_col = end_pos[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)


    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
