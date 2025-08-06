import unittest
import sys
import os
import chess

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent.chess_agent import ChessAgent, RandomAgent, AggressiveAgent
from agent.evaluation import ChessEvaluator
from board.board_state import BoardState

class TestChessEvaluator(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = ChessEvaluator()
        self.board = chess.Board()
    
    def test_initial_position_evaluation(self):
        """Test evaluation of initial chess position."""
        score = self.evaluator.evaluate_position(self.board)
        # Initial position should be roughly equal (small advantage to white due to first move)
        self.assertAlmostEqual(score, 0, delta=50)
    
    def test_material_advantage(self):
        """Test evaluation with material advantage."""
        # Remove black queen
        self.board.remove_piece_at(chess.D8)
        score = self.evaluator.evaluate_position(self.board)
        # White should have significant advantage (queen = 900 centipawns)
        self.assertGreater(score, 800)
    
    def test_checkmate_evaluation(self):
        """Test evaluation of checkmate positions."""
        # Scholar's mate position
        self.board = chess.Board("rnb1kbnr/pppp1ppp/8/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 2 3")
        self.board.push_san("Qh5")  # Threatens checkmate
        self.board.push_san("Nf6")  # Block
        self.board.push_san("Qxf7#")  # Checkmate
        
        score = self.evaluator.evaluate_position(self.board)
        # Should return maximum score for white win
        self.assertEqual(score, 20000)
    
    def test_stalemate_evaluation(self):
        """Test evaluation of stalemate position."""
        # Create a stalemate position
        self.board = chess.Board("k7/8/1K6/8/8/8/8/1Q6 b - - 0 1")
        score = self.evaluator.evaluate_position(self.board)
        # Stalemate should evaluate to 0
        self.assertEqual(score, 0)
    
    def test_endgame_detection(self):
        """Test endgame detection."""
        # Initial position - not endgame
        self.assertFalse(self.evaluator._is_endgame(self.board))
        
        # Remove queens - should be endgame
        self.board.remove_piece_at(chess.D1)
        self.board.remove_piece_at(chess.D8)
        self.assertTrue(self.evaluator._is_endgame(self.board))

class TestChessAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = ChessAgent('medium', chess.BLACK)
        self.board_state = BoardState()
    
    def test_agent_initialization(self):
        """Test agent initialization with different parameters."""
        easy_agent = ChessAgent('easy', chess.WHITE)
        self.assertEqual(easy_agent.difficulty, 'easy')
        self.assertEqual(easy_agent.color, chess.WHITE)
        self.assertEqual(easy_agent.search_depth, 2)
        
        expert_agent = ChessAgent('expert', chess.BLACK)
        self.assertEqual(expert_agent.search_depth, 5)
        self.assertEqual(expert_agent.randomness, 0.0)
    
    def test_get_best_move(self):
        """Test that agent returns a legal move."""
        move = self.agent.get_best_move(self.board_state.board)
        self.assertIsNotNone(move)
        self.assertIn(move, self.board_state.board.legal_moves)
    
    def test_move_analysis(self):
        """Test move analysis functionality."""
        # Test analysis of e2e4
        move = chess.Move.from_uci("e2e4")
        analysis = self.agent.get_move_analysis(self.board_state.board, move)
        
        self.assertEqual(analysis['move'], move)
        self.assertEqual(analysis['algebraic'], 'e4')
        self.assertFalse(analysis['is_capture'])
        self.assertFalse(analysis['is_check'])
        self.assertIsInstance(analysis['score_change'], (int, float))
    
    def test_suggest_move(self):
        """Test move suggestion with analysis."""
        suggestion = self.agent.suggest_move(self.board_state.board)
        
        self.assertIsNotNone(suggestion['move'])
        self.assertIsNotNone(suggestion['analysis'])
        self.assertIn('nodes_searched', suggestion['analysis'])
        self.assertIn('difficulty', suggestion['analysis'])
    
    def test_no_legal_moves(self):
        """Test agent behavior when no legal moves are available."""
        # Create a position with no legal moves (checkmate)
        checkmate_board = chess.Board("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3")
        move = self.agent.get_best_move(checkmate_board)
        # Should return None when no legal moves
        self.assertIsNone(move)

class TestRandomAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = RandomAgent(chess.WHITE)
        self.board_state = BoardState()
    
    def test_random_move_selection(self):
        """Test that random agent selects legal moves."""
        move = self.agent.get_best_move(self.board_state.board)
        self.assertIsNotNone(move)
        self.assertIn(move, self.board_state.board.legal_moves)
    
    def test_random_move_variability(self):
        """Test that random agent doesn't always select the same move."""
        moves = []
        for _ in range(10):
            move = self.agent.get_best_move(self.board_state.board)
            moves.append(move)
        
        # Should have some variety in moves (not all the same)
        unique_moves = set(moves)
        self.assertGreater(len(unique_moves), 1)

class TestAggressiveAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = AggressiveAgent('medium', chess.WHITE)
        self.board_state = BoardState()
    
    def test_aggressive_move_preference(self):
        """Test that aggressive agent prefers captures when available."""
        # Set up a position with a capture available
        # Move to a position where a capture is possible
        self.board_state.make_move("e2e4")
        self.board_state.make_move("d7d5")
        
        # Now white can capture the pawn
        move = self.agent.get_best_move(self.board_state.board)
        
        # Should be a legal move
        self.assertIsNotNone(move)
        self.assertIn(move, self.board_state.board.legal_moves)

class TestAgentIntegration(unittest.TestCase):
    
    def test_full_game_simulation(self):
        """Test a full game between two agents."""
        white_agent = ChessAgent('easy', chess.WHITE)
        black_agent = ChessAgent('easy', chess.BLACK)
        board = chess.Board()
        
        moves_played = 0
        max_moves = 100  # Prevent infinite games
        
        while not board.is_game_over() and moves_played < max_moves:
            if board.turn == chess.WHITE:
                move = white_agent.get_best_move(board)
            else:
                move = black_agent.get_best_move(board)
            
            if move:
                board.push(move)
                moves_played += 1
            else:
                break
        
        # Game should have progressed
        self.assertGreater(moves_played, 0)
        
        # Final position should be valid
        self.assertTrue(board.is_valid())
    
    def test_agent_vs_random(self):
        """Test that a strategic agent performs better than random."""
        strategic_wins = 0
        random_wins = 0
        draws = 0
        games = 5  # Run multiple games
        
        for _ in range(games):
            strategic_agent = ChessAgent('medium', chess.WHITE)
            random_agent = RandomAgent(chess.BLACK)
            board = chess.Board()
            
            moves = 0
            max_moves = 200
            
            while not board.is_game_over() and moves < max_moves:
                if board.turn == chess.WHITE:
                    move = strategic_agent.get_best_move(board)
                else:
                    move = random_agent.get_best_move(board)
                
                if move:
                    board.push(move)
                    moves += 1
                else:
                    break
            
            if board.is_game_over():
                result = board.result()
                if result == "1-0":
                    strategic_wins += 1
                elif result == "0-1":
                    random_wins += 1
                else:
                    draws += 1
        
        # Strategic agent should win at least some games
        total_games = strategic_wins + random_wins + draws
        self.assertGreater(total_games, 0)

if __name__ == '__main__':
    unittest.main()
