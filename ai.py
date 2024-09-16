# ai.py

import random
import math

piece_scores = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}

CHECKMATE = 1000
STALEMATE = 0

def find_best_move(gs, valid_moves):
    global best_move
    best_move = None
    random.shuffle(valid_moves)
    find_move_nega_max_alpha_beta(gs, valid_moves, DEPTH=3, alpha=-CHECKMATE, beta=CHECKMATE, turn_multiplier=1 if gs.white_to_move else -1)
    return best_move

def find_move_nega_max_alpha_beta(gs, valid_moves, DEPTH, alpha, beta, turn_multiplier):
    global best_move
    if DEPTH == 0:
        return turn_multiplier * score_board(gs)

    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(gs, next_moves, DEPTH - 1, -beta, -alpha, -turn_multiplier)
        gs.undo_move()
        if score > max_score:
            max_score = score
            if DEPTH == 3:
                best_move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return max_score

def score_board(gs):
    if gs.checkmate:
        if gs.white_to_move:
            return -CHECKMATE  # Black wins
        else:
            return CHECKMATE  # White wins
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += piece_scores[square[1]]
            elif square[0] == 'b':
                score -= piece_scores[square[1]]
    return score
