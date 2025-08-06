#!/usr/bin/env python3
"""
Chess Game Launcher
Run this script to start the interactive chess game.
"""

import sys
import os

# Add src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from gui.chess_gui import ChessGUI

def main():
    """Launch the chess game."""
    print("Starting Chess Game...")
    print("Controls:")
    print("- Click to select and move pieces")
    print("- Press 'R' to reset the game")
    print("- Press 'U' to undo the last move")
    print("- Close the window to quit")
    
    try:
        game = ChessGUI()
        game.run()
    except Exception as e:
        print(f"Error starting the game: {e}")
        print("Make sure you have pygame and python-chess installed:")
        print("pip install pygame python-chess")

if __name__ == "__main__":
    main()
