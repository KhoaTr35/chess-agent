#!/usr/bin/env python3
"""
Chess Game Demo
This script demonstrates how to run the interactive chess game.
"""

import sys
import os

def main():
    print("=== Chess Game Demo ===")
    print()
    print("This is an interactive chess game with the following features:")
    print("✓ Click-to-move interface")
    print("✓ Visual highlighting of legal moves")
    print("✓ Game status display")
    print("✓ Undo functionality")
    print("✓ Reset game functionality")
    print()
    
    try:
        # Import and run the game
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(current_dir, 'src')
        sys.path.insert(0, src_dir)
        
        from gui.chess_gui import ChessGUI
        
        print("Starting the chess game...")
        print("Game Controls:")
        print("  Mouse: Click to select pieces and make moves")
        print("  R key: Reset the game")
        print("  U key: Undo last move")
        print("  Close window: Quit the game")
        print()
        print("Enjoy your game!")
        
        game = ChessGUI()
        game.run()
        
    except ImportError as e:
        print(f"Error importing game modules: {e}")
        print("Make sure you have installed the required dependencies:")
        print("  pip install pygame python-chess")
    except Exception as e:
        print(f"Error starting the game: {e}")

if __name__ == "__main__":
    main()
