# Chess AI Agent Documentation

This document describes the AI agent implementation for the chess game.

## Overview

The chess AI agent uses a minimax algorithm with alpha-beta pruning to evaluate positions and select the best moves. It includes multiple difficulty levels and sophisticated position evaluation.

## Features

### Core AI Components

1. **ChessEvaluator** (`src/agent/evaluation.py`)
   - Material evaluation with piece values
   - Piece-square tables for positional evaluation
   - Mobility evaluation (number of legal moves)
   - King safety assessment
   - Pawn structure analysis
   - Endgame detection

2. **ChessAgent** (`src/agent/chess_agent.py`)
   - Minimax algorithm with alpha-beta pruning
   - Iterative deepening for time management
   - Move ordering for better pruning efficiency
   - Configurable difficulty levels
   - Move analysis and suggestions

### Difficulty Levels

| Level  | Search Depth | Randomness | Description |
|--------|--------------|------------|-------------|
| Easy   | 2 ply        | 30%        | Quick moves, some random choices |
| Medium | 3 ply        | 10%        | Balanced play with occasional variety |
| Hard   | 4 ply        | 5%         | Strong tactical play |
| Expert | 5 ply        | 0%         | Maximum strength, no randomness |

### Agent Types

1. **ChessAgent** - Standard minimax agent with evaluation function
2. **RandomAgent** - Makes random legal moves (testing/very easy)
3. **AggressiveAgent** - Prefers captures and attacking moves

## Evaluation Function

The position evaluation considers multiple factors:

### Material Count
- Pawn: 100 centipawns
- Knight: 320 centipawns  
- Bishop: 330 centipawns
- Rook: 500 centipawns
- Queen: 900 centipawns
- King: 20,000 centipawns

### Positional Factors
- **Piece-Square Tables**: Encourage pieces to occupy good squares
- **Mobility**: Reward positions with more legal moves
- **King Safety**: Bonus for castling rights, penalty for checks
- **Pawn Structure**: Penalties for doubled and isolated pawns

### Special Cases
- **Checkmate**: ±20,000 centipawns
- **Stalemate/Draw**: 0 centipawns
- **Endgame**: Uses different king piece-square table

## Search Algorithm

### Minimax with Alpha-Beta Pruning
```
function minimax(position, depth, alpha, beta, maximizing):
    if depth == 0 or game_over:
        return evaluate(position)
    
    if maximizing:
        for each move in legal_moves:
            score = minimax(make_move(position, move), depth-1, alpha, beta, false)
            alpha = max(alpha, score)
            if beta <= alpha:
                break  // Alpha-beta cutoff
        return alpha
    else:
        for each move in legal_moves:
            score = minimax(make_move(position, move), depth-1, alpha, beta, true)
            beta = min(beta, score)
            if beta <= alpha:
                break  // Alpha-beta cutoff
        return beta
```

### Move Ordering
To improve alpha-beta pruning efficiency, moves are ordered by:
1. **Captures** (sorted by MVV-LVA: Most Valuable Victim - Least Valuable Attacker)
2. **Checks**
3. **Normal moves**

### Time Management
- Maximum 5 seconds per move
- Iterative deepening: searches depth 1, 2, 3... up to maximum
- Returns best move found within time limit

## Usage Examples

### Basic Agent Creation
```python
from agent.chess_agent import ChessAgent
import chess

# Create a medium-difficulty agent playing as black
agent = ChessAgent('medium', chess.BLACK)

# Get best move for current position
board = chess.Board()
move = agent.get_best_move(board)
```

### Move Analysis
```python
# Analyze a specific move
move = chess.Move.from_uci("e2e4")
analysis = agent.get_move_analysis(board, move)

print(f"Move: {analysis['algebraic']}")
print(f"Score change: {analysis['score_change']}")
print(f"Comments: {', '.join(analysis['comments'])}")
```

### Full Game Integration
```python
from gui.chess_gui_ai import ChessGUIWithAI
import chess

# Create game with AI enabled
game = ChessGUIWithAI(
    ai_enabled=True,
    ai_difficulty='hard',
    ai_color=chess.BLACK
)
game.run()
```

## Performance Characteristics

### Search Efficiency
- **Nodes searched**: Typically 1,000-50,000 nodes per move (depending on depth)
- **Alpha-beta pruning**: Reduces search space by ~50-90%
- **Move ordering**: Improves pruning effectiveness significantly

### Time Complexity
- **Without pruning**: O(b^d) where b = branching factor (~35), d = depth
- **With alpha-beta**: O(b^(d/2)) in best case
- **Practical performance**: Easy (2-ply) ~0.01s, Expert (5-ply) ~1-5s

### Memory Usage
- **Evaluation tables**: ~2KB for piece-square tables
- **Search tree**: Limited by time rather than memory
- **Move generation**: Uses python-chess library efficiently

## Configuration Options

### GUI Integration
The AI can be controlled through the GUI with these keys:
- **A**: Toggle AI on/off
- **C**: Toggle AI color (white/black)
- **1-4**: Change difficulty (Easy/Medium/Hard/Expert)

### Command Line Options
```bash
# Start with AI as white on expert difficulty
python play_chess_ai.py --ai-color white --difficulty expert

# Human vs human mode
python play_chess_ai.py --human-only

# AI disabled (can be enabled in-game)
python play_chess_ai.py --difficulty easy
```

## Testing

Run the AI tests:
```bash
python tests/test_agent.py
```

Test coverage includes:
- Position evaluation accuracy
- Move legality validation
- Different difficulty levels
- Agent vs agent games
- Move analysis functionality
- Performance benchmarks

## Future Enhancements

Planned improvements:
- **Opening book**: Pre-computed opening moves
- **Endgame tablebase**: Perfect endgame play
- **Neural network evaluation**: ML-based position assessment
- **Quiescence search**: Extend search for tactical sequences
- **Transposition table**: Cache evaluated positions
- **Multi-threading**: Parallel search for better performance
