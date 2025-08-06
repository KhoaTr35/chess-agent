import pygame
import chess
import sys
import os

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from board.board_state import BoardState

class ChessGUI:
    def __init__(self):
        pygame.init()
        
        # Constants
        self.BOARD_SIZE = 640
        self.SQUARE_SIZE = self.BOARD_SIZE // 8
        self.LIGHT_COLOR = (240, 217, 181)  # Light brown
        self.DARK_COLOR = (181, 136, 99)    # Dark brown
        self.HIGHLIGHT_COLOR = (255, 255, 0, 128)  # Yellow with transparency
        self.SELECTED_COLOR = (0, 255, 0, 128)     # Green with transparency
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.BOARD_SIZE, self.BOARD_SIZE + 100))
        pygame.display.set_caption("Chess Game")
        
        # Game state
        self.board_state = BoardState()
        self.selected_square = None
        self.highlighted_moves = []
        
        # Load chess piece images
        self.load_piece_images()
        
        # Font for displaying game info
        self.font = pygame.font.Font(None, 36)
        
    def load_piece_images(self):
        """Load chess piece images. For now, we'll use text representation."""
        self.piece_symbols = {
            chess.PAWN: {'white': '♙', 'black': '♟'},
            chess.ROOK: {'white': '♖', 'black': '♜'},
            chess.KNIGHT: {'white': '♘', 'black': '♞'},
            chess.BISHOP: {'white': '♗', 'black': '♝'},
            chess.QUEEN: {'white': '♕', 'black': '♛'},
            chess.KING: {'white': '♔', 'black': '♚'}
        }
        
        # Create font for pieces
        self.piece_font = pygame.font.Font(None, 48)
        
    def square_to_coords(self, square):
        """Convert chess square (0-63) to screen coordinates."""
        file = square % 8
        rank = 7 - (square // 8)  # Flip rank for display
        x = file * self.SQUARE_SIZE
        y = rank * self.SQUARE_SIZE
        return x, y
    
    def coords_to_square(self, x, y):
        """Convert screen coordinates to chess square (0-63)."""
        if x < 0 or x >= self.BOARD_SIZE or y < 0 or y >= self.BOARD_SIZE:
            return None
        file = x // self.SQUARE_SIZE
        rank = 7 - (y // self.SQUARE_SIZE)  # Flip rank
        return rank * 8 + file
    
    def draw_board(self):
        """Draw the chess board."""
        for rank in range(8):
            for file in range(8):
                x = file * self.SQUARE_SIZE
                y = rank * self.SQUARE_SIZE
                
                # Determine square color
                if (rank + file) % 2 == 0:
                    color = self.LIGHT_COLOR
                else:
                    color = self.DARK_COLOR
                
                pygame.draw.rect(self.screen, color, 
                               (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))
    
    def draw_highlights(self):
        """Draw highlights for selected square and possible moves."""
        # Create a surface with alpha for transparency
        highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
        
        # Highlight selected square
        if self.selected_square is not None:
            x, y = self.square_to_coords(self.selected_square)
            highlight_surface.fill(self.SELECTED_COLOR)
            self.screen.blit(highlight_surface, (x, y))
        
        # Highlight possible moves
        for move_square in self.highlighted_moves:
            x, y = self.square_to_coords(move_square)
            highlight_surface.fill(self.HIGHLIGHT_COLOR)
            self.screen.blit(highlight_surface, (x, y))
    
    def draw_pieces(self):
        """Draw chess pieces on the board."""
        for square in range(64):
            piece = self.board_state.board.piece_at(square)
            if piece:
                x, y = self.square_to_coords(square)
                color = 'white' if piece.color else 'black'
                symbol = self.piece_symbols[piece.piece_type][color]
                
                # Render piece symbol
                piece_surface = self.piece_font.render(symbol, True, (0, 0, 0))
                piece_rect = piece_surface.get_rect()
                piece_rect.center = (x + self.SQUARE_SIZE // 2, y + self.SQUARE_SIZE // 2)
                self.screen.blit(piece_surface, piece_rect)
    
    def draw_game_info(self):
        """Draw game information below the board."""
        y_offset = self.BOARD_SIZE + 10
        
        # Current player
        current_player = "White" if self.board_state.board.turn else "Black"
        player_text = self.font.render(f"Current Player: {current_player}", True, (0, 0, 0))
        self.screen.blit(player_text, (10, y_offset))
        
        # Game status
        if self.board_state.is_game_over():
            result = self.board_state.get_result()
            if result == "1-0":
                status = "White Wins!"
            elif result == "0-1":
                status = "Black Wins!"
            else:
                status = "Draw!"
        else:
            if self.board_state.board.is_check():
                status = "Check!"
            else:
                status = "In Progress"
        
        status_text = self.font.render(f"Status: {status}", True, (0, 0, 0))
        self.screen.blit(status_text, (10, y_offset + 30))
    
    def handle_square_click(self, clicked_square):
        """Handle clicking on a square."""
        if clicked_square is None:
            return
        
        # If no square is selected, select this square (if it has a piece of current player)
        if self.selected_square is None:
            piece = self.board_state.board.piece_at(clicked_square)
            if piece and piece.color == self.board_state.board.turn:
                self.selected_square = clicked_square
                # Get legal moves from this square
                self.highlighted_moves = []
                for move in self.board_state.get_legal_moves():
                    if move.from_square == clicked_square:
                        self.highlighted_moves.append(move.to_square)
        else:
            # Try to make a move from selected square to clicked square
            move = chess.Move(self.selected_square, clicked_square)
            
            # Check for promotion (simplified - always promote to queen)
            piece = self.board_state.board.piece_at(self.selected_square)
            if (piece and piece.piece_type == chess.PAWN and 
                ((piece.color and clicked_square >= 56) or (not piece.color and clicked_square <= 7))):
                move.promotion = chess.QUEEN
            
            if self.board_state.make_move(move):
                # Move was successful
                self.selected_square = None
                self.highlighted_moves = []
            else:
                # Invalid move, select new square if it has a piece of current player
                piece = self.board_state.board.piece_at(clicked_square)
                if piece and piece.color == self.board_state.board.turn:
                    self.selected_square = clicked_square
                    # Get legal moves from this square
                    self.highlighted_moves = []
                    for move in self.board_state.get_legal_moves():
                        if move.from_square == clicked_square:
                            self.highlighted_moves.append(move.to_square)
                else:
                    self.selected_square = None
                    self.highlighted_moves = []
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        x, y = event.pos
                        clicked_square = self.coords_to_square(x, y)
                        self.handle_square_click(clicked_square)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reset game with 'R' key
                        self.board_state.reset()
                        self.selected_square = None
                        self.highlighted_moves = []
                    elif event.key == pygame.K_u:  # Undo move with 'U' key
                        self.board_state.undo_move()
                        self.selected_square = None
                        self.highlighted_moves = []
            
            # Clear screen
            self.screen.fill((255, 255, 255))
            
            # Draw everything
            self.draw_board()
            self.draw_highlights()
            self.draw_pieces()
            self.draw_game_info()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = ChessGUI()
    game.run()
