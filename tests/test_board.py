from src.board.board_state import BoardState

board = BoardState()
board.print_board()

print("Legal moves:", board.get_legal_moves())

# Try a move
if board.make_move("e2e4"):
    print("\nAfter e2e4:")
    board.print_board()
else:
    print("Invalid move.")
