import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.chess_gui import ChessGUI
import chess

class TestChessGUI(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Note: We won't actually initialize pygame for unit tests
        # as it requires a display. We'll test the logic methods only.
        pass
    
    def test_square_conversion(self):
        """Test coordinate to square conversion."""
        gui = ChessGUI()
        
        # Test coords_to_square (using SQUARE_SIZE = 80)
        self.assertEqual(gui.coords_to_square(0, 560), 0)    # a1
        self.assertEqual(gui.coords_to_square(560, 0), 63)   # h8
        self.assertEqual(gui.coords_to_square(240, 320), 27) # d4
        
        # Test square_to_coords
        self.assertEqual(gui.square_to_coords(0), (0, 560))   # a1
        self.assertEqual(gui.square_to_coords(63), (560, 0))  # h8
        self.assertEqual(gui.square_to_coords(27), (240, 320)) # d4
    
    def test_board_state_integration(self):
        """Test that GUI properly integrates with BoardState."""
        gui = ChessGUI()
        
        # Test initial position
        self.assertIsNotNone(gui.board_state.board)
        self.assertTrue(len(gui.board_state.get_legal_moves()) > 0)
        
        # Test making a move
        initial_fen = gui.board_state.fen()
        gui.board_state.make_move("e2e4")
        new_fen = gui.board_state.fen()
        
        # After e2e4, the position should be different and it should be black's turn
        self.assertFalse(gui.board_state.board.turn)  # Should be black's turn
        self.assertNotEqual(initial_fen, new_fen)     # Position should be different

if __name__ == '__main__':
    unittest.main()
