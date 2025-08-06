#!/usr/bin/env python3
"""
Chess Game with AI Launcher
Run this script to start the interactive chess game with AI opponent.
"""

import sys
import os
import argparse

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def main():
    """Launch the chess game with AI."""
    parser = argparse.ArgumentParser(description='Chess Game with AI')
    parser.add_argument('--ai', action='store_true', default=True,
                        help='Enable AI opponent (default: True)')
    parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard', 'expert'],
                        default='medium', help='AI difficulty level (default: medium)')
    parser.add_argument('--ai-color', choices=['white', 'black'], default='black',
                        help='AI color (default: black)')
    parser.add_argument('--human-only', action='store_true',
                        help='Play human vs human (disable AI)')
    
    args = parser.parse_args()
    
    # Disable AI if human-only mode is requested
    if args.human_only:
        args.ai = False
    
    print("=== Chess Game with AI ===")
    print()
    
    if args.ai:
        print("🤖 AI Features:")
        print(f"  ✓ Difficulty: {args.difficulty.title()}")
        print(f"  ✓ AI Color: {args.ai_color.title()}")
        print("  ✓ Minimax algorithm with alpha-beta pruning")
        print("  ✓ Position evaluation with multiple factors")
        print("  ✓ Move ordering for better performance")
        print()
    else:
        print("👥 Human vs Human mode")
        print()
    
    print("🎮 Game Controls:")
    print("  Mouse: Click to select pieces and make moves")
    print("  R key: Reset the game")
    print("  U key: Undo last move")
    print("  A key: Toggle AI on/off")
    print("  C key: Toggle AI color")
    print("  1-4 keys: Change AI difficulty (Easy/Medium/Hard/Expert)")
    print("  Close window: Quit the game")
    print()
    
    try:
        from gui.chess_gui_ai import ChessGUIWithAI
        import chess
        
        ai_color = chess.WHITE if args.ai_color == 'white' else chess.BLACK
        
        print("Starting the chess game...")
        game = ChessGUIWithAI(
            ai_enabled=args.ai,
            ai_difficulty=args.difficulty,
            ai_color=ai_color
        )
        game.run()
        
    except ImportError as e:
        print(f"❌ Error importing game modules: {e}")
        print("Make sure you have installed the required dependencies:")
        print("  pip install pygame python-chess")
    except Exception as e:
        print(f"❌ Error starting the game: {e}")

if __name__ == "__main__":
    main()
