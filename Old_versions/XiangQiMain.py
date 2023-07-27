import pygame as p
import XiangQiEngine
import SmartMoveFinder
import time
import random
from multiprocessing import Process, Queue


WIDTH = 800
HEIGHT = 500
R_DIMENSION = 10
C_DIMENSION = 9
SQ_SIZE = HEIGHT // R_DIMENSION
MAX_FPS = 15
IMAGES = {}
RED_START_MOVE = ['C2=1', 'C2=3', 'C2=4', 'C2=5', 'C2=6', 'C2=7', 'C2+1', 'C2+2', 'C2-1', 'C8=9', 'C8=7', 'C8=6', 'C8=5',
                  'C8=4', 'C8=3', 'C8+1', 'C8+2', 'C8-1', 'H2+1', 'H2+3', 'H8+9', 'H8+7', 'P1+1', 'P3+1', 'P7+1', 'P9+1',
                  'E3+5', 'E7+5']
BLACK_START_MOVE = ['c2=1', 'c2=3', 'c2=4', 'c2=5', 'c2=6', 'c2=7', 'c2+1', 'c2+2', 'c2-1', 'c8=9', 'c8=7', 'c8=6', 'c8=5',
                    'c8=4', 'c8=3', 'c8+1', 'c8+2', 'c8-1', 'h2+1', 'h2+3', 'h8+9', 'h8+7', 'p1+1', 'p3+1', 'p7+1', 'p9+1',
                    'e3+5', 'e7+5']


def load_images():
    pieces = ['rp', 'rc', 'rr', 'rn', 'rb', 'ra', 'rk', 'bp', 'bc', 'br', 'bn', 'bb', 'ba', 'bk']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("XiangQi")
    clock = p.time.Clock()
    screen.fill(p.Color('black'))
    game_over = False
    captured_pieces = []
    red_captured_pieces = []
    black_captured_pieces = []
    xiangqi_moves = []
    moves_counter = 1
    notation_counter = 0
    move_log_font = p.font.SysFont('arial', 12, False, False)
    gs = XiangQiEngine.GameState()
    valid_moves = gs.get_valid_moves()
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
                        move = XiangQiEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        xiangqi_move = gs.xiangqi_notation(move)
                        if move in valid_moves:
                            gs.make_move(move)
                            move_made = True
                            move_coords = move
                            sq_selected = ()
                            player_clicks = []
                            xiangqi_moves.append(xiangqi_move)
                            if move.piece_captured != '.':
                                captured_pieces.append(move.piece_captured)
                        if not move_made:
                            player_clicks = [sq_selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_q:
                    if gs.move_log:
                        move = gs.move_log[-1]
                        if move.piece_captured != '.':
                            captured_pieces.pop()
                        gs.undo_move()
                        xiangqi_moves.pop()
                        if moves_counter > 1:
                            moves_counter -= 1
                        move_made = True
                        if len(gs.move_log) != 0:
                            move_coords = gs.move_log[-1]
                        else:
                            move_coords = None
                        if notation_counter:
                            notation_counter -= 1
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                if e.key == p.K_n:
                    # notation = input('Введите нотацию хода: ')
                    # move = gs.make_notation_move(notation)
                    # xiangqi_move = gs.xiangqi_notation(move)
                    notation_list = get_notation()
                    while notation_counter < len(notation_list):
                        time.sleep(3)
                        move = gs.make_notation_move(str(notation_list[notation_counter]))
                        xiangqi_move = gs.xiangqi_notation(move)
                        notation_counter += 1
                        if move in valid_moves:
                            gs.make_move(move)
                            move_made = True
                            move_coords = move
                            xiangqi_moves.append(xiangqi_move)
                            if move.piece_captured != '.':
                                captured_pieces.append(move.piece_captured)
                        if move_made:
                            if gs.move_log:
                                animate_move(gs.move_log[-1], screen, gs.board, move_coords, clock)
                            valid_moves = gs.get_valid_moves()
                            move_made = False
                        draw_game_state(screen, gs, move_coords, sq_selected, valid_moves, move_log_font, xiangqi_moves, captured_pieces)
                        clock.tick(MAX_FPS)
                        p.display.flip()
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
                if e.key == p.K_m:
                    notation_list = get_notation()
                    if notation_counter < len(notation_list):
                        move = gs.make_notation_move(str(notation_list[notation_counter]))
                        xiangqi_move = gs.xiangqi_notation(move)
                        notation_counter += 1
                        if move in valid_moves:
                            gs.make_move(move)
                            move_made = True
                            move_coords = move
                            xiangqi_moves.append(xiangqi_move)
                            if move.piece_captured != '.':
                                captured_pieces.append(move.piece_captured)
                if e.key == p.K_z:
                    write_notation(xiangqi_moves)
                if e.key == p.K_r:
                    game_over = False
                    gs = XiangQiEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    moves_counter = 1
                    notation_counter = 0
                    captured_pieces = []
                    red_captured_pieces = []
                    black_captured_pieces = []
                    xiangqi_moves = []
                    move_coords = None
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = False
        if not game_over and not human_turn and not move_undone:
            if gs.red_to_move and moves_counter == 1:
                move = gs.make_notation_move(random.choice(RED_START_MOVE))
                xiangqi_move = gs.xiangqi_notation(move)
                if move in valid_moves:
                    gs.make_move(move)
                    move_made = True
                    move_coords = move
                    xiangqi_moves.append(xiangqi_move)
                    if move.piece_captured != '.':
                        captured_pieces.append(move.piece_captured)
            elif not gs.red_to_move and moves_counter == 1:
                move = gs.make_notation_move(random.choice(BLACK_START_MOVE))
                xiangqi_move = gs.xiangqi_notation(move)
                if move in valid_moves:
                    gs.make_move(move)
                    move_made = True
                    move_coords = move
                    xiangqi_moves.append(xiangqi_move)
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
                    ai_move = return_queue.get()
                    if ai_move is None:
                        ai_move = SmartMoveFinder.find_random_move(valid_moves)
                    xiangqi_move = gs.xiangqi_notation(ai_move)
                    gs.make_move(ai_move)
                    move_made = True
                    move_coords = ai_move
                    xiangqi_moves.append(xiangqi_move)
                    ai_thinking = False
                    if ai_move.piece_captured != '.':
                        captured_pieces.append(ai_move.piece_captured)
        if move_made:
            if gs.move_log:
                animate_move(gs.move_log[-1], screen, gs.board, move_coords, clock)
                if not len(gs.move_log) % 2:
                    moves_counter += 1
            valid_moves = gs.get_valid_moves()
            move_made = False
            move_undone = False
        draw_game_state(screen, gs, move_coords, sq_selected, valid_moves, move_log_font, xiangqi_moves, captured_pieces)
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
        clock.tick(MAX_FPS)
        p.display.flip()

def draw_game_state(screen, gs, move_coords, sq_selected, valid_moves, font, xiangqi_moves, captured_pieces):
    draw_board(screen)
    draw_pieces(screen, gs.board, move_coords)
    selected_piece(screen, gs, sq_selected, valid_moves)
    draw_move_notation(screen, font, xiangqi_moves)
    draw_captured_pieces(screen, captured_pieces)

def selected_piece(screen, gs, sq_selected, valid_moves):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('r' if gs.red_to_move else 'b'):
            if gs.board[r][c][0] == 'r':
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

def draw_captured_pieces(screen, captured_pieces):
    red_captured_pieces = []
    black_captured_pieces = []
    count_c = 0
    count_r = 0
    if captured_pieces:
        for piece in captured_pieces:
            if piece[0] == 'r':
                red_captured_pieces.append(piece)
            else:
                black_captured_pieces.append(piece)
    sum_captured_pieces = red_captured_pieces + black_captured_pieces
    if sum_captured_pieces:
        for piece in sum_captured_pieces:
            screen.blit(IMAGES[piece], p.Rect((13 + count_c) * SQ_SIZE, count_r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            count_c += 1
            if count_c > 2:
                count_c = 0
                count_r += 1

def draw_move_notation(screen, font, xiangqi_moves):
    moves_counter = 1
    move_log_rect = p.Rect(SQ_SIZE * 9, 0, WIDTH - SQ_SIZE * 9, HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    padding = 5
    text_y = padding
    line_spacing = 2
    if xiangqi_moves:
        for i in range(len(xiangqi_moves)):
            if i % 2:
                text = f'{moves_counter}. {xiangqi_moves[i - 1]} {xiangqi_moves[i]}'
                moves_counter += 1
            else:
                text = f'{moves_counter}. {xiangqi_moves[i]}'
            text_object = font.render(text, True, p.Color('white'))
            text_location = move_log_rect.move(padding, text_y)
            screen.blit(text_object, text_location)
            if len(text) >= 12:
                text_y += text_object.get_height() + line_spacing
            if moves_counter == 32:
                text_y = 5
                padding = SQ_SIZE * 2
            if moves_counter > 32:
                padding = SQ_SIZE * 2

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

def get_notation():
    with open('notations.txt', 'r') as f:
        return f.readlines()

def write_notation(notations):
    with open('new_notations.txt', 'w') as f:
        for notation in notations:
            f.write(f'{notation} \n')

def draw_game_text(screen, text):
    font = p.font.SysFont('arial', 32, True, False)
    text_object = font.render(text, False, p.Color('Gold'))
    text_location = p.Rect(0, 0, HEIGHT*9/10, HEIGHT).move((HEIGHT/6 - text_object.get_height()/6)*9/10, HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)


if __name__ == '__main__':
    main()
