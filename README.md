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
- 🤖 **AI Opponent**: Multiple difficulty levels with minimax algorithm
- 🧠 **Smart Evaluation**: Position evaluation with material, mobility, and positional factors
- ⚡ **Alpha-Beta Pruning**: Efficient search with move ordering optimization
- 🎯 **Difficulty Levels**: Easy, Medium, Hard, and Expert modes
- 📊 **Move Analysis**: Detailed analysis of moves with scoring
- 🔄 **Flexible AI**: Toggle AI on/off, change difficulty, and switch colors during play

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

Launch the interactive chess game with AI:
```bash
python play_chess_ai.py
```

Or launch the basic version:
```bash
python play_chess.py
```

Run the demo:
```bash
python demo.py
```

#### AI Options
```bash
# Play against AI as black (medium difficulty)
python play_chess_ai.py

# Play as black against expert AI
python play_chess_ai.py --difficulty expert --ai-color white

# Human vs human mode
python play_chess_ai.py --human-only
```

### Game Controls

#### Mouse Controls
- **Left Click**: Select a piece or make a move
  - Click on a piece to select it (shows legal moves)
  - Click on a highlighted square to move the selected piece

#### Keyboard Controls
- **R**: Reset the game to starting position
- **U**: Undo the last move
- **A**: Toggle AI on/off
- **C**: Toggle AI color (white/black)
- **1-4**: Change AI difficulty (Easy/Medium/Hard/Expert)
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
│   │   ├── chess_gui_ai.py
│   │   └── README.md
│   └── utils/           # Utility functions
│       └── move_generator.py
├── tests/               # Unit tests
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup
├── play_chess.py       # Basic game launcher
├── play_chess_ai.py    # AI game launcher
├── demo.py             # Demo script
└── AI_DOCUMENTATION.md # AI implementation details
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

- 📁 Save and load games (PGN format)
- 🎨 Customizable themes and piece sets
- 🌐 Online multiplayer support
- 📈 Game analysis and move suggestions
- 📚 Opening book integration
- 🏆 Endgame tablebase support

## Contributing

Feel free to contribute to this project by:
- Adding new features
- Improving the AI agent
- Enhancing the user interface
- Writing additional tests
- Fixing bugs

## License

This project is licensed under the MIT License - see the LICENSE file for details.
