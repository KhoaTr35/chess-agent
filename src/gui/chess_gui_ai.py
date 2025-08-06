import pygame
import chess
import sys
import os
import threading
import time

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from board.board_state import BoardState
from agent.chess_agent import ChessAgent, RandomAgent, AggressiveAgent

class ChessGUIWithAI:
    def __init__(self, ai_enabled=False, ai_difficulty='medium', ai_color=chess.BLACK):
        pygame.init()
        
        # Constants
        self.BOARD_SIZE = 640
        self.SQUARE_SIZE = self.BOARD_SIZE // 8
        self.LIGHT_COLOR = (240, 217, 181)  # Light brown
        self.DARK_COLOR = (181, 136, 99)    # Dark brown
        self.HIGHLIGHT_COLOR = (255, 255, 0, 128)  # Yellow with transparency
        self.SELECTED_COLOR = (0, 255, 0, 128)     # Green with transparency
        self.AI_MOVE_COLOR = (255, 0, 0, 128)      # Red for AI moves
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.BOARD_SIZE, self.BOARD_SIZE + 150))
        pygame.display.set_caption("Chess Game with AI")
        
        # Game state
        self.board_state = BoardState()
        self.selected_square = None
        self.highlighted_moves = []
        self.last_move = None
        
        # AI settings
        self.ai_enabled = ai_enabled
        self.ai_color = ai_color
        self.ai_agent = None
        self.ai_thinking = False
        self.ai_move_suggestion = None
        
        if self.ai_enabled:
            self.ai_agent = ChessAgent(ai_difficulty, ai_color)
        
        # Load chess piece images
        self.load_piece_images()
        
        # Fonts for displaying game info
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 32)
        
        # Game mode
        self.game_mode = "AI vs Human" if ai_enabled else "Human vs Human"
        
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
        
        # Highlight last move
        if self.last_move:
            for square in [self.last_move.from_square, self.last_move.to_square]:
                x, y = self.square_to_coords(square)
                highlight_surface.fill(self.AI_MOVE_COLOR)
                self.screen.blit(highlight_surface, (x, y))
        
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
        
        # Game mode
        mode_text = self.title_font.render(f"Mode: {self.game_mode}", True, (0, 0, 0))
        self.screen.blit(mode_text, (10, y_offset))
        
        # Current player
        current_player = "White" if self.board_state.board.turn else "Black"
        player_text = self.font.render(f"Current Player: {current_player}", True, (0, 0, 0))
        self.screen.blit(player_text, (10, y_offset + 35))
        
        # AI status
        if self.ai_enabled:
            ai_color_name = "White" if self.ai_color else "Black"
            ai_text = self.font.render(f"AI: {ai_color_name} ({self.ai_agent.difficulty})", True, (0, 0, 0))
            self.screen.blit(ai_text, (200, y_offset + 35))
            
            if self.ai_thinking:
                thinking_text = self.font.render("AI is thinking...", True, (255, 0, 0))
                self.screen.blit(thinking_text, (400, y_offset + 35))
        
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
        self.screen.blit(status_text, (10, y_offset + 60))
        
        # Controls
        controls = [
            "R: Reset  |  U: Undo  |  A: Toggle AI  |  1-4: AI Difficulty  |  C: AI Color"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.font.render(control, True, (100, 100, 100))
            self.screen.blit(control_text, (10, y_offset + 85 + i * 20))
    
    def handle_square_click(self, clicked_square):
        """Handle clicking on a square."""
        if clicked_square is None or self.ai_thinking:
            return
        
        # If it's AI's turn, don't allow human moves
        if self.ai_enabled and self.board_state.board.turn == self.ai_color:
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
                self.last_move = move
                self.selected_square = None
                self.highlighted_moves = []
                
                # Trigger AI move if needed
                if self.ai_enabled and not self.board_state.is_game_over():
                    self.trigger_ai_move()
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
    
    def trigger_ai_move(self):
        """Trigger AI to make a move in a separate thread."""
        if not self.ai_enabled or self.ai_thinking or self.board_state.is_game_over():
            return
        
        if self.board_state.board.turn == self.ai_color:
            self.ai_thinking = True
            thread = threading.Thread(target=self.make_ai_move)
            thread.daemon = True
            thread.start()
    
    def make_ai_move(self):
        """Make an AI move (runs in separate thread)."""
        try:
            ai_move = self.ai_agent.get_best_move(self.board_state.board)
            if ai_move:
                # Small delay to show AI is thinking
                time.sleep(0.5)
                
                # Make the move
                if self.board_state.make_move(ai_move):
                    self.last_move = ai_move
                    self.selected_square = None
                    self.highlighted_moves = []
        except Exception as e:
            print(f"AI move error: {e}")
        finally:
            self.ai_thinking = False
    
    def toggle_ai(self):
        """Toggle AI on/off."""
        self.ai_enabled = not self.ai_enabled
        if self.ai_enabled and not self.ai_agent:
            self.ai_agent = ChessAgent('medium', self.ai_color)
        
        self.game_mode = "AI vs Human" if self.ai_enabled else "Human vs Human"
        
        # Trigger AI move if it's AI's turn
        if self.ai_enabled:
            self.trigger_ai_move()
    
    def change_ai_difficulty(self, difficulty):
        """Change AI difficulty."""
        if self.ai_enabled:
            self.ai_agent = ChessAgent(difficulty, self.ai_color)
    
    def toggle_ai_color(self):
        """Toggle AI color between white and black."""
        if self.ai_enabled:
            self.ai_color = not self.ai_color
            self.ai_agent = ChessAgent(self.ai_agent.difficulty, self.ai_color)
            self.trigger_ai_move()
    
    def reset_game(self):
        """Reset the game."""
        self.board_state.reset()
        self.selected_square = None
        self.highlighted_moves = []
        self.last_move = None
        self.ai_thinking = False
        
        # Trigger AI move if AI plays white
        if self.ai_enabled and self.ai_color == chess.WHITE:
            self.trigger_ai_move()
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True
        
        # Trigger AI move if AI plays white
        if self.ai_enabled and self.ai_color == chess.WHITE:
            self.trigger_ai_move()
        
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
                    if event.key == pygame.K_r:  # Reset game
                        self.reset_game()
                    elif event.key == pygame.K_u:  # Undo move
                        self.board_state.undo_move()
                        self.selected_square = None
                        self.highlighted_moves = []
                        self.last_move = None
                    elif event.key == pygame.K_a:  # Toggle AI
                        self.toggle_ai()
                    elif event.key == pygame.K_c:  # Toggle AI color
                        self.toggle_ai_color()
                    elif event.key == pygame.K_1:  # Easy difficulty
                        self.change_ai_difficulty('easy')
                    elif event.key == pygame.K_2:  # Medium difficulty
                        self.change_ai_difficulty('medium')
                    elif event.key == pygame.K_3:  # Hard difficulty
                        self.change_ai_difficulty('hard')
                    elif event.key == pygame.K_4:  # Expert difficulty
                        self.change_ai_difficulty('expert')
            
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

# Backward compatibility with original ChessGUI
class ChessGUI(ChessGUIWithAI):
    def __init__(self):
        super().__init__(ai_enabled=False)

if __name__ == "__main__":
    # Run with AI enabled by default
    game = ChessGUIWithAI(ai_enabled=True, ai_difficulty='medium', ai_color=chess.BLACK)
    game.run()
