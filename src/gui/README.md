# Chess Game GUI

This directory contains the graphical user interface for the chess game.

## Features

- Interactive chess board with click-to-move functionality
- Visual highlighting of selected pieces and legal moves
- Game status display (current player, check status, game result)
- Keyboard shortcuts for game control

## Controls

### Mouse Controls
- **Left Click**: Select a piece or make a move
  - Click on a piece to select it (highlights legal moves)
  - Click on a highlighted square to move the selected piece
  - Click on another piece of the same color to select it instead

### Keyboard Controls
- **R**: Reset the game to the starting position
- **U**: Undo the last move
- **ESC/Close Window**: Quit the game

## Game Features

- **Legal Move Validation**: Only legal moves are allowed
- **Check Detection**: Visual indication when a king is in check
- **Game End Detection**: Automatic detection of checkmate, stalemate, and draws
- **Piece Promotion**: Pawns are automatically promoted to queens when reaching the end
- **Move History**: Support for undoing moves

## Visual Elements

- **Light Brown Squares**: Light squares on the chess board
- **Dark Brown Squares**: Dark squares on the chess board
- **Green Highlight**: Currently selected piece
- **Yellow Highlights**: Legal move destinations for the selected piece
- **Unicode Chess Pieces**: Clear visual representation of all piece types

## Running the Game

From the project root directory:

```bash
python play_chess.py
```

Or directly:

```bash
python src/gui/chess_gui.py
```

## Dependencies

- `pygame`: For the graphical interface
- `python-chess`: For chess logic and rules
- `sys`, `os`: For path management (built-in Python modules)
