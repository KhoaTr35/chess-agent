"""
Chess AI Agent Module

This module implements various AI algorithms for playing chess,
including minimax with alpha-beta pruning and different difficulty levels.
"""

import chess
import random
import time
from typing import Optional, Tuple, List
from .evaluation import ChessEvaluator

class ChessAgent:
    """
    Chess AI agent with configurable difficulty levels and search algorithms.
    """
    
    DIFFICULTY_LEVELS = {
        'easy': {'depth': 2, 'randomness': 0.3},
        'medium': {'depth': 3, 'randomness': 0.1},
        'hard': {'depth': 4, 'randomness': 0.05},
        'expert': {'depth': 5, 'randomness': 0.0}
    }
    
    def __init__(self, difficulty='medium', color=chess.BLACK):
        """
        Initialize the chess agent.
        
        Args:
            difficulty (str): Difficulty level ('easy', 'medium', 'hard', 'expert')
            color (bool): Color the agent plays (chess.WHITE or chess.BLACK)
        """
        self.difficulty = difficulty
        self.color = color
        self.evaluator = ChessEvaluator()
        self.search_depth = self.DIFFICULTY_LEVELS[difficulty]['depth']
        self.randomness = self.DIFFICULTY_LEVELS[difficulty]['randomness']
        self.nodes_searched = 0
        self.time_limit = 5.0  # Maximum time per move in seconds
        
    def get_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        """
        Get the best move for the current position.
        
        Args:
            board (chess.Board): Current board position
            
        Returns:
            chess.Move: Best move found, or None if no legal moves
        """
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        
        # For very easy difficulty, sometimes make random moves
        if self.difficulty == 'easy' and random.random() < 0.2:
            return random.choice(legal_moves)
        
        start_time = time.time()
        self.nodes_searched = 0
        
        best_move = None
        best_score = float('-inf') if board.turn == self.color else float('inf')
        
        # Try iterative deepening for better time management
        for depth in range(1, self.search_depth + 1):
            if time.time() - start_time > self.time_limit * 0.8:
                break
                
            move, score = self._minimax_root(board, depth, start_time)
            if move:
                best_move = move
                best_score = score
        
        # Add some randomness for lower difficulties
        if self.randomness > 0 and random.random() < self.randomness:
            # Get top moves within a reasonable score range
            good_moves = self._get_good_moves(board, best_score)
            if good_moves:
                best_move = random.choice(good_moves)
        
        return best_move
    
    def _minimax_root(self, board: chess.Board, depth: int, start_time: float) -> Tuple[Optional[chess.Move], float]:
        """
        Root minimax function that returns the best move and its score.
        """
        best_move = None
        
        if board.turn == self.color:
            best_score = float('-inf')
            for move in board.legal_moves:
                if time.time() - start_time > self.time_limit:
                    break
                    
                board.push(move)
                score = self._minimax(board, depth - 1, float('-inf'), float('inf'), False, start_time)
                board.pop()
                
                if score > best_score:
                    best_score = score
                    best_move = move
        else:
            best_score = float('inf')
            for move in board.legal_moves:
                if time.time() - start_time > self.time_limit:
                    break
                    
                board.push(move)
                score = self._minimax(board, depth - 1, float('-inf'), float('inf'), True, start_time)
                board.pop()
                
                if score < best_score:
                    best_score = score
                    best_move = move
        
        return best_move, best_score
    
    def _minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, 
                 maximizing: bool, start_time: float) -> float:
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            board: Current board position
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing: True if maximizing player's turn
            start_time: Start time for time management
            
        Returns:
            float: Evaluation score
        """
        self.nodes_searched += 1
        
        # Time check
        if time.time() - start_time > self.time_limit:
            return self.evaluator.evaluate_position(board)
        
        # Base case: maximum depth reached or game over
        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate_position(board)
        
        legal_moves = list(board.legal_moves)
        
        # Move ordering: captures and checks first
        legal_moves = self._order_moves(board, legal_moves)
        
        if maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval_score = self._minimax(board, depth - 1, alpha, beta, False, start_time)
                board.pop()
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break  # Alpha-beta pruning
                    
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval_score = self._minimax(board, depth - 1, alpha, beta, True, start_time)
                board.pop()
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break  # Alpha-beta pruning
                    
            return min_eval
    
    def _order_moves(self, board: chess.Board, moves: List[chess.Move]) -> List[chess.Move]:
        """
        Order moves for better alpha-beta pruning efficiency.
        
        Priority: Captures > Checks > Normal moves
        """
        captures = []
        checks = []
        normal = []
        
        for move in moves:
            if board.is_capture(move):
                captures.append(move)
            elif board.gives_check(move):
                checks.append(move)
            else:
                normal.append(move)
        
        # Sort captures by Most Valuable Victim - Least Valuable Attacker (MVV-LVA)
        captures.sort(key=lambda move: self._mvv_lva_score(board, move), reverse=True)
        
        return captures + checks + normal
    
    def _mvv_lva_score(self, board: chess.Board, move: chess.Move) -> int:
        """
        Calculate MVV-LVA (Most Valuable Victim - Least Valuable Attacker) score.
        """
        victim = board.piece_at(move.to_square)
        attacker = board.piece_at(move.from_square)
        
        if victim and attacker:
            victim_value = self.evaluator.PIECE_VALUES.get(victim.piece_type, 0)
            attacker_value = self.evaluator.PIECE_VALUES.get(attacker.piece_type, 0)
            return victim_value - attacker_value // 10
        
        return 0
    
    def _get_good_moves(self, board: chess.Board, best_score: float) -> List[chess.Move]:
        """
        Get moves that are within a reasonable score range of the best move.
        """
        good_moves = []
        score_threshold = 50  # Allow moves within 50 centipawns of best
        
        for move in board.legal_moves:
            board.push(move)
            score = self.evaluator.evaluate_position(board)
            board.pop()
            
            if abs(score - best_score) <= score_threshold:
                good_moves.append(move)
        
        return good_moves if good_moves else [random.choice(list(board.legal_moves))]
    
    def get_move_analysis(self, board: chess.Board, move: chess.Move) -> dict:
        """
        Analyze a specific move and return detailed information.
        
        Args:
            board: Current board position
            move: Move to analyze
            
        Returns:
            dict: Move analysis including score, type, and comments
        """
        analysis = {
            'move': move,
            'algebraic': board.san(move),
            'is_capture': board.is_capture(move),
            'is_check': board.gives_check(move),
            'is_castling': board.is_castling(move),
            'comments': []
        }
        
        # Calculate position evaluation before and after move
        initial_score = self.evaluator.evaluate_position(board)
        board.push(move)
        final_score = self.evaluator.evaluate_position(board)
        board.pop()
        
        analysis['score_change'] = final_score - initial_score
        analysis['evaluation'] = final_score
        
        # Add comments based on move characteristics
        if analysis['is_capture']:
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                piece_name = chess.piece_name(captured_piece.piece_type)
                analysis['comments'].append(f"Captures {piece_name}")
        
        if analysis['is_check']:
            analysis['comments'].append("Gives check")
        
        if analysis['is_castling']:
            analysis['comments'].append("Castling")
        
        if move.promotion:
            promoted_piece = chess.piece_name(move.promotion)
            analysis['comments'].append(f"Promotes to {promoted_piece}")
        
        return analysis
    
    def suggest_move(self, board: chess.Board) -> dict:
        """
        Suggest a move with detailed analysis.
        
        Returns:
            dict: Move suggestion with analysis
        """
        best_move = self.get_best_move(board)
        if not best_move:
            return {'move': None, 'analysis': None}
        
        analysis = self.get_move_analysis(board, best_move)
        analysis['nodes_searched'] = self.nodes_searched
        analysis['difficulty'] = self.difficulty
        analysis['search_depth'] = self.search_depth
        
        return {
            'move': best_move,
            'analysis': analysis
        }

class RandomAgent(ChessAgent):
    """
    Simple random agent for testing or very easy difficulty.
    """
    
    def __init__(self, color=chess.BLACK):
        super().__init__('easy', color)
    
    def get_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Return a random legal move."""
        legal_moves = list(board.legal_moves)
        return random.choice(legal_moves) if legal_moves else None

class AggressiveAgent(ChessAgent):
    """
    Agent that prefers aggressive moves (captures, checks, attacks).
    """
    
    def __init__(self, difficulty='medium', color=chess.BLACK):
        super().__init__(difficulty, color)
    
    def _order_moves(self, board: chess.Board, moves: List[chess.Move]) -> List[chess.Move]:
        """Override move ordering to heavily favor aggressive moves."""
        captures = []
        checks = []
        attacks = []
        normal = []
        
        for move in moves:
            if board.is_capture(move):
                captures.append(move)
            elif board.gives_check(move):
                checks.append(move)
            elif self._is_attacking_move(board, move):
                attacks.append(move)
            else:
                normal.append(move)
        
        captures.sort(key=lambda move: self._mvv_lva_score(board, move), reverse=True)
        
        return captures + checks + attacks + normal
    
    def _is_attacking_move(self, board: chess.Board, move: chess.Move) -> bool:
        """Check if a move attacks enemy pieces."""
        board.push(move)
        attacking = False
        
        # Check if the moved piece attacks any enemy pieces
        piece_square = move.to_square
        piece = board.piece_at(piece_square)
        
        if piece:
            attacked_squares = board.attacks(piece_square)
            for square in attacked_squares:
                target_piece = board.piece_at(square)
                if target_piece and target_piece.color != piece.color:
                    attacking = True
                    break
        
        board.pop()
        return attacking
