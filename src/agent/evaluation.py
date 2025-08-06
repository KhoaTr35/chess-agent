"""
Chess Position Evaluation Module

This module provides various evaluation functions for chess positions,
including material count, piece-square tables, and positional factors.
"""

import chess

class ChessEvaluator:
    """
    Chess position evaluator with multiple evaluation criteria.
    """
    
    # Piece values in centipawns
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }
    
    # Piece-square tables for positional evaluation
    # Values are from white's perspective, need to flip for black
    PAWN_TABLE = [
        [  0,   0,   0,   0,   0,   0,   0,   0],
        [ 50,  50,  50,  50,  50,  50,  50,  50],
        [ 10,  10,  20,  30,  30,  20,  10,  10],
        [  5,   5,  10,  25,  25,  10,   5,   5],
        [  0,   0,   0,  20,  20,   0,   0,   0],
        [  5,  -5, -10,   0,   0, -10,  -5,   5],
        [  5,  10,  10, -20, -20,  10,  10,   5],
        [  0,   0,   0,   0,   0,   0,   0,   0]
    ]
    
    KNIGHT_TABLE = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-30,   5,  15,  20,  20,  15,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]
    
    BISHOP_TABLE = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ]
    
    ROOK_TABLE = [
        [  0,   0,   0,   0,   0,   0,   0,   0],
        [  5,  10,  10,  10,  10,  10,  10,   5],
        [ -5,   0,   0,   0,   0,   0,   0,  -5],
        [ -5,   0,   0,   0,   0,   0,   0,  -5],
        [ -5,   0,   0,   0,   0,   0,   0,  -5],
        [ -5,   0,   0,   0,   0,   0,   0,  -5],
        [ -5,   0,   0,   0,   0,   0,   0,  -5],
        [  0,   0,   0,   5,   5,   0,   0,   0]
    ]
    
    QUEEN_TABLE = [
        [-20, -10, -10,  -5,  -5, -10, -10, -20],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-10,   0,   5,   5,   5,   5,   0, -10],
        [ -5,   0,   5,   5,   5,   5,   0,  -5],
        [  0,   0,   5,   5,   5,   5,   0,  -5],
        [-10,   5,   5,   5,   5,   5,   0, -10],
        [-10,   0,   5,   0,   0,   0,   0, -10],
        [-20, -10, -10,  -5,  -5, -10, -10, -20]
    ]
    
    KING_MIDDLEGAME_TABLE = [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [ 20,  20,   0,   0,   0,   0,  20,  20],
        [ 20,  30,  10,   0,   0,  10,  30,  20]
    ]
    
    KING_ENDGAME_TABLE = [
        [-50, -40, -30, -20, -20, -30, -40, -50],
        [-30, -20, -10,   0,   0, -10, -20, -30],
        [-30, -10,  20,  30,  30,  20, -10, -30],
        [-30, -10,  30,  40,  40,  30, -10, -30],
        [-30, -10,  30,  40,  40,  30, -10, -30],
        [-30, -10,  20,  30,  30,  20, -10, -30],
        [-30, -30,   0,   0,   0,   0, -30, -30],
        [-50, -30, -30, -30, -30, -30, -30, -50]
    ]
    
    PIECE_SQUARE_TABLES = {
        chess.PAWN: PAWN_TABLE,
        chess.KNIGHT: KNIGHT_TABLE,
        chess.BISHOP: BISHOP_TABLE,
        chess.ROOK: ROOK_TABLE,
        chess.QUEEN: QUEEN_TABLE,
        chess.KING: KING_MIDDLEGAME_TABLE  # Will be swapped in endgame
    }
    
    def __init__(self):
        pass
    
    def evaluate_position(self, board):
        """
        Evaluate the current position from white's perspective.
        
        Args:
            board (chess.Board): The current board position
            
        Returns:
            int: Evaluation score in centipawns (positive = white advantage)
        """
        if board.is_checkmate():
            return -20000 if board.turn else 20000
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        score = 0
        
        # Material and positional evaluation
        score += self._evaluate_material_and_position(board)
        
        # Mobility evaluation
        score += self._evaluate_mobility(board)
        
        # King safety
        score += self._evaluate_king_safety(board)
        
        # Pawn structure
        score += self._evaluate_pawn_structure(board)
        
        return score
    
    def _evaluate_material_and_position(self, board):
        """Evaluate material count and piece positions."""
        score = 0
        is_endgame = self._is_endgame(board)
        
        for square in range(64):
            piece = board.piece_at(square)
            if piece:
                # Material value
                value = self.PIECE_VALUES[piece.piece_type]
                
                # Positional value
                if piece.piece_type == chess.KING and is_endgame:
                    table = self.KING_ENDGAME_TABLE
                else:
                    table = self.PIECE_SQUARE_TABLES[piece.piece_type]
                
                rank, file = divmod(square, 8)
                if piece.color:  # White
                    positional_value = table[rank][file]
                    score += value + positional_value
                else:  # Black
                    positional_value = table[7-rank][file]
                    score -= value + positional_value
        
        return score
    
    def _evaluate_mobility(self, board):
        """Evaluate piece mobility."""
        original_turn = board.turn
        
        # White mobility
        board.turn = chess.WHITE
        white_moves = len(list(board.legal_moves))
        
        # Black mobility
        board.turn = chess.BLACK
        black_moves = len(list(board.legal_moves))
        
        # Restore original turn
        board.turn = original_turn
        
        return (white_moves - black_moves) * 2
    
    def _evaluate_king_safety(self, board):
        """Evaluate king safety."""
        score = 0
        
        # Check if kings are in check
        if board.is_check():
            score -= 50 if board.turn else -50
        
        # Evaluate castling rights
        if board.has_kingside_castling_rights(chess.WHITE):
            score += 20
        if board.has_queenside_castling_rights(chess.WHITE):
            score += 15
        if board.has_kingside_castling_rights(chess.BLACK):
            score -= 20
        if board.has_queenside_castling_rights(chess.BLACK):
            score -= 15
        
        return score
    
    def _evaluate_pawn_structure(self, board):
        """Evaluate pawn structure."""
        score = 0
        
        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)
        
        # Doubled pawns penalty
        for file in range(8):
            white_pawns_on_file = len([p for p in white_pawns if chess.square_file(p) == file])
            black_pawns_on_file = len([p for p in black_pawns if chess.square_file(p) == file])
            
            if white_pawns_on_file > 1:
                score -= 20 * (white_pawns_on_file - 1)
            if black_pawns_on_file > 1:
                score += 20 * (black_pawns_on_file - 1)
        
        # Isolated pawns penalty
        for pawn in white_pawns:
            file = chess.square_file(pawn)
            has_adjacent_pawn = False
            for adj_file in [file-1, file+1]:
                if 0 <= adj_file <= 7:
                    if any(chess.square_file(p) == adj_file for p in white_pawns):
                        has_adjacent_pawn = True
                        break
            if not has_adjacent_pawn:
                score -= 15
        
        for pawn in black_pawns:
            file = chess.square_file(pawn)
            has_adjacent_pawn = False
            for adj_file in [file-1, file+1]:
                if 0 <= adj_file <= 7:
                    if any(chess.square_file(p) == adj_file for p in black_pawns):
                        has_adjacent_pawn = True
                        break
            if not has_adjacent_pawn:
                score += 15
        
        return score
    
    def _is_endgame(self, board):
        """Determine if the position is in the endgame."""
        # Simple heuristic: endgame if queens are off or limited material
        queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK))
        
        if queens == 0:
            return True
        
        # Count major pieces (rooks, bishops, knights)
        major_pieces = (
            len(board.pieces(chess.ROOK, chess.WHITE)) + 
            len(board.pieces(chess.ROOK, chess.BLACK)) +
            len(board.pieces(chess.BISHOP, chess.WHITE)) + 
            len(board.pieces(chess.BISHOP, chess.BLACK)) +
            len(board.pieces(chess.KNIGHT, chess.WHITE)) + 
            len(board.pieces(chess.KNIGHT, chess.BLACK))
        )
        
        return major_pieces <= 6
