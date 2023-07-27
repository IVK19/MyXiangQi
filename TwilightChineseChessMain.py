import pygame as p
import TwilightChineseChessEngine
import SmartMoveFinder
from multiprocessing import Process, Queue
import asyncio


WIDTH = 1499.2
HEIGHT = 937
R_DIMENSION = 10
C_DIMENSION = 9
SQ_SIZE = HEIGHT // R_DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_images():
    pieces = ['rp', 'rc', 'rr', 'rn', 'rb', 'ra', 'rk', 'ru', 'bp', 'bc', 'br', 'bn', 'bb', 'ba', 'bk', 'bu']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

async def main():
    game_over = False
    captured_pieces = []
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("XiangQi")
    clock = p.time.Clock()
    screen.fill(p.Color('black'))
    gs = TwilightChineseChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    valid_mirror_moves = gs.get_mirror_valid_moves()
    move_made = False
    load_images()
    running = True
    sq_selected = ()
    player_clicks = []
    move_coords = None
    player_one = True
    player_two = True
    ai_thinking = False
    move_finder_process = None
    move_undone = False
    moves_counter = 1
    reversed_board = False
    if not reversed_board:
        board = gs.board
    else:
        board = gs.mirror_board
    while running:
        human_turn = (gs.red_to_move and player_one) or (not gs.red_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sq_selected == (row, col) or col >= 9:
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)
                    if len(player_clicks) == 2:
                        if reversed_board:
                            move = TwilightChineseChessEngine.Move(player_clicks[0], player_clicks[1], board)
                            if move in valid_mirror_moves:
                                gs.make_mirror_move(move)
                                if move.piece_moved == 'ru':
                                    gs.mirror_red_pieces.pop()
                                    gs.mirror_pos_board[move.start_row][move.start_col] = '.'
                                if move.piece_moved == 'bu':
                                    gs.mirror_black_pieces.pop()
                                    gs.mirror_pos_board[move.start_row][move.start_col] = '.'
                                gs.red_to_move = not gs.red_to_move
                                gs.make_move(TwilightChineseChessEngine.Move((9 - move.start_row, 8 - move.start_col),
                                                                (9 - move.end_row, 8 - move.end_col),
                                                                gs.board))
                                if gs.move_log[-1].piece_moved == 'ru':
                                    gs.red_pieces.pop()
                                    gs.pos_board[gs.move_log[-1].start_row][gs.move_log[-1].start_col] = '.'
                                if gs.move_log[-1].piece_moved == 'bu':
                                    gs.black_pieces.pop()
                                    gs.pos_board[gs.move_log[-1].start_row][gs.move_log[-1].start_col] = '.'
                                move_made = True
                                move_coords = move
                                sq_selected = ()
                                player_clicks = []
                                if move.piece_captured != '.':
                                    captured_pieces.append(move.piece_captured)
                            if not move_made:
                                player_clicks = [sq_selected]
                        else:
                            move = TwilightChineseChessEngine.Move(player_clicks[0], player_clicks[1], board)
                            if move in valid_moves:
                                gs.make_move(move)
                                if move.piece_moved == 'ru':
                                    gs.red_pieces.pop()
                                    gs.pos_board[move.start_row][move.start_col] = '.'
                                if move.piece_moved == 'bu':
                                    gs.black_pieces.pop()
                                    gs.pos_board[move.start_row][move.start_col] = '.'
                                gs.red_to_move = not gs.red_to_move
                                gs.make_mirror_move(
                                    TwilightChineseChessEngine.Move((9 - move.start_row, 8 - move.start_col),
                                                       (9 - move.end_row, 8 - move.end_col),
                                                       gs.mirror_board))
                                if gs.mirror_move_log[-1].piece_moved == 'ru':
                                    gs.mirror_red_pieces.pop()
                                    gs.mirror_pos_board[gs.mirror_move_log[-1].start_row][gs.mirror_move_log[-1].start_col] = '.'
                                if gs.mirror_move_log[-1].piece_moved == 'bu':
                                    gs.mirror_black_pieces.pop()
                                    gs.mirror_pos_board[gs.mirror_move_log[-1].start_row][gs.mirror_move_log[-1].start_col] = '.'
                                move_made = True
                                move_coords = move
                                sq_selected = ()
                                player_clicks = []
                                if move.piece_captured != '.':
                                    captured_pieces.append(move.piece_captured)
                            if not move_made:
                                player_clicks = [sq_selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_s:
                    reversed_board = not reversed_board
                    if reversed_board:
                        board = gs.mirror_board
                        if gs.mirror_move_log:
                            move_coords = gs.mirror_move_log[-1]
                        else:
                            move_coords = None
                    else:
                        board = gs.board
                        if gs.move_log:
                            move_coords = gs.move_log[-1]
                        else:
                            move_coords = None
                    draw_game_state(screen, gs, move_coords, sq_selected, valid_moves, valid_mirror_moves, captured_pieces, reversed_board, game_over)
                    clock.tick(MAX_FPS)
                    p.display.flip()
                if e.key == p.K_r:
                    game_over = False
                    gs = TwilightChineseChessEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    valid_mirror_moves = gs.get_mirror_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    moves_counter = 1
                    captured_pieces = []
                    xiangqi_moves = []
                    move_coords = None
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = False
                    if reversed_board:
                        board = gs.mirror_board
                    else:
                        board = gs.board
        if not game_over and not human_turn and not move_undone:
            if gs.red_to_move and moves_counter == 1:
                if reversed_board:
                    not_mirror_move = SmartMoveFinder.find_random_move(valid_moves)
                    move = TwilightChineseChessEngine.Move((9 - not_mirror_move.start_row, 8 - not_mirror_move.start_col), (9 - not_mirror_move.end_row, 8 - not_mirror_move.end_col), board)
                    if move in valid_mirror_moves:
                        gs.make_mirror_move(move)
                        if move.piece_moved == 'ru':
                            gs.mirror_red_pieces.pop()
                            gs.mirror_pos_board[move.start_row][move.start_col] = '.'
                        if move.piece_moved == 'bu':
                            gs.mirror_black_pieces.pop()
                            gs.mirror_pos_board[move.start_row][move.start_col] = '.'
                        gs.red_to_move = not gs.red_to_move
                        gs.make_move(not_mirror_move)
                        if not_mirror_move.piece_moved == 'ru':
                            gs.red_pieces.pop()
                            gs.pos_board[not_mirror_move.start_row][not_mirror_move.start_col] = '.'
                        if not_mirror_move.piece_moved == 'bu':
                            gs.black_pieces.pop()
                            gs.pos_board[not_mirror_move.start_row][not_mirror_move.start_col] = '.'
                else:
                    move = SmartMoveFinder.find_random_move(valid_moves)
                    if move in valid_moves:
                        gs.make_move(move)
                        if move.piece_moved == 'ru':
                            gs.red_pieces.pop()
                            gs.pos_board[move.start_row][move.start_col] = '.'
                        if move.piece_moved == 'bu':
                            gs.black_pieces.pop()
                            gs.pos_board[move.start_row][move.start_col] = '.'
                        gs.red_to_move = not gs.red_to_move
                        gs.make_mirror_move(
                            TwilightChineseChessEngine.Move((9 - move.start_row, 8 - move.start_col),
                                                     (9 - move.end_row, 8 - move.end_col),
                                                     gs.mirror_board))
                        if gs.mirror_move_log[-1].piece_moved == 'ru':
                            gs.mirror_red_pieces.pop()
                            gs.mirror_pos_board[gs.mirror_move_log[-1].start_row][gs.mirror_move_log[-1].start_col] = '.'
                        if gs.mirror_move_log[-1].piece_moved == 'bu':
                            gs.mirror_black_pieces.pop()
                            gs.mirror_pos_board[gs.mirror_move_log[-1].start_row][gs.mirror_move_log[-1].start_col] = '.'
                move_made = True
                move_coords = move
                if move.piece_captured != '.':
                    captured_pieces.append(move.piece_captured)
            elif not gs.red_to_move and moves_counter == 1:
                if not reversed_board:
                    move = SmartMoveFinder.find_random_move(valid_moves)
                    if move in valid_moves:
                        gs.make_move(move)
                        if move.piece_moved == 'ru':
                            gs.red_pieces.pop()
                            gs.pos_board[move.start_row][move.start_col] = '.'
                        if move.piece_moved == 'bu':
                            gs.black_pieces.pop()
                            gs.pos_board[move.start_row][move.start_col] = '.'
                        gs.red_to_move = not gs.red_to_move
                        gs.make_mirror_move(
                            TwilightChineseChessEngine.Move((9 - move.start_row, 8 - move.start_col),
                                                     (9 - move.end_row, 8 - move.end_col),
                                                     gs.mirror_board))
                        if gs.mirror_move_log[-1].piece_moved == 'ru':
                            gs.mirror_red_pieces.pop()
                            gs.mirror_pos_board[gs.mirror_move_log[-1].start_row][gs.mirror_move_log[-1].start_col] = '.'
                        if gs.mirror_move_log[-1].piece_moved == 'bu':
                            gs.mirror_black_pieces.pop()
                            gs.mirror_pos_board[gs.mirror_move_log[-1].start_row][gs.mirror_move_log[-1].start_col] = '.'
                else:
                    not_mirror_move = SmartMoveFinder.find_random_move(valid_moves)
                    move = TwilightChineseChessEngine.Move((9 - not_mirror_move.start_row, 8 - not_mirror_move.start_col), (9 - not_mirror_move.end_row, 8 - not_mirror_move.end_col), board)
                    if move in valid_mirror_moves:
                        gs.make_mirror_move(move)
                        if move.piece_moved == 'ru':
                            gs.mirror_red_pieces.pop()
                            gs.mirror_pos_board[move.start_row][move.start_col] = '.'
                        if move.piece_moved == 'bu':
                            gs.mirror_black_pieces.pop()
                            gs.mirror_pos_board[move.start_row][move.start_col] = '.'
                        gs.red_to_move = not gs.red_to_move
                        gs.make_move(not_mirror_move)
                        if not_mirror_move.piece_moved == 'ru':
                            gs.red_pieces.pop()
                            gs.pos_board[not_mirror_move.start_row][not_mirror_move.start_col] = '.'
                        if not_mirror_move.piece_moved == 'bu':
                            gs.black_pieces.pop()
                            gs.pos_board[not_mirror_move.start_row][not_mirror_move.start_col] = '.'
                move_made = True
                move_coords = move
                if move.piece_captured != '.':
                    captured_pieces.append(move.piece_captured)
            else:
                if not ai_thinking:
                    ai_thinking = True
                    print('thinking...')
                    return_queue = Queue()
                    move_finder_process = Process(target=SmartMoveFinder.find_best_move_min_max, args=(gs, valid_moves, return_queue))
                    move_finder_process.start()
                if not move_finder_process.is_alive():
                    print('done thinking')
                    if not reversed_board:
                        ai_move = return_queue.get()
                        if ai_move is None:
                            ai_move = SmartMoveFinder.find_random_move(valid_moves)
                        gs.make_move(ai_move)
                        if ai_move.piece_moved == 'ru':
                            gs.red_pieces.pop()
                            gs.pos_board[ai_move.start_row][ai_move.start_col] = '.'
                        if ai_move.piece_moved == 'bu':
                            gs.black_pieces.pop()
                            gs.pos_board[ai_move.start_row][ai_move.start_col] = '.'
                        gs.red_to_move = not gs.red_to_move
                        gs.make_mirror_move(
                            TwilightChineseChessEngine.Move((9 - ai_move.start_row, 8 - ai_move.start_col),
                                                 (9 - ai_move.end_row, 8 - ai_move.end_col),
                                                 gs.mirror_board))
                        if gs.mirror_move_log[-1].piece_moved == 'ru':
                            gs.mirror_red_pieces.pop()
                            gs.mirror_pos_board[gs.mirror_move_log[-1].start_row][gs.mirror_move_log[-1].start_col] = '.'
                        if gs.mirror_move_log[-1].piece_moved == 'bu':
                            gs.mirror_black_pieces.pop()
                            gs.mirror_pos_board[gs.mirror_move_log[-1].start_row][gs.mirror_move_log[-1].start_col] = '.'
                    else:
                        origin_ai_move = return_queue.get()
                        if origin_ai_move is None:
                            origin_ai_move = SmartMoveFinder.find_random_move(valid_moves)
                        ai_move = TwilightChineseChessEngine.Move(
                            (9 - origin_ai_move.start_row, 8 - origin_ai_move.start_col),
                            (9 - origin_ai_move.end_row, 8 - origin_ai_move.end_col), board)
                        gs.make_mirror_move(ai_move)
                        if ai_move.piece_moved == 'ru':
                            gs.mirror_red_pieces.pop()
                            gs.mirror_pos_board[ai_move.start_row][ai_move.start_col] = '.'
                        if ai_move.piece_moved == 'bu':
                            gs.mirror_black_pieces.pop()
                            gs.mirror_pos_board[ai_move.start_row][ai_move.start_col] = '.'
                        gs.red_to_move = not gs.red_to_move
                        gs.make_move(origin_ai_move)
                        if origin_ai_move.piece_moved == 'ru':
                            gs.red_pieces.pop()
                            gs.pos_board[origin_ai_move.start_row][origin_ai_move.start_col] = '.'
                        if origin_ai_move.piece_moved == 'bu':
                            gs.black_pieces.pop()
                            gs.pos_board[origin_ai_move.start_row][origin_ai_move.start_col] = '.'
                    move_made = True
                    move_coords = ai_move
                    ai_thinking = False
                    if ai_move.piece_captured != '.':
                        captured_pieces.append(ai_move.piece_captured)
        if move_made:
            if reversed_board:
                if gs.mirror_move_log:
                    animate_move(gs.mirror_move_log[-1], screen, board, move_coords, clock)
                    if not len(gs.mirror_move_log) % 2:
                        moves_counter += 1
                valid_moves = gs.get_valid_moves()
                valid_mirror_moves = gs.get_mirror_valid_moves()
                move_made = False
                move_undone = False
            else:
                if gs.move_log:
                    animate_move(gs.move_log[-1], screen, board, move_coords, clock)
                    if not len(gs.move_log) % 2:
                        moves_counter += 1
                valid_moves = gs.get_valid_moves()
                valid_mirror_moves = gs.get_mirror_valid_moves()
                move_made = False
                move_undone = False
        draw_game_state(screen, gs, move_coords, sq_selected, valid_moves, valid_mirror_moves, captured_pieces, reversed_board, game_over)
        if not reversed_board:
            if gs.in_check() and not game_over:
                if gs.red_to_move:
                    draw_game_text(screen, 'Шах генералу красных!')
                else:
                    draw_game_text(screen, 'Шах генералу чёрных!')
            if gs.checkmate:
                game_over = True
                if gs.red_to_move:
                    draw_game_text(screen, 'Мат! Победа чёрных!')
                else:
                    draw_game_text(screen, 'Мат! Победа красных!')
            elif gs.stalemate:
                game_over = True
                if gs.red_to_move:
                    draw_game_text(screen, 'Пат! Победа чёрных!')
                else:
                    draw_game_text(screen, 'Пат! Победа красных!')
        else:
            if gs.in_mirror_check() and not game_over:
                if gs.red_to_move:
                    draw_game_text(screen, 'Шах генералу красных!')
                else:
                    draw_game_text(screen, 'Шах генералу чёрных!')
            if gs.checkmate:
                game_over = True
                if gs.red_to_move:
                    draw_game_text(screen, 'Мат! Победа чёрных!')
                else:
                    draw_game_text(screen, 'Мат! Победа красных!')
            elif gs.stalemate:
                game_over = True
                if gs.red_to_move:
                    draw_game_text(screen, 'Пат! Победа чёрных!')
                else:
                    draw_game_text(screen, 'Пат! Победа красных!')
        if game_over:
            draw_other_pieces(screen, gs.red_pieces, gs.black_pieces, board)
        clock.tick(MAX_FPS)
        p.display.flip()
        await asyncio.sleep(0)

def draw_game_state(screen, gs, move_coords, sq_selected, valid_moves, valid_mirror_moves, captured_pieces, reversed_board, game_over):
    draw_board(screen)
    draw_captured_pieces(screen, captured_pieces, game_over, gs.red_pieces, gs.black_pieces)
    if reversed_board:
        draw_pieces(screen, gs.mirror_board, move_coords)
        selected_piece(screen, gs, gs.mirror_board, sq_selected, valid_mirror_moves)
    else:
        draw_pieces(screen, gs.board, move_coords)
        selected_piece(screen, gs, gs.board, sq_selected, valid_moves)

def selected_piece(screen, gs, board, sq_selected, valid_moves):
    if sq_selected != ():
        r, c = sq_selected
        if board[r][c][0] == ('r' if gs.red_to_move else 'b'):
            if board[r][c][0] == 'r':
                p.draw.circle(screen, 'red', (SQ_SIZE // 2 + SQ_SIZE * c, SQ_SIZE // 2 + SQ_SIZE * r), radius=SQ_SIZE // 2, width=3)
            else:
                p.draw.circle(screen, 'blue', (SQ_SIZE // 2 + SQ_SIZE * c, SQ_SIZE // 2 + SQ_SIZE * r), radius=SQ_SIZE // 2, width=3)
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    p.draw.circle(screen, 'green', (SQ_SIZE // 2 + SQ_SIZE * move.end_col, SQ_SIZE // 2 + SQ_SIZE * move.end_row), radius=SQ_SIZE // 2, width=3)

def draw_board(screen):
    screen.fill(p.Color('black'))
    p.draw.line(screen, 'gold', (SQ_SIZE//2, SQ_SIZE//2), (SQ_SIZE//2 + SQ_SIZE*8, SQ_SIZE//2), width=7)
    p.draw.line(screen, 'gold', (SQ_SIZE//2, SQ_SIZE//2), (SQ_SIZE//2, SQ_SIZE//2 + SQ_SIZE*9), width=7)
    p.draw.line(screen, 'gold', (SQ_SIZE//2, SQ_SIZE//2 + SQ_SIZE*9), (SQ_SIZE//2 + SQ_SIZE*8, SQ_SIZE//2 + SQ_SIZE*9), width=7)
    p.draw.line(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE*8, SQ_SIZE//2), (SQ_SIZE//2 + SQ_SIZE*8, SQ_SIZE//2 + SQ_SIZE*9), width=7)
    p.draw.line(screen, 'gold', (SQ_SIZE//2, SQ_SIZE//2 + SQ_SIZE), (SQ_SIZE//2 + SQ_SIZE*8, SQ_SIZE//2 + SQ_SIZE), width=3)
    for i in range(2, 9):
        p.draw.line(screen, 'gold', (SQ_SIZE//2, SQ_SIZE//2 + SQ_SIZE*i), (SQ_SIZE//2 + SQ_SIZE*8, SQ_SIZE//2 + SQ_SIZE*i), width=3)
    for i in range(1, 8):
        p.draw.line(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE*i, SQ_SIZE//2), (SQ_SIZE//2 + SQ_SIZE*i, SQ_SIZE//2 + SQ_SIZE*4), width=3)
    for i in range(1, 8):
        p.draw.line(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE*i, SQ_SIZE//2 + SQ_SIZE*5), (SQ_SIZE//2 + SQ_SIZE*i, SQ_SIZE//2 + SQ_SIZE*9), width=3)
    p.draw.line(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE*3, SQ_SIZE//2), (SQ_SIZE//2 + SQ_SIZE*5, SQ_SIZE//2 + SQ_SIZE*2), width=3)
    p.draw.line(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE*5, SQ_SIZE//2), (SQ_SIZE//2 + SQ_SIZE*3, SQ_SIZE//2 + SQ_SIZE*2), width=3)
    p.draw.line(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE*3, SQ_SIZE//2 + SQ_SIZE*7), (SQ_SIZE//2 + SQ_SIZE*5, SQ_SIZE//2 + SQ_SIZE*9), width=3)
    p.draw.line(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE*5, SQ_SIZE//2 + SQ_SIZE*7), (SQ_SIZE//2 + SQ_SIZE*3, SQ_SIZE//2 + SQ_SIZE*9), width=3)
    for i in range(0, 10, 2):
        p.draw.circle(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE*i, SQ_SIZE//2 + SQ_SIZE*3), radius=6, width=0)
    for i in range(0, 10, 2):
        p.draw.circle(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE*i, SQ_SIZE//2 + SQ_SIZE*6), radius=6, width=0)
    p.draw.circle(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE, SQ_SIZE//2 + SQ_SIZE*2), radius=6, width=0)
    p.draw.circle(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE*7, SQ_SIZE//2 + SQ_SIZE*2), radius=6, width=0)
    p.draw.circle(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE, SQ_SIZE//2 + SQ_SIZE*7), radius=6, width=0)
    p.draw.circle(screen, 'gold', (SQ_SIZE//2 + SQ_SIZE*7, SQ_SIZE//2 + SQ_SIZE*7), radius=6, width=0)

def draw_pieces(screen, board, move_coords):
    for r in range(R_DIMENSION):
        for c in range(C_DIMENSION):
            piece = board[r][c]
            if piece != '.':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if move_coords:
        screen.blit(p.transform.scale(p.image.load('images/mask.png'), (SQ_SIZE, SQ_SIZE)), p.Rect(move_coords.start_col * SQ_SIZE, move_coords.start_row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        screen.blit(p.transform.scale(p.image.load('images/mask.png'), (SQ_SIZE, SQ_SIZE)), p.Rect(move_coords.end_col * SQ_SIZE, move_coords.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_captured_pieces(screen, captured_pieces, game_over, reds, blacks):
    red_captured_pieces = []
    black_captured_pieces = []
    count_c = 0
    count_r = 0
    global i, j
    i = -1
    j = -1
    if captured_pieces:
        for piece in captured_pieces:
            if piece[0] == 'r':
                red_captured_pieces.append(piece)
            else:
                black_captured_pieces.append(piece)
    sum_captured_pieces = red_captured_pieces + black_captured_pieces
    if sum_captured_pieces:
        if game_over:
            for piece in sum_captured_pieces:
                if piece == 'ru':
                    screen.blit(IMAGES[reds[i]], p.Rect((10 + count_c) * SQ_SIZE, count_r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    p.draw.circle(screen, 'red', (SQ_SIZE // 2 + (10 + count_c) * SQ_SIZE, SQ_SIZE // 2 + count_r * SQ_SIZE), radius=SQ_SIZE // 2, width=3)
                    count_c += 1
                    i -= 1
                    if count_c > 2:
                        count_c = 0
                        count_r += 1
                elif piece == 'bu':
                    screen.blit(IMAGES[blacks[j]], p.Rect((10 + count_c) * SQ_SIZE, count_r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    p.draw.circle(screen, 'blue', (SQ_SIZE // 2 + (10 + count_c) * SQ_SIZE, SQ_SIZE // 2 + count_r * SQ_SIZE), radius=SQ_SIZE // 2, width=3)
                    count_c += 1
                    j -= 1
                    if count_c > 2:
                        count_c = 0
                        count_r += 1
                else:
                    screen.blit(IMAGES[piece], p.Rect((10 + count_c) * SQ_SIZE, count_r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    count_c += 1
                    if count_c > 2:
                        count_c = 0
                        count_r += 1
        else:
            for piece in sum_captured_pieces:
                screen.blit(IMAGES[piece], p.Rect((10 + count_c) * SQ_SIZE, count_r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                count_c += 1
                if count_c > 2:
                    count_c = 0
                    count_r += 1

def draw_other_pieces(screen, reds, blacks, board):
    global i, j
    if reds or blacks:
        for r in range(R_DIMENSION):
            for c in range(C_DIMENSION):
                piece = board[r][c]
                if piece == 'ru':
                    figure = reds[i]
                    screen.blit(IMAGES[figure], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    p.draw.circle(screen, 'red', (SQ_SIZE // 2 + SQ_SIZE * c, SQ_SIZE // 2 + SQ_SIZE * r), radius=SQ_SIZE // 2, width=3)
                    i -= 1
                if piece == 'bu':
                    figure = blacks[j]
                    screen.blit(IMAGES[figure], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    p.draw.circle(screen, 'blue', (SQ_SIZE // 2 + SQ_SIZE * c, SQ_SIZE // 2 + SQ_SIZE * r), radius=SQ_SIZE // 2, width=3)
                    j -= 1

def animate_move(move, screen, board, move_coords, clock):
    dr = move.end_row - move.start_row
    dc = move.end_col - move.start_col
    frames_per_point = 10
    frame_count = (abs(dr) + abs(dc)) * frames_per_point
    for frame in range(frame_count + 1):
        r, c = (move.start_row + dr*frame/frame_count, move.start_col + dc*frame/frame_count)
        draw_board(screen)
        draw_pieces(screen, board, move_coords)
        end_point = p.Rect(move.end_col*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, (252, 115, 3), end_point)
        if move.piece_captured != '.':
            screen.blit(IMAGES[move.piece_captured], end_point)
        screen.blit(IMAGES[move.piece_moved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def draw_game_text(screen, text):
    font = p.font.SysFont('arial', 60, True, False)
    text_object = font.render(text, 0, p.Color('Gold'))
    text_location = p.Rect(0, 0, HEIGHT*9/10, HEIGHT).move((HEIGHT/6 - text_object.get_height()/6)*9/10, HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)


if __name__ == '__main__':
    asyncio.run(main())
