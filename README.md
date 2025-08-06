# Chess Agent Project

An interactive chess game with AI agent capabilities built using Python, pygame, and python-chess.

## Features

### Interactive Chess Game
- 🎮 **Graphical Interface**: Full interactive chess board with click-to-move functionality
- ♟️ **Complete Chess Rules**: Full implementation of chess rules including castling, en passant, and promotion
- 🎯 **Visual Feedback**: Highlighting of selected pieces and legal moves
- ↩️ **Move History**: Undo moves and reset the game
- 🏆 **Game States**: Automatic detection of check, checkmate, stalemate, and draws

### Chess Engine
- 🤖 **Board State Management**: Efficient board representation and move generation
- 🧠 **AI Agent Framework**: Ready for implementing chess AI algorithms
- 📊 **Position Evaluation**: Foundation for implementing position evaluation functions

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chess-agent-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Game

Launch the interactive chess game:
```bash
python play_chess.py
```

Or run the demo:
```bash
python demo.py
```

### Game Controls

#### Mouse Controls
- **Left Click**: Select a piece or make a move
  - Click on a piece to select it (shows legal moves)
  - Click on a highlighted square to move the selected piece

#### Keyboard Controls
- **R**: Reset the game to starting position
- **U**: Undo the last move
- **ESC/Close Window**: Quit the game

## Project Structure

```
chess-agent-project/
├── src/
│   ├── agent/           # AI agent implementation
│   │   ├── chess_agent.py
│   │   └── evaluation.py
│   ├── board/           # Chess board logic
│   │   └── board_state.py
│   ├── gui/             # Graphical user interface
│   │   ├── chess_gui.py
│   │   └── README.md
│   └── utils/           # Utility functions
│       └── move_generator.py
├── tests/               # Unit tests
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup
├── play_chess.py       # Game launcher
└── demo.py             # Demo script
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Running Individual Test Files
```bash
python tests/test_gui.py
python tests/test_board.py
```

## Dependencies

- **pygame**: For the graphical user interface
- **python-chess**: For chess logic, rules, and move validation

## Future Enhancements

- 🤖 AI opponent with different difficulty levels
- 📁 Save and load games (PGN format)
- 🎨 Customizable themes and piece sets
- 🌐 Online multiplayer support
- 📈 Game analysis and move suggestions

## Contributing

Feel free to contribute to this project by:
- Adding new features
- Improving the AI agent
- Enhancing the user interface
- Writing additional tests
- Fixing bugs

## License

This project is licensed under the MIT License - see the LICENSE file for details.
