import pygame as p
from constants import WIDTH, HEIGHT, MAX_FPS
from chess_engine import GameState, Move
from chess_gui import draw_game_state, load_images
from ai import find_best_move
import random

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    animate = False
    load_images()
    running = True
    sq_selected = ()
    player_clicks = []
    game_over = False
    player_one = True 
    player_two = False

    while running:
        is_human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and is_human_turn:
                    location = p.mouse.get_pos()
                    col = location[0] // (WIDTH // 8)
                    row = location[1] // (HEIGHT // 8)
                    if sq_selected == (row, col):
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)
                    if len(player_clicks) == 2:
                        move = Move(player_clicks[0], player_clicks[1], gs.board)
                        if move in valid_moves:
                            gs.make_move(move)
                            move_made = True
                            animate = True
                            sq_selected = ()
                            player_clicks = []
                        else:
                            player_clicks = [sq_selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True
                    animate = False
                    game_over = False
                elif e.key == p.K_r:
                    gs = GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False

        if not game_over and not is_human_turn:
            ai_move = find_best_move(gs, valid_moves)
            if ai_move is None:
                ai_move = random.choice(valid_moves)
            gs.make_move(ai_move)
            move_made = True
            animate = True

        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, gs, valid_moves, sq_selected)

        if gs.checkmate:
            game_over = True
            if gs.white_to_move:
                draw_endgame_text(screen, 'Black wins by checkmate')
            else:
                draw_endgame_text(screen, 'White wins by checkmate')
        elif gs.stalemate:
            game_over = True
            draw_endgame_text(screen, 'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()

def animate_move(move, screen, board, clock):
    pass

def draw_endgame_text(screen, text):
    font = p.font.SysFont('Helvetica', 32, True, False)
    text_object = font.render(text, False, p.Color('Gray'))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH // 2 - text_object.get_width() // 2,
        HEIGHT // 2 - text_object.get_height() // 2
    )
    screen.blit(text_object, text_location)

if __name__ == '__main__':
    main()
