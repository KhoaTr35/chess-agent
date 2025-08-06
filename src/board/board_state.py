import chess

class BoardState:
    def __init__(self):
        self.board = chess.Board()

    def reset(self):
        """Reset the board to the initial position."""
        self.board.reset()

    def get_legal_moves(self):
        """Return a list of all legal moves."""
        return list(self.board.legal_moves)

    def make_move(self, move):
        """
        Apply a move if it's legal.
        Args:
            move (chess.Move or str): e.g. "e2e4"
        Returns:
            bool: True if move was made, False if illegal
        """
        if isinstance(move, str):
            move = chess.Move.from_uci(move)

        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False

    def undo_move(self):
        """Undo the last move."""
        if self.board.move_stack:
            self.board.pop()

    def is_game_over(self):
        return self.board.is_game_over()

    def get_result(self):
        """Get game result if it's over."""
        if self.board.is_game_over():
            return self.board.result()
        return None

    def print_board(self):
        print(self.board)

    def fen(self):
        return self.board.fen()

    def turn(self):
        return "White" if self.board.turn == chess.WHITE else "Black"
