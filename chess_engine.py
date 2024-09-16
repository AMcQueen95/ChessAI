# chess_engine.py

class GameState:
    def __init__(self):
        # 8x8 board initialization
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.move_functions = {
            'p': self.get_pawn_moves,
            'R': self.get_rook_moves,
            'N': self.get_knight_moves,
            'B': self.get_bishop_moves,
            'Q': self.get_queen_moves,
            'K': self.get_king_moves
        }
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False

    def make_move(self, move):
        # Update the board
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        # Update king's location
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

    def undo_move(self):
        # Undo the last move
        if self.move_log:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            # Update king's location
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)

    def get_valid_moves(self):
        moves = self.get_all_possible_moves()
        # For each move, make the move, check for checks
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])  # Move leaves king in check
            self.white_to_move = not self.white_to_move
            self.undo_move()
        if not moves:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        return moves

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location)
        else:
            return self.square_under_attack(self.black_king_location)

    def square_under_attack(self, king_position):
        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opponent_moves:
            if move.end_row == king_position[0] and move.end_col == king_position[1]:
                return True
        return False

    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece_type = self.board[row][col][1]
                    self.move_functions[piece_type](row, col, moves)
        return moves

    # Implement piece-specific move functions (examples below)

    def get_pawn_moves(self, r, c, moves):
        if self.white_to_move:  # White pawn moves
            if self.board[r - 1][c] == "--":  # Move forward by 1 square
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # Move forward by 2 squares if on starting rank
                    moves.append(Move((r, c), (r - 2, c), self.board))
            # Capturing diagonally
            if c - 1 >= 0:  # Capture to the left
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # Capture to the right
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:  # Black pawn moves
            if self.board[r + 1][c] == "--":  # Move forward by 1 square
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # Move forward by 2 squares if on starting rank
                    moves.append(Move((r, c), (r + 2, c), self.board))
            # Capturing diagonally
            if c - 1 >= 0:  # Capture to the left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # Capture to the right
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))


    def get_rook_moves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):  # Maximum distance a rook can move
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # Within bounds
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Empty square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Capture enemy piece
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # Friendly piece is blocking
                        break
                else:
                    break


    def get_knight_moves(self, r, c, moves):
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        ally_color = 'w' if self.white_to_move else 'b'
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:  # Within bounds
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] != ally_color:  # Either empty or enemy piece
                    moves.append(Move((r, c), (end_row, end_col), self.board))


    def get_bishop_moves(self, r, c, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):  # Maximum distance a bishop can move
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # Within bounds
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Empty square
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Capture enemy piece
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # Friendly piece is blocking
                        break
                else:
                    break


    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)  # Queen moves like a rook
        self.get_bishop_moves(r, c, moves)  # Queen moves like a bishop


    def get_king_moves(self, r, c, moves):
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        ally_color = 'w' if self.white_to_move else 'b'
        for m in king_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:  # Within bounds
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] != ally_color:  # Either empty or enemy piece
                    moves.append(Move((r, c), (end_row, end_col), self.board))


class Move:
    # Maps for converting rows and columns to chess notation
    ranks_to_rows = {str(i + 1): 7 - i for i in range(8)}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {chr(97 + i): i for i in range(8)}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # For move ordering
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    # Overriding equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        # Returns move in standard chess notation
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
