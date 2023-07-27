import random
import time

piece_score = {'k': 0, 'p': 1, 'a': 1, 'b': 2, 'n': 3, 'c': 4, 'r': 5, 'u': 1}
CHECKMATE = STALEMATE = 1000
DEPTH = 4

red_pawn_scores = [[1, 1, 2, 2, 2, 2, 2, 1, 1],
                   [2, 3, 4, 4, 4, 4, 4, 3, 2],
                   [2, 4, 5, 5, 5, 5, 5, 4, 2],
                   [3, 4, 5, 5, 5, 5, 5, 4, 3],
                   [3, 3, 3, 3, 3, 3, 3, 3, 3],
                   [2, 2, 3, 2, 2, 2, 3, 2, 2],
                   [1, 0, 0, 0, 1, 0, 0, 0, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0]]

black_pawn_scores = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 0, 0, 0, 1, 0, 0, 0, 1],
                     [2, 2, 3, 2, 2, 2, 3, 2, 2],
                     [3, 3, 3, 3, 3, 3, 3, 3, 3],
                     [3, 4, 5, 5, 5, 5, 5, 4, 3],
                     [2, 4, 5, 5, 5, 5, 5, 4, 2],
                     [2, 3, 4, 4, 4, 4, 4, 3, 2],
                     [1, 1, 2, 2, 2, 2, 2, 1, 1]]

red_elephant_scores = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 1, 0, 0, 0, 1, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [1, 0, 0, 0, 2, 0, 0, 0, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 2, 0, 0, 0, 2, 0, 0]]

black_elephant_scores = [[0, 0, 2, 0, 0, 0, 2, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [1, 0, 0, 0, 2, 0, 0, 0, 1],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0]]

red_adviser_scores = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 2, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 1, 0, 0, 0]]

black_adviser_scores = [[0, 0, 0, 1, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 2, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]]

horse_scores = [[1, 1, 2, 2, 1, 2, 2, 1, 1],
                [1, 1, 6, 2, 1, 2, 6, 1, 1],
                [1, 2, 4, 5, 2, 5, 4, 2, 1],
                [1, 1, 4, 5, 5, 5, 4, 1, 1],
                [1, 3, 1, 4, 3, 4, 1, 3, 1],
                [1, 3, 1, 4, 3, 4, 1, 3, 1],
                [1, 1, 4, 5, 5, 5, 4, 1, 1],
                [1, 2, 4, 5, 2, 5, 4, 2, 1],
                [1, 1, 6, 2, 1, 2, 6, 1, 1],
                [1, 1, 2, 2, 1, 2, 2, 1, 1]]

cannon_scores = [[6, 1, 4, 2, 2, 2, 4, 1, 6],
                 [4, 4, 4, 3, 3, 3, 4, 4, 4],
                 [3, 2, 3, 4, 6, 4, 3, 2, 3],
                 [3, 3, 3, 3, 6, 3, 3, 3, 3],
                 [4, 4, 4, 4, 6, 4, 4, 4, 4],
                 [4, 4, 4, 4, 6, 4, 4, 4, 4],
                 [3, 3, 3, 3, 6, 3, 3, 3, 3],
                 [3, 2, 3, 4, 6, 4, 3, 2, 3],
                 [4, 4, 4, 3, 3, 3, 4, 4, 4],
                 [6, 1, 4, 2, 2, 2, 4, 1, 6]]

chariot_scores = [[4, 5, 4, 5, 4, 5, 4, 5, 4],
                 [5, 4, 4, 6, 4, 6, 4, 4, 5],
                 [5, 5, 4, 5, 5, 5, 4, 5, 5],
                 [4, 5, 4, 5, 5, 5, 4, 5, 4],
                 [4, 5, 4, 5, 5, 5, 4, 5, 4],
                 [0, 5, 0, 0, 0, 0, 0, 5, 0],
                 [4, 5, 4, 5, 5, 5, 4, 5, 4],
                 [5, 5, 4, 5, 5, 5, 4, 5, 5],
                 [5, 4, 4, 6, 4, 6, 4, 4, 5],
                 [4, 5, 4, 5, 4, 5, 4, 5, 4]]

undefined_piece_scores = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0]]

piece_position_scores = {'rp': red_pawn_scores, 'bp': black_pawn_scores, 'rb': red_elephant_scores, 'bb': black_elephant_scores,
                         'ra': red_adviser_scores, 'ba': black_adviser_scores, 'n': horse_scores, 'c': cannon_scores, 'r': chariot_scores, 'u': undefined_piece_scores}

def find_random_move(valid_moves):
    time.sleep(1)
    return valid_moves[random.randint(0, len(valid_moves)-1)]

def find_best_move(gs, valid_moves):
    time.sleep(3)
    turn_multiplier = 1 if gs.red_to_move else -1
    opponent_min_max_score = CHECKMATE
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        gs.make_move(player_move)
        opponent_moves = gs.get_valid_moves()
        # opponent_max_score = -CHECKMATE
    if gs.stalemate:
        opponent_max_score = -STALEMATE
    elif gs.checkmate:
        opponent_max_score = -CHECKMATE
    else:
        opponent_max_score = -CHECKMATE
        for opponent_move in opponent_moves:
            gs.make_move(opponent_move)
            gs.get_valid_moves()
            if gs.checkmate:
                score = CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
            else:
                score = -turn_multiplier * score_material(gs.board)
            if score > opponent_max_score:
                opponent_max_score = score
            gs.undo_move()
    if opponent_min_max_score < opponent_max_score:
        opponent_min_max_score = opponent_max_score
        best_player_move = player_move
    gs.undo_move()
    return best_player_move

def find_best_move_min_max(gs, valid_moves, return_queue):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    # find_move_min_max(gs, valid_moves, DEPTH, gs.red_to_move)
    find_move_nega_max_alpha_beta(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.red_to_move else -1)
    return_queue.put(next_move)
    # return next_move

def find_move_min_max(gs, valid_moves, depth, red_to_move):
    random.shuffle(valid_moves)
    global next_move
    if depth == 0:
        return score_material(gs.board)
    if red_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return max_score
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score

def find_move_nega_max(gs, valid_moves, depth, turn_multiplier):
    random.shuffle(valid_moves)
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(gs)
    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_nega_max(gs, next_moves, depth - 1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
    return max_score

def find_move_nega_max_alpha_beta(gs, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(gs)
    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(gs, next_moves, depth - 1, -alpha, -beta, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score

def score_board(gs):
    if gs.checkmate:
        if gs.red_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        if gs.red_to_move:
            return -STALEMATE
        else:
            return STALEMATE
    score = 0
    for row in range(10):
        for col in range(9):
            square = gs.board[row][col]
            if square != '.':
                piece_position_score = 0
                if square[1] != 'k':
                    if square[1] == 'p' or square[1] == 'b' or square[1] == 'a':
                        piece_position_score = piece_position_scores[square][row][col]
                    else:
                        piece_position_score = piece_position_scores[square[1]][row][col]
                if gs.board[row][col][0] == 'r':
                    if gs.board[row][col] == 'rp' and row <= 4:
                        score += 2 + piece_position_score * .1
                    else:
                        score += piece_score[gs.board[row][col][1]] + piece_position_score * .1
                elif gs.board[row][col][0] == 'b':
                    if gs.board[row][col] == 'bp' and row >= 5:
                        score -= 2 - piece_position_score * .1
                    else:
                        score -= piece_score[gs.board[row][col][1]] - piece_position_score * .1
    return score

def score_material(board):
    score = 0
    for row in range(10):
        for col in range(9):
            if board[row][col][0] == 'r':
                if board[row][col] == 'rp' and row <= 4:
                    score += 2
                else:
                    score += piece_score[board[row][col][1]]
            elif board[row][col][0] == 'b':
                if board[row][col] == 'bp' and row >= 5:
                    score -= 2
                else:
                    score -= piece_score[board[row][col][1]]
    return score