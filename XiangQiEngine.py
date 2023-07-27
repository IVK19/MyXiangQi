import copy


class GameState:
    def __init__(self):
        self.board = [
            ['br', 'bn', 'bb', 'ba', 'bk', 'ba', 'bb', 'bn', 'br'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', 'bc', '.', '.', '.', '.', '.', 'bc', '.'],
            ['bp', '.', 'bp', '.', 'bp', '.', 'bp', '.', 'bp'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['rp', '.', 'rp', '.', 'rp', '.', 'rp', '.', 'rp'],
            ['.', 'rc', '.', '.', '.', '.', '.', 'rc', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['rr', 'rn', 'rb', 'ra', 'rk', 'ra', 'rb', 'rn', 'rr']
        ]
        self.move_functions = {'p': self.get_pawn_moves, 'c': self.get_cannon_moves, 'r': self.get_chariot_moves, 'n': self.get_horse_moves,
                               'b': self.get_elephant_moves, 'a': self.get_advisor_moves, 'k': self.get_king_moves}
        self.mirror_move_functions = {'p': self.get_mirror_pawn_moves, 'c': self.get_mirror_cannon_moves, 'r': self.get_mirror_chariot_moves,
                               'n': self.get_mirror_horse_moves, 'b': self.get_mirror_elephant_moves, 'a': self.get_mirror_advisor_moves,
                               'k': self.get_mirror_king_moves}
        self.red_to_move = True
        self.move_log = []
        self.mirror_move_log = []
        self.red_king_location = (9, 4)
        self.black_king_location = (0, 4)
        self.mirror_red_king_location = (0, 4)
        self.mirror_black_king_location = (9, 4)
        self.checkmate = False
        self.stalemate = False
        self.check = False
        self.mirror_board = copy.deepcopy(self.board)
        for row in self.mirror_board:
            row.reverse()
        self.mirror_board.reverse()
        self.game_history = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '.'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.red_to_move = not self.red_to_move
        if move.piece_moved == 'rk':
            self.red_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bk':
            self.black_king_location = (move.end_row, move.end_col)

    def make_mirror_move(self, move):
        self.mirror_board[move.start_row][move.start_col] = '.'
        self.mirror_board[move.end_row][move.end_col] = move.piece_moved
        self.mirror_move_log.append(move)
        self.red_to_move = not self.red_to_move
        if move.piece_moved == 'rk':
            self.mirror_red_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bk':
            self.mirror_black_king_location = (move.end_row, move.end_col)

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.red_to_move = not self.red_to_move
            if move.piece_moved == 'rk':
                self.red_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bk':
                self.black_king_location = (move.start_row, move.start_col)

    def undo_mirror_move(self):
        if len(self.mirror_move_log) != 0:
            move = self.mirror_move_log.pop()
            self.mirror_board[move.start_row][move.start_col] = move.piece_moved
            self.mirror_board[move.end_row][move.end_col] = move.piece_captured
            self.red_to_move = not self.red_to_move
            if move.piece_moved == 'rk':
                self.mirror_red_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bk':
                self.mirror_black_king_location = (move.start_row, move.start_col)

    def make_notation_move(self, notation):
        points = []
        columns = []
        counter = 0
        pos = []
        if notation[0] == 'P':
            if notation[1] in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                start_col = Move.files_to_cols[notation[1]]
                for i in range(10):
                    if self.board[i][start_col] == 'rp':
                        start_row = i
                        if notation[2] == '+':
                            end_row = start_row - 1
                            end_col = start_col
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '=':
                            end_row = start_row
                            end_col = Move.files_to_cols[notation[3]]
                            return Move((start_row, start_col), (end_row, end_col), self.board)
            if notation[1] in ('-', '+'):
                for c in range(9):
                    for r in range(10):
                        points.append(self.board[r][c])
                for i in range(10, len(points)+1, 10):
                    columns.append(points[counter:i])
                    counter += 10
                for c in range(len(columns)):
                    for r in range(len(columns[c])):
                        if columns[c][r] == 'rp':
                            pos.append((r, c))
                    if len(pos) == 2:
                        break
                    else:
                        pos = []
                if notation[1] == '-':
                    start_row = pos[1][0]
                    start_col = pos[1][1]
                    if notation[2] == '+':
                        end_row = start_row - 1
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = Move.files_to_cols[notation[3]]
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                if notation[1] == '+':
                    start_row = pos[0][0]
                    start_col = pos[0][1]
                    if notation[2] == '+':
                        end_row = start_row - 1
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = Move.files_to_cols[notation[3]]
                        return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'p':
            if notation[1] in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                start_col = abs(8 - Move.files_to_cols[notation[1]])
                for i in range(10):
                    if self.board[i][start_col] == 'bp':
                        start_row = i
                        if notation[2] == '+':
                            end_row = start_row + 1
                            end_col = start_col
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '=':
                            end_row = start_row
                            end_col = abs(8 - Move.files_to_cols[notation[3]])
                            return Move((start_row, start_col), (end_row, end_col), self.board)
            if notation[1] in ('-', '+'):
                for c in range(9):
                    for r in range(10):
                        points.append(self.board[r][c])
                for i in range(10, len(points)+1, 10):
                    columns.append(points[counter:i])
                    counter += 10
                for c in range(len(columns)):
                    for r in range(len(columns[c])):
                        if columns[c][r] == 'bp':
                            pos.append((r, c))
                    if len(pos) == 2:
                        break
                    else:
                        pos = []
                if notation[1] == '-':
                    start_row = pos[0][0]
                    start_col = pos[0][1]
                    if notation[2] == '+':
                        end_row = start_row + 1
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = abs(8 - Move.files_to_cols[notation[3]])
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                if notation[1] == '+':
                    start_row = pos[1][0]
                    start_col = pos[1][1]
                    if notation[2] == '+':
                        end_row = start_row + 1
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = abs(8 - Move.files_to_cols[notation[3]])
                        return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[:2] in ('1P', '2P', '3P', '4P', '5P'):
            for c in range(9):
                for r in range(10):
                    points.append(self.board[r][c])
            for i in range(10, len(points) + 1, 10):
                columns.append(points[counter:i])
                counter += 10
            for c in range(len(columns)):
                for r in range(len(columns[c])):
                    if columns[c][r] == 'rp':
                        pos.append((r, c))
                    if r == 9 and len(pos) < 3:
                        pos = []
                    if r == 9 and len(pos) >= 3:
                        break
            start_row = pos[int(notation[0])-1][0]
            start_col = pos[int(notation[0])-1][1]
            if notation[2] == '+':
                end_row = start_row - 1
                end_col = start_col
                return Move((start_row, start_col), (end_row, end_col), self.board)
            if notation[2] == '=':
                end_row = start_row
                end_col = Move.files_to_cols[notation[3]]
                return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[:2] in ('1p', '2p', '3p', '4p', '5p'):
            for c in range(9):
                for r in range(10):
                    points.append(self.board[r][c])
            for i in range(10, len(points) + 1, 10):
                columns.append(points[counter:i])
                counter += 10
            for c in range(len(columns)):
                for r in range(len(columns[c])):
                    if columns[c][r] == 'bp':
                        pos.append((r, c))
                    if r == 0 and len(pos) < 3:
                        pos = []
                    if r == 0 and len(pos) >= 3:
                        break
            pos.reverse()
            start_row = pos[int(notation[0])-1][0]
            start_col = pos[int(notation[0])-1][1]
            if notation[2] == '+':
                end_row = start_row + 1
                end_col = start_col
                return Move((start_row, start_col), (end_row, end_col), self.board)
            if notation[2] == '=':
                end_row = start_row
                end_col = abs(8 - Move.files_to_cols[notation[3]])
                return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'C':
            if notation[1] in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                start_col = Move.files_to_cols[notation[1]]
                for i in range(10):
                    if self.board[i][start_col] == 'rc':
                        start_row = i
                        if notation[2] == '+':
                            end_row = start_row - int(notation[3])
                            end_col = start_col
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '-':
                            end_row = start_row + int(notation[3])
                            end_col = start_col
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '=':
                            end_row = start_row
                            end_col = Move.files_to_cols[notation[3]]
                            return Move((start_row, start_col), (end_row, end_col), self.board)
            if notation[1] in ('-', '+'):
                for c in range(9):
                    for r in range(10):
                        points.append(self.board[r][c])
                for i in range(10, len(points)+1, 10):
                    columns.append(points[counter:i])
                    counter += 10
                for c in range(len(columns)):
                    for r in range(len(columns[c])):
                        if columns[c][r] == 'rc':
                            pos.append((r, c))
                    if len(pos) == 2:
                        break
                    else:
                        pos = []
                if notation[1] == '-':
                    start_row = pos[1][0]
                    start_col = pos[1][1]
                    if notation[2] == '+':
                        end_row = start_row - int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_row = start_row + int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = Move.files_to_cols[notation[3]]
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                if notation[1] == '+':
                    start_row = pos[0][0]
                    start_col = pos[0][1]
                    if notation[2] == '+':
                        end_row = start_row - int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_row = start_row + int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = Move.files_to_cols[notation[3]]
                        return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'c':
            if notation[1] in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                start_col = abs(8 - Move.files_to_cols[notation[1]])
                for i in range(10):
                    if self.board[i][start_col] == 'bc':
                        start_row = i
                        if notation[2] == '+':
                            end_row = start_row + int(notation[3])
                            end_col = start_col
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '-':
                            end_row = start_row - int(notation[3])
                            end_col = start_col
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '=':
                            end_row = start_row
                            end_col = abs(8 - Move.files_to_cols[notation[3]])
                            return Move((start_row, start_col), (end_row, end_col), self.board)
            if notation[1] in ('-', '+'):
                for c in range(9):
                    for r in range(10):
                        points.append(self.board[r][c])
                for i in range(10, len(points)+1, 10):
                    columns.append(points[counter:i])
                    counter += 10
                for c in range(len(columns)):
                    for r in range(len(columns[c])):
                        if columns[c][r] == 'bc':
                            pos.append((r, c))
                    if len(pos) == 2:
                        break
                    else:
                        pos = []
                if notation[1] == '-':
                    start_row = pos[0][0]
                    start_col = pos[0][1]
                    if notation[2] == '+':
                        end_row = start_row + int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_row = start_row - int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = abs(8 - Move.files_to_cols[notation[3]])
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                if notation[1] == '+':
                    start_row = pos[1][0]
                    start_col = pos[1][1]
                    if notation[2] == '+':
                        end_row = start_row + int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_row = start_row - int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = abs(8 - Move.files_to_cols[notation[3]])
                        return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'R':
            if notation[1] in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                start_col = Move.files_to_cols[notation[1]]
                for i in range(10):
                    if self.board[i][start_col] == 'rr':
                        start_row = i
                        if notation[2] == '+':
                            end_row = start_row - int(notation[3])
                            end_col = start_col
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '-':
                            end_row = start_row + int(notation[3])
                            end_col = start_col
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '=':
                            end_row = start_row
                            end_col = Move.files_to_cols[notation[3]]
                            return Move((start_row, start_col), (end_row, end_col), self.board)
            if notation[1] in ('-', '+'):
                for c in range(9):
                    for r in range(10):
                        points.append(self.board[r][c])
                for i in range(10, len(points)+1, 10):
                    columns.append(points[counter:i])
                    counter += 10
                for c in range(len(columns)):
                    for r in range(len(columns[c])):
                        if columns[c][r] == 'rr':
                            pos.append((r, c))
                    if len(pos) == 2:
                        break
                    else:
                        pos = []
                if notation[1] == '-':
                    start_row = pos[1][0]
                    start_col = pos[1][1]
                    if notation[2] == '+':
                        end_row = start_row - int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_row = start_row + int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = Move.files_to_cols[notation[3]]
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                if notation[1] == '+':
                    start_row = pos[0][0]
                    start_col = pos[0][1]
                    if notation[2] == '+':
                        end_row = start_row - int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_row = start_row + int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = Move.files_to_cols[notation[3]]
                        return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'r':
            if notation[1] in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                start_col = abs(8 - Move.files_to_cols[notation[1]])
                for i in range(10):
                    if self.board[i][start_col] == 'br':
                        start_row = i
                        if notation[2] == '+':
                            end_row = start_row + int(notation[3])
                            end_col = start_col
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '-':
                            end_row = start_row - int(notation[3])
                            end_col = start_col
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '=':
                            end_row = start_row
                            end_col = abs(8 - Move.files_to_cols[notation[3]])
                            return Move((start_row, start_col), (end_row, end_col), self.board)
            if notation[1] in ('-', '+'):
                for c in range(9):
                    for r in range(10):
                        points.append(self.board[r][c])
                for i in range(10, len(points)+1, 10):
                    columns.append(points[counter:i])
                    counter += 10
                for c in range(len(columns)):
                    for r in range(len(columns[c])):
                        if columns[c][r] == 'br':
                            pos.append((r, c))
                    if len(pos) == 2:
                        break
                    else:
                        pos = []
                if notation[1] == '-':
                    start_row = pos[0][0]
                    start_col = pos[0][1]
                    if notation[2] == '+':
                        end_row = start_row + int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_row = start_row - int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = abs(8 - Move.files_to_cols[notation[3]])
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                if notation[1] == '+':
                    start_row = pos[1][0]
                    start_col = pos[1][1]
                    if notation[2] == '+':
                        end_row = start_row + int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_row = start_row - int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = abs(8 - Move.files_to_cols[notation[3]])
                        return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'H':
            if notation[1] in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                start_col = Move.files_to_cols[notation[1]]
                for i in range(10):
                    if self.board[i][start_col] == 'rn':
                        start_row = i
                        if notation[2] == '+':
                            end_col = Move.files_to_cols[notation[3]]
                            if abs(end_col - start_col) == 1:
                                end_row = start_row - 2
                                return Move((start_row, start_col), (end_row, end_col), self.board)
                            if abs(end_col - start_col) == 2:
                                end_row = start_row - 1
                                return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '-':
                            end_col = Move.files_to_cols[notation[3]]
                            if abs(end_col - start_col) == 1:
                                end_row = start_row + 2
                                return Move((start_row, start_col), (end_row, end_col), self.board)
                            if abs(end_col - start_col) == 2:
                                end_row = start_row + 1
                                return Move((start_row, start_col), (end_row, end_col), self.board)
            if notation[1] in ('-', '+'):
                for c in range(9):
                    for r in range(10):
                        points.append(self.board[r][c])
                for i in range(10, len(points)+1, 10):
                    columns.append(points[counter:i])
                    counter += 10
                for c in range(len(columns)):
                    for r in range(len(columns[c])):
                        if columns[c][r] == 'rn':
                            pos.append((r, c))
                    if len(pos) == 2:
                        break
                    else:
                        pos = []
                if notation[1] == '-':
                    start_row = pos[1][0]
                    start_col = pos[1][1]
                    if notation[2] == '+':
                        end_col = Move.files_to_cols[notation[3]]
                        if abs(end_col - start_col) == 1:
                            end_row = start_row - 2
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if abs(end_col - start_col) == 2:
                            end_row = start_row - 1
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_col = Move.files_to_cols[notation[3]]
                        if abs(end_col - start_col) == 1:
                            end_row = start_row + 2
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if abs(end_col - start_col) == 2:
                            end_row = start_row + 1
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                if notation[1] == '+':
                    start_row = pos[0][0]
                    start_col = pos[0][1]
                    if notation[2] == '+':
                        end_col = Move.files_to_cols[notation[3]]
                        if abs(end_col - start_col) == 1:
                            end_row = start_row - 2
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if abs(end_col - start_col) == 2:
                            end_row = start_row - 1
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_col = Move.files_to_cols[notation[3]]
                        if abs(end_col - start_col) == 1:
                            end_row = start_row + 2
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if abs(end_col - start_col) == 2:
                            end_row = start_row + 1
                            return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'h':
            if notation[1] in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                start_col = abs(8 - Move.files_to_cols[notation[1]])
                for i in range(10):
                    if self.board[i][start_col] == 'bn':
                        start_row = i
                        if notation[2] == '+':
                            end_col = abs(8 - Move.files_to_cols[notation[3]])
                            if abs(end_col - start_col) == 1:
                                end_row = start_row + 2
                                return Move((start_row, start_col), (end_row, end_col), self.board)
                            if abs(end_col - start_col) == 2:
                                end_row = start_row + 1
                                return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '-':
                            end_col = abs(8 - Move.files_to_cols[notation[3]])
                            if abs(end_col - start_col) == 1:
                                end_row = start_row - 2
                                return Move((start_row, start_col), (end_row, end_col), self.board)
                            if abs(end_col - start_col) == 2:
                                end_row = start_row - 1
                                return Move((start_row, start_col), (end_row, end_col), self.board)
            if notation[1] in ('-', '+'):
                for c in range(9):
                    for r in range(10):
                        points.append(self.board[r][c])
                for i in range(10, len(points)+1, 10):
                    columns.append(points[counter:i])
                    counter += 10
                for c in range(len(columns)):
                    for r in range(len(columns[c])):
                        if columns[c][r] == 'bn':
                            pos.append((r, c))
                    if len(pos) == 2:
                        break
                    else:
                        pos = []
                if notation[1] == '-':
                    start_row = pos[0][0]
                    start_col = pos[0][1]
                    if notation[2] == '+':
                        end_col = abs(8 - Move.files_to_cols[notation[3]])
                        if abs(end_col - start_col) == 1:
                            end_row = start_row + 2
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if abs(end_col - start_col) == 2:
                            end_row = start_row + 1
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_col = abs(8 - Move.files_to_cols[notation[3]])
                        if abs(end_col - start_col) == 1:
                            end_row = start_row - 2
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if abs(end_col - start_col) == 2:
                            end_row = start_row - 1
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                if notation[1] == '+':
                    start_row = pos[1][0]
                    start_col = pos[1][1]
                    if notation[2] == '+':
                        end_col = abs(8 - Move.files_to_cols[notation[3]])
                        if abs(end_col - start_col) == 1:
                            end_row = start_row + 2
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if abs(end_col - start_col) == 2:
                            end_row = start_row + 1
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_col = abs(8 - Move.files_to_cols[notation[3]])
                        if abs(end_col - start_col) == 1:
                            end_row = start_row - 2
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if abs(end_col - start_col) == 2:
                            end_row = start_row - 1
                            return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'E':
            for c in range(9):
                for r in range(10):
                    points.append(self.board[r][c])
            for i in range(10, len(points) + 1, 10):
                columns.append(points[counter:i])
                counter += 10
            for c in range(len(columns)):
                for r in range(len(columns[c])):
                    if columns[c][r] == 'rb':
                        pos.append((r, c))
                if len(pos) == 2:
                    break
                else:
                    pos = []
            if len(pos) == 2:
                if notation[2] == '+':
                    start_row = pos[1][0]
                    start_col = pos[1][1]
                    end_row = start_row - 2
                    end_col = Move.files_to_cols[notation[3]]
                    return Move((start_row, start_col), (end_row, end_col), self.board)
                if notation[2] == '-':
                    start_row = pos[0][0]
                    start_col = pos[0][1]
                    end_row = start_row + 2
                    end_col = Move.files_to_cols[notation[3]]
                    return Move((start_row, start_col), (end_row, end_col), self.board)
            else:
                start_col = Move.files_to_cols[notation[1]]
                for i in range(10):
                    if self.board[i][start_col] == 'rb':
                        start_row = i
                        if notation[2] == '+':
                            end_row = start_row - 2
                            end_col = Move.files_to_cols[notation[3]]
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '-':
                            end_row = start_row + 2
                            end_col = Move.files_to_cols[notation[3]]
                            return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'e':
            for c in range(9):
                for r in range(10):
                    points.append(self.board[r][c])
            for i in range(10, len(points) + 1, 10):
                columns.append(points[counter:i])
                counter += 10
            for c in range(len(columns)):
                for r in range(len(columns[c])):
                    if columns[c][r] == 'bb':
                        pos.append((r, c))
                if len(pos) == 2:
                    break
                else:
                    pos = []
            if len(pos) == 2:
                if notation[2] == '+':
                    start_row = pos[0][0]
                    start_col = pos[0][1]
                    end_row = start_row + 2
                    end_col = abs(8 - Move.files_to_cols[notation[3]])
                    return Move((start_row, start_col), (end_row, end_col), self.board)
                if notation[2] == '-':
                    start_row = pos[1][0]
                    start_col = pos[1][1]
                    end_row = start_row - 2
                    end_col = abs(8 - Move.files_to_cols[notation[3]])
                    return Move((start_row, start_col), (end_row, end_col), self.board)
            else:
                start_col = abs(8 - Move.files_to_cols[notation[1]])
                for i in range(10):
                    if self.board[i][start_col] == 'bb':
                        start_row = i
                        if notation[2] == '+':
                            end_row = start_row + 2
                            end_col = abs(8 - Move.files_to_cols[notation[3]])
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '-':
                            end_row = start_row - 2
                            end_col = abs(8 - Move.files_to_cols[notation[3]])
                            return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'A':
            for c in range(9):
                for r in range(10):
                    points.append(self.board[r][c])
            for i in range(10, len(points) + 1, 10):
                columns.append(points[counter:i])
                counter += 10
            for c in range(len(columns)):
                for r in range(len(columns[c])):
                    if columns[c][r] == 'ra':
                        pos.append((r, c))
                if len(pos) == 2:
                    break
                else:
                    pos = []
            if len(pos) == 2:
                if notation[2] == '+':
                    start_row = pos[1][0]
                    start_col = pos[1][1]
                    end_row = start_row - 1
                    end_col = Move.files_to_cols[notation[3]]
                    return Move((start_row, start_col), (end_row, end_col), self.board)
                if notation[2] == '-':
                    start_row = pos[0][0]
                    start_col = pos[0][1]
                    end_row = start_row + 1
                    end_col = Move.files_to_cols[notation[3]]
                    return Move((start_row, start_col), (end_row, end_col), self.board)
            else:
                start_col = Move.files_to_cols[notation[1]]
                for i in range(10):
                    if self.board[i][start_col] == 'ra':
                        start_row = i
                        if notation[2] == '+':
                            end_row = start_row - 1
                            end_col = Move.files_to_cols[notation[3]]
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '-':
                            end_row = start_row + 1
                            end_col = Move.files_to_cols[notation[3]]
                            return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'a':
            for c in range(9):
                for r in range(10):
                    points.append(self.board[r][c])
            for i in range(10, len(points) + 1, 10):
                columns.append(points[counter:i])
                counter += 10
            for c in range(len(columns)):
                for r in range(len(columns[c])):
                    if columns[c][r] == 'ba':
                        pos.append((r, c))
                if len(pos) == 2:
                    break
                else:
                    pos = []
            if len(pos) == 2:
                if notation[2] == '+':
                    start_row = pos[0][0]
                    start_col = pos[0][1]
                    end_row = start_row + 1
                    end_col = abs(8 - Move.files_to_cols[notation[3]])
                    return Move((start_row, start_col), (end_row, end_col), self.board)
                if notation[2] == '-':
                    start_row = pos[1][0]
                    start_col = pos[1][1]
                    end_row = start_row - 1
                    end_col = abs(8 - Move.files_to_cols[notation[3]])
                    return Move((start_row, start_col), (end_row, end_col), self.board)
            else:
                start_col = abs(8 - Move.files_to_cols[notation[1]])
                for i in range(10):
                    if self.board[i][start_col] == 'ba':
                        start_row = i
                        if notation[2] == '+':
                            end_row = start_row + 1
                            end_col = abs(8 - Move.files_to_cols[notation[3]])
                            return Move((start_row, start_col), (end_row, end_col), self.board)
                        if notation[2] == '-':
                            end_row = start_row - 1
                            end_col = abs(8 - Move.files_to_cols[notation[3]])
                            return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'K':
            start_col = Move.files_to_cols[notation[1]]
            for i in range(10):
                if self.board[i][start_col] == 'rk':
                    start_row = i
                    if notation[2] == '+':
                        end_row = start_row - int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_row = start_row + int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = Move.files_to_cols[notation[3]]
                        return Move((start_row, start_col), (end_row, end_col), self.board)
        if notation[0] == 'k':
            start_col = abs(8 - Move.files_to_cols[notation[1]])
            for i in range(10):
                if self.board[i][start_col] == 'bk':
                    start_row = i
                    if notation[2] == '+':
                        end_row = start_row + int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '-':
                        end_row = start_row - int(notation[3])
                        end_col = start_col
                        return Move((start_row, start_col), (end_row, end_col), self.board)
                    if notation[2] == '=':
                        end_row = start_row
                        end_col = abs(8 - Move.files_to_cols[notation[3]])
                        return Move((start_row, start_col), (end_row, end_col), self.board)

    def xiangqi_notation(self, move):
        counter = 0
        max_pos = 0
        coords = move.get_chess_notation()
        pawn_pos = {}
        pawn_count = 1
        if move.piece_moved == 'rp':
            for i in range(6, -1, -1):
                if self.board[i][move.start_col] == 'rp':
                    max_pos = i
                    counter += 1
            if counter == 1:
                if coords[0] == coords[2]:
                    return f'P{coords[0]}+1'
                else:
                    return f'P{coords[0]}={coords[2]}'
            if counter == 2:
                if move.start_row > max_pos:
                    if coords[0] == coords[2]:
                        return 'P-+1'
                    else:
                        return f'P-={coords[2]}'
                if move.start_row == max_pos:
                    if coords[0] == coords[2]:
                        return 'P++1'
                    else:
                        return f'P+={coords[2]}'
            if counter >= 3:
                for row in range(7):
                    if self.board[row][move.start_col] == 'rp':
                        pawn_pos[row] = pawn_count
                        pawn_count += 1
                if coords[0] == coords[2]:
                    return f'{pawn_pos[move.start_row]}P+1'
                else:
                    return f'{pawn_pos[move.start_row]}P={coords[2]}'
        if move.piece_moved == 'bp':
            for i in range(3, 10):
                if self.board[i][move.start_col] == 'bp':
                    max_pos = i
                    counter += 1
            if counter == 1:
                if coords[0] == coords[2]:
                    return f'p{abs(10 - int(coords[0]))}+1'
                else:
                    return f'p{abs(10 - int(coords[0]))}={abs(10 - int(coords[2]))}'
            if counter == 2:
                if move.start_row < max_pos:
                    if coords[0] == coords[2]:
                        return 'p-+1'
                    else:
                        return f'p-={abs(10 - int(coords[2]))}'
                if move.start_row == max_pos:
                    if coords[0] == coords[2]:
                        return 'p++1'
                    else:
                        return f'p+={abs(10 - int(coords[2]))}'
            if counter >= 3:
                for row in range(9, 2, -1):
                    if self.board[row][move.start_col] == 'bp':
                        pawn_pos[row] = pawn_count
                        pawn_count += 1
                if coords[0] == coords[2]:
                    return f'{pawn_pos[move.start_row]}p+1'
                else:
                    return f'{pawn_pos[move.start_row]}p={abs(10 - int(coords[2]))}'
        if move.piece_moved == 'rc':
            for i in range(9, -1, -1):
                if self.board[i][move.start_col] == 'rc':
                    max_pos = i
                    counter += 1
            if counter == 1:
                if coords[0] == coords[2]:
                    if coords[1] < coords[3]:
                        return f'C{coords[0]}+{abs(int(coords[3]) - int(coords[1]))}'
                    else:
                        return f'C{coords[0]}-{abs(int(coords[3]) - int(coords[1]))}'
                else:
                    return f'C{coords[0]}={coords[2]}'
            if counter == 2:
                if move.start_row > max_pos:
                    if coords[0] == coords[2]:
                        if coords[1] < coords[3]:
                            return f'C-+{abs(int(coords[3]) - int(coords[1]))}'
                        else:
                            return f'C--{abs(int(coords[3]) - int(coords[1]))}'
                    else:
                        return f'C-={coords[2]}'
                if move.start_row == max_pos:
                    if coords[0] == coords[2]:
                        if coords[1] < coords[3]:
                            return f'C++{abs(int(coords[3]) - int(coords[1]))}'
                        else:
                            return f'C+-{abs(int(coords[3]) - int(coords[1]))}'
                    else:
                        return f'C+={coords[2]}'

        if move.piece_moved == 'bc':
            for i in range(10):
                if self.board[i][move.start_col] == 'bc':
                    max_pos = i
                    counter += 1
            if counter == 1:
                if coords[0] == coords[2]:
                    if coords[1] > coords[3]:
                        return f'c{abs(10 - int(coords[0]))}+{abs(int(coords[3]) - int(coords[1]))}'
                    else:
                        return f'c{abs(10 - int(coords[0]))}-{abs(int(coords[3]) - int(coords[1]))}'
                else:
                    return f'c{abs(10 - int(coords[0]))}={abs(10 - int(coords[2]))}'
            if counter == 2:
                if move.start_row < max_pos:
                    if coords[0] == coords[2]:
                        if coords[1] > coords[3]:
                            return f'c-+{abs(int(coords[3]) - int(coords[1]))}'
                        else:
                            return f'c--{abs(int(coords[3]) - int(coords[1]))}'
                    else:
                        return f'c-={abs(10 - int(coords[2]))}'
                if move.start_row == max_pos:
                    if coords[0] == coords[2]:
                        if coords[1] > coords[3]:
                            return f'c++{abs(int(coords[3]) - int(coords[1]))}'
                        else:
                            return f'c+-{abs(int(coords[3]) - int(coords[1]))}'
                    else:
                        return f'c+={abs(10 - int(coords[2]))}'
        if move.piece_moved == 'rr':
            for i in range(9, -1, -1):
                if self.board[i][move.start_col] == 'rr':
                    max_pos = i
                    counter += 1
            if counter == 1:
                if coords[0] == coords[2]:
                    if coords[1] < coords[3]:
                        return f'R{coords[0]}+{abs(int(coords[3]) - int(coords[1]))}'
                    else:
                        return f'R{coords[0]}-{abs(int(coords[3]) - int(coords[1]))}'
                else:
                    return f'R{coords[0]}={coords[2]}'
            if counter == 2:
                if move.start_row > max_pos:
                    if coords[0] == coords[2]:
                        if coords[1] < coords[3]:
                            return f'R-+{abs(int(coords[3]) - int(coords[1]))}'
                        else:
                            return f'R--{abs(int(coords[3]) - int(coords[1]))}'
                    else:
                        return f'R-={coords[2]}'
                if move.start_row == max_pos:
                    if coords[0] == coords[2]:
                        if coords[1] < coords[3]:
                            return f'R++{abs(int(coords[3]) - int(coords[1]))}'
                        else:
                            return f'R+-{abs(int(coords[3]) - int(coords[1]))}'
                    else:
                        return f'R+={coords[2]}'
        if move.piece_moved == 'br':
            for i in range(10):
                if self.board[i][move.start_col] == 'br':
                    max_pos = i
                    counter += 1
            if counter == 1:
                if coords[0] == coords[2]:
                    if coords[1] > coords[3]:
                        return f'r{abs(10 - int(coords[0]))}+{abs(int(coords[3]) - int(coords[1]))}'
                    else:
                        return f'r{abs(10 - int(coords[0]))}-{abs(int(coords[3]) - int(coords[1]))}'
                else:
                    return f'r{abs(10 - int(coords[0]))}={abs(10 - int(coords[2]))}'
            if counter == 2:
                if move.start_row < max_pos:
                    if coords[0] == coords[2]:
                        if coords[1] > coords[3]:
                            return f'r-+{abs(int(coords[3]) - int(coords[1]))}'
                        else:
                            return f'r--{abs(int(coords[3]) - int(coords[1]))}'
                    else:
                        return f'r-={abs(10 - int(coords[2]))}'
                if move.start_row == max_pos:
                    if coords[0] == coords[2]:
                        if coords[1] > coords[3]:
                            return f'r++{abs(int(coords[3]) - int(coords[1]))}'
                        else:
                            return f'r+-{abs(int(coords[3]) - int(coords[1]))}'
                    else:
                        return f'r+={abs(10 - int(coords[2]))}'
        if move.piece_moved == 'rn':
            for i in range(9, -1, -1):
                if self.board[i][move.start_col] == 'rn':
                    max_pos = i
                    counter += 1
            if counter == 1:
                if coords[1] < coords[3]:
                    return f'H{coords[0]}+{coords[2]}'
                else:
                    return f'H{coords[0]}-{coords[2]}'
            if counter == 2:
                if move.start_row > max_pos:
                    if coords[1] < coords[3]:
                        return f'H-+{coords[2]}'
                    else:
                        return f'H--{coords[2]}'
                if move.start_row == max_pos:
                    if coords[1] < coords[3]:
                        return f'H++{coords[2]}'
                    else:
                        return f'H+-{coords[2]}'
        if move.piece_moved == 'bn':
            for i in range(10):
                if self.board[i][move.start_col] == 'bn':
                    max_pos = i
                    counter += 1
            if counter == 1:
                if coords[1] > coords[3]:
                    return f'h{abs(10 - int(coords[0]))}+{abs(10 - int(coords[2]))}'
                else:
                    return f'h{abs(10 - int(coords[0]))}-{abs(10 - int(coords[2]))}'
            if counter == 2:
                if move.start_row < max_pos:
                    if coords[1] > coords[3]:
                        return f'h-+{abs(10 - int(coords[2]))}'
                    else:
                        return f'h--{abs(10 - int(coords[2]))}'
                if move.start_row == max_pos:
                    if coords[1] > coords[3]:
                        return f'h++{abs(10 - int(coords[2]))}'
                    else:
                        return f'h+-{abs(10 - int(coords[2]))}'
        if move.piece_moved == 'rb':
            if coords[1] < coords[3]:
                return f'E{coords[0]}+{coords[2]}'
            else:
                return f'E{coords[0]}-{coords[2]}'
        if move.piece_moved == 'bb':
            if coords[1] > coords[3]:
                return f'e{abs(10 - int(coords[0]))}+{abs(10 - int(coords[2]))}'
            else:
                return f'e{abs(10 - int(coords[0]))}-{abs(10 - int(coords[2]))}'
        if move.piece_moved == 'ra':
            if coords[1] < coords[3]:
                return f'A{coords[0]}+{coords[2]}'
            else:
                return f'A{coords[0]}-{coords[2]}'
        if move.piece_moved == 'ba':
            if coords[1] > coords[3]:
                return f'a{abs(10 - int(coords[0]))}+{abs(10 - int(coords[2]))}'
            else:
                return f'a{abs(10 - int(coords[0]))}-{abs(10 - int(coords[2]))}'
        if move.piece_moved == 'rk':
            if coords[0] == coords[2]:
                if coords[1] < coords[3]:
                    return f'K{coords[0]}+{abs(int(coords[3]) - int(coords[1]))}'
                else:
                    return f'K{coords[0]}-{abs(int(coords[3]) - int(coords[1]))}'
            else:
                return f'K{coords[0]}={coords[2]}'
        if move.piece_moved == 'bk':
            if coords[0] == coords[2]:
                if coords[1] > coords[3]:
                    return f'k{abs(10 - int(coords[0]))}+{abs(int(coords[3]) - int(coords[1]))}'
                else:
                    return f'k{abs(10 - int(coords[0]))}-{abs(int(coords[3]) - int(coords[1]))}'
            else:
                return f'k{abs(10 - int(coords[0]))}={abs(10 - int(coords[2]))}'

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

    def is_mirror_repetition(self, count):
        counter_r = 0
        counter_r1 = 0
        counter_b = 0
        counter_b1 = 0
        if len(self.mirror_move_log) < 5:
            return False
        if len(self.mirror_move_log) >= 5:
            for i in range(0, len(self.mirror_move_log) - 4, 4):
                if self.mirror_move_log[i].move_id == self.mirror_move_log[i+4].move_id:
                    counter_r += 1
                else:
                    counter_r = 0
        if len(self.mirror_move_log) >= 7:
            for i in range(2, len(self.mirror_move_log) - 4, 4):
                if self.mirror_move_log[i].move_id == self.mirror_move_log[i+4].move_id:
                    counter_r1 += 1
                else:
                    counter_r1 = 0
        if len(self.mirror_move_log) >= 6:
            for i in range(1, len(self.mirror_move_log) - 4, 4):
                if self.mirror_move_log[i].move_id == self.mirror_move_log[i+4].move_id:
                    counter_b += 1
                else:
                    counter_b = 0
        if len(self.mirror_move_log) >= 8:
            for i in range(3, len(self.mirror_move_log) - 4, 4):
                if self.mirror_move_log[i].move_id == self.mirror_move_log[i+4].move_id:
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
        return moves

    def get_mirror_valid_moves(self):
        moves = self.get_all_possible_mirror_moves()
        for i in range(len(moves) - 1, -1, -1):
            self.make_mirror_move(moves[i])
            self.red_to_move = not self.red_to_move
            if self.in_mirror_check():
                moves.remove(moves[i])
            if self.is_mirror_repetition(3):
                moves.remove(moves[i])
            self.red_to_move = not self.red_to_move
            self.undo_mirror_move()
        if len(moves) == 0:
            if self.in_mirror_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        return moves

    def in_check(self):
        if self.red_to_move:
            return self.point_under_attack(self.red_king_location[0], self.red_king_location[1])
        else:
            return self.point_under_attack(self.black_king_location[0], self.black_king_location[1])

    def in_mirror_check(self):
        if self.red_to_move:
            return self.mirror_point_under_attack(self.mirror_red_king_location[0], self.mirror_red_king_location[1])
        else:
            return self.mirror_point_under_attack(self.mirror_black_king_location[0], self.mirror_black_king_location[1])

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

    def mirror_point_under_attack(self, r, c):
        pieces = []
        self.red_to_move = not self.red_to_move
        opp_moves = self.get_all_possible_mirror_moves()
        self.red_to_move = not self.red_to_move
        for move in opp_moves:
            if self.mirror_red_king_location[1] == self.mirror_black_king_location[1]:
                for i in range(self.mirror_red_king_location[0] + 1, self.mirror_black_king_location[0]):
                    if self.mirror_board[i][self.mirror_red_king_location[1]] != '.':
                        pieces.append(self.mirror_board[i][self.mirror_black_king_location[1]])
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

    def get_all_possible_mirror_moves(self):
        moves = []
        for r in range(len(self.mirror_board)):
            for c in range(len(self.mirror_board[r])):
                turn = self.mirror_board[r][c][0]
                if (turn == 'r' and self.red_to_move) or (turn == 'b' and not self.red_to_move):
                    piece = self.mirror_board[r][c][1]
                    self.mirror_move_functions[piece](r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.red_to_move:
            if (r <= 6) and (r > 4):
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
            if (r >= 3) and (r < 5):
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

    def get_mirror_pawn_moves(self, r, c, moves):
        if self.red_to_move:
            if (r >= 3) and (r < 5):
                moves.append(Move((r, c), (r + 1, c), self.mirror_board))
            if (r >= 5) and (r < 9):
                moves.append(Move((r, c), (r + 1, c), self.mirror_board))
                if r >= 5:
                    if c - 1 >= 0:
                        moves.append(Move((r, c), (r, c - 1), self.mirror_board))
                    if c + 1 <= 8:
                        moves.append(Move((r, c), (r, c + 1), self.mirror_board))
            if r == 9:
                if c - 1 >= 0:
                    moves.append(Move((r, c), (r, c - 1), self.mirror_board))
                if c + 1 <= 8:
                    moves.append(Move((r, c), (r, c + 1), self.mirror_board))
        else:
            if (r <= 6) and (r > 4):
                moves.append(Move((r, c), (r - 1, c), self.mirror_board))
            if (r <= 4) and (r > 0):
                moves.append(Move((r, c), (r - 1, c), self.mirror_board))
                if r <= 4:
                    if c - 1 >= 0:
                        moves.append(Move((r, c), (r, c - 1), self.mirror_board))
                    if c + 1 <= 8:
                        moves.append(Move((r, c), (r, c + 1), self.mirror_board))
            if r == 0:
                if c - 1 >= 0:
                    moves.append(Move((r, c), (r, c - 1), self.mirror_board))
                if c + 1 <= 8:
                    moves.append(Move((r, c), (r, c + 1), self.mirror_board))

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

    def get_mirror_cannon_moves(self, r, c, moves):
        enemy_color = 'b' if self.red_to_move else 'r'
        if not self.red_to_move:
            m = r
            while (m - 1 >= 0):
                if self.mirror_board[m - 1][c] == '.':
                    moves.append(Move((r, c), (m - 1, c), self.mirror_board))
                else:
                    k = m - 2
                    while (k > 0 and self.mirror_board[k][c] == '.'):
                        k = k - 1
                    if k >= 0 and self.mirror_board[k][c][0] == enemy_color:
                        moves.append(Move((r, c), (k, c), self.mirror_board))
                    break
                m = m - 1
            m = c
            while (m - 1 >= 0):
                if self.mirror_board[r][m - 1] == '.':
                    moves.append(Move((r, c), (r, m - 1), self.mirror_board))
                else:
                    k = m - 2
                    while (k > 0 and self.mirror_board[r][k] == '.'):
                        k = k - 1
                    if k >= 0 and self.mirror_board[r][k][0] == enemy_color:
                        moves.append(Move((r, c), (r, k), self.mirror_board))
                    break
                m = m - 1
            m = c
            while (m + 1 <= 8):
                if self.mirror_board[r][m + 1] == '.':
                    moves.append(Move((r, c), (r, m + 1), self.mirror_board))
                else:
                    k = m + 2
                    while (k < 8 and self.mirror_board[r][k] == '.'):
                        k = k + 1
                    if k <= 8 and self.mirror_board[r][k][0] == enemy_color:
                        moves.append(Move((r, c), (r, k), self.mirror_board))
                    break
                m = m + 1
            m = r
            while (m + 1 <= 9):
                if self.mirror_board[m + 1][c] == '.':
                    moves.append(Move((r, c), (m + 1, c), self.mirror_board))
                else:
                    k = m + 2
                    while (k < 9 and self.mirror_board[k][c] == '.'):
                        k = k + 1
                    if k <= 9 and self.mirror_board[k][c][0] == enemy_color:
                        moves.append(Move((r, c), (k, c), self.mirror_board))
                    break
                m = m + 1
        else:
            m = r
            while (m - 1 >= 0):
                if self.mirror_board[m - 1][c] == '.':
                    moves.append(Move((r, c), (m - 1, c), self.mirror_board))
                else:
                    k = m - 2
                    while (k > 0 and self.mirror_board[k][c] == '.'):
                        k = k - 1
                    if k >= 0 and self.mirror_board[k][c][0] == enemy_color:
                        moves.append(Move((r, c), (k, c), self.mirror_board))
                    break
                m = m - 1
            m = c
            while (m - 1 >= 0):
                if self.mirror_board[r][m - 1] == '.':
                    moves.append(Move((r, c), (r, m - 1), self.mirror_board))
                else:
                    k = m - 2
                    while (k > 0 and self.mirror_board[r][k] == '.'):
                        k = k - 1
                    if k >= 0 and self.mirror_board[r][k][0] == enemy_color:
                        moves.append(Move((r, c), (r, k), self.mirror_board))
                    break
                m = m - 1
            m = c
            while (m + 1 <= 8):
                if self.mirror_board[r][m + 1] == '.':
                    moves.append(Move((r, c), (r, m + 1), self.mirror_board))
                else:
                    k = m + 2
                    while (k < 8 and self.mirror_board[r][k] == '.'):
                        k = k + 1
                    if k <= 8 and self.mirror_board[r][k][0] == enemy_color:
                        moves.append(Move((r, c), (r, k), self.mirror_board))
                    break
                m = m + 1
            m = r
            while (m + 1 <= 9):
                if self.mirror_board[m + 1][c] == '.':
                    moves.append(Move((r, c), (m + 1, c), self.mirror_board))
                else:
                    k = m + 2
                    while (k < 9 and self.mirror_board[k][c] == '.'):
                        k = k + 1
                    if k <= 9 and self.mirror_board[k][c][0] == enemy_color:
                        moves.append(Move((r, c), (k, c), self.mirror_board))
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

    def get_mirror_chariot_moves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.red_to_move else 'r'
        for d in directions:
            for i in range(1, 10):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 10 and 0 <= end_col < 9:
                    end_piece = self.mirror_board[end_row][end_col]
                    if end_piece == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.mirror_board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.mirror_board))
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

    def get_mirror_horse_moves(self, r, c, moves):
        ally_color = 'r' if self.red_to_move else 'b'
        if not self.red_to_move:
            if r - 1 > 0 and self.mirror_board[r - 1][c] == '.':
                if c - 1 >= 0 and self.mirror_board[r - 2][c - 1][0] != ally_color:
                    moves.append(Move((r, c), (r - 2, c - 1), self.mirror_board))
                if c + 1 <= 8 and self.mirror_board[r - 2][c + 1][0] != ally_color:
                    moves.append(Move((r, c), (r - 2, c + 1), self.mirror_board))
            if c - 1 > 0 and self.mirror_board[r][c - 1] == '.':
                if r - 1 >= 0 and self.mirror_board[r - 1][c - 2][0] != ally_color:
                    moves.append(Move((r, c), (r - 1, c - 2), self.mirror_board))
                if r + 1 <= 9 and self.mirror_board[r + 1][c - 2][0] != ally_color:
                    moves.append(Move((r, c), (r + 1, c - 2), self.mirror_board))
            if c + 1 < 8 and self.mirror_board[r][c + 1] == '.':
                if r - 1 >= 0 and self.mirror_board[r - 1][c + 2][0] != ally_color:
                    moves.append(Move((r, c), (r - 1, c + 2), self.mirror_board))
                if r + 1 <= 9 and self.mirror_board[r + 1][c + 2][0] != ally_color:
                    moves.append(Move((r, c), (r + 1, c + 2), self.mirror_board))
            if r + 1 < 9 and self.mirror_board[r + 1][c] == '.':
                if c - 1 >= 0 and self.mirror_board[r + 2][c - 1][0] != ally_color:
                    moves.append(Move((r, c), (r + 2, c - 1), self.mirror_board))
                if c + 1 <= 8 and self.mirror_board[r + 2][c + 1][0] != ally_color:
                    moves.append(Move((r, c), (r + 2, c + 1), self.mirror_board))
        else:
            if r - 1 > 0 and self.mirror_board[r - 1][c] == '.':
                if c - 1 >= 0 and self.mirror_board[r - 2][c - 1][0] != ally_color:
                    moves.append(Move((r, c), (r - 2, c - 1), self.mirror_board))
                if c + 1 <= 8 and self.mirror_board[r - 2][c + 1][0] != ally_color:
                    moves.append(Move((r, c), (r - 2, c + 1), self.mirror_board))
            if c - 1 > 0 and self.mirror_board[r][c - 1] == '.':
                if r - 1 >= 0 and self.mirror_board[r - 1][c - 2][0] != ally_color:
                    moves.append(Move((r, c), (r - 1, c - 2), self.mirror_board))
                if r + 1 <= 9 and self.mirror_board[r + 1][c - 2][0] != ally_color:
                    moves.append(Move((r, c), (r + 1, c - 2), self.mirror_board))
            if c + 1 < 8 and self.mirror_board[r][c + 1] == '.':
                if r - 1 >= 0 and self.mirror_board[r - 1][c + 2][0] != ally_color:
                    moves.append(Move((r, c), (r - 1, c + 2), self.mirror_board))
                if r + 1 <= 9 and self.mirror_board[r + 1][c + 2][0] != ally_color:
                    moves.append(Move((r, c), (r + 1, c + 2), self.mirror_board))
            if r + 1 < 9 and self.mirror_board[r + 1][c] == '.':
                if c - 1 >= 0 and self.mirror_board[r + 2][c - 1][0] != ally_color:
                    moves.append(Move((r, c), (r + 2, c - 1), self.mirror_board))
                if c + 1 <= 8 and self.mirror_board[r + 2][c + 1][0] != ally_color:
                    moves.append(Move((r, c), (r + 2, c + 1), self.mirror_board))

    def get_elephant_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.red_to_move else 'r'
        for d in directions:
            end_row = r + d[0] * 2
            end_col = c + d[1] * 2
            if self.red_to_move:
                if 5 <= end_row <= 9 and 0 <= end_col <= 8:
                    end_piece = self.board[end_row][end_col]
                    cross_point = self.board[r + d[0]][c + d[1]]
                    if end_piece == '.' and cross_point == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color and cross_point == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
            else:
                if 0 <= end_row <= 4 and 0 <= end_col <= 8:
                    end_piece = self.board[end_row][end_col]
                    cross_point = self.board[r + d[0]][c + d[1]]
                    if end_piece == '.' and cross_point == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color and cross_point == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break

    def get_mirror_elephant_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.red_to_move else 'r'
        for d in directions:
            end_row = r + d[0] * 2
            end_col = c + d[1] * 2
            if self.red_to_move:
                if 0 <= end_row <= 4 and 0 <= end_col <= 8:
                    end_piece = self.mirror_board[end_row][end_col]
                    cross_point = self.mirror_board[r + d[0]][c + d[1]]
                    if end_piece == '.' and cross_point == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.mirror_board))
                    elif end_piece[0] == enemy_color and cross_point == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.mirror_board))
            else:
                if 5 <= end_row <= 9 and 0 <= end_col <= 8:
                    end_piece = self.mirror_board[end_row][end_col]
                    cross_point = self.mirror_board[r + d[0]][c + d[1]]
                    if end_piece == '.' and cross_point == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.mirror_board))
                    elif end_piece[0] == enemy_color and cross_point == '.':
                        moves.append(Move((r, c), (end_row, end_col), self.mirror_board))

    def get_advisor_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
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

    def get_mirror_advisor_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        ally_color = 'r' if self.red_to_move else 'b'
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if self.red_to_move:
                if 0 <= end_row <= 2 and 3 <= end_col <= 5:
                    end_piece = self.mirror_board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.mirror_board))
            else:
                if 7 <= end_row <= 9 and 3 <= end_col <= 5:
                    end_piece = self.mirror_board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.mirror_board))

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

    def get_mirror_king_moves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        ally_color = 'r' if self.red_to_move else 'b'
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if self.red_to_move:
                if 0 <= end_row <= 2 and 3 <= end_col <= 5:
                    end_piece = self.mirror_board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.mirror_board))
            else:
                if 7 <= end_row <= 9 and 3 <= end_col <= 5:
                    end_piece = self.mirror_board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.mirror_board))


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
        self.move_coords = (self.start_row, self.start_col, self.end_row, self.end_col)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)


    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
