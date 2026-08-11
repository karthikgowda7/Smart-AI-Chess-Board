"""
chess_game.py - Smart AI Chess Board
Minimal chess game controller using python-chess and Stockfish.
"""

import chess
import chess.engine
from src.config import STOCKFISH_PATH, STOCKFISH_TIME_LIMIT


class ChessGame:
    """Manages a chess game: board state, move validation, and Stockfish responses."""

    def __init__(self):
        self.board = chess.Board()
        self.engine = None

    def start_engine(self):
        """Start the Stockfish engine."""
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    def stop_engine(self):
        """Shut down the Stockfish engine."""
        if self.engine:
            self.engine.quit()
            self.engine = None

    def is_legal_move(self, uci_string):
        """Check if a UCI move string (e.g. 'e2e4') is legal in the current position."""
        try:
            move = chess.Move.from_uci(uci_string)
        except ValueError:
            return False
        return move in self.board.legal_moves

    def player_move(self, uci_string):
        """
        Attempt to play a player move given in UCI format.
        Returns (success, message) tuple.
        """
        try:
            move = chess.Move.from_uci(uci_string)
        except ValueError:
            return False, f"Invalid move format: '{uci_string}'"

        if move not in self.board.legal_moves:
            return False, f"Illegal move: {uci_string}"

        san = self.board.san(move)
        self.board.push(move)
        return True, f"Player: {san} ({uci_string})"

    def engine_move(self):
        """
        Ask Stockfish for the best move and play it.
        Returns (move_uci, move_san) tuple.
        """
        if not self.engine:
            raise RuntimeError("Engine not started. Call start_engine() first.")

        result = self.engine.play(
            self.board, chess.engine.Limit(time=STOCKFISH_TIME_LIMIT)
        )
        move = result.move
        san = self.board.san(move)
        uci = move.uci()
        self.board.push(move)
        return uci, san

    def get_board_display(self):
        """Return a string representation of the current board."""
        return str(self.board)

    def is_game_over(self):
        """Check if the game is over."""
        return self.board.is_game_over()

    def get_fen(self):
        """Return the current board state as a FEN string."""
        return self.board.fen()

    def detect_sensor_move(self, prev_state, curr_state):
        """
        Detect a move from sensor state changes and resolve it using chess logic.
        Handles both normal moves and captures.

        Returns (uci_string, description) or (None, error_description).
        """
        from src.move_detector import detect_move

        result = detect_move(prev_state, curr_state)

        if result["type"] == "normal":
            return result["move"], f"Normal move: {result['move']}"

        elif result["type"] == "capture":
            # Sensor only knows the from_square; use legal moves to find to_square
            from_sq = result["from_square"]
            from_square_idx = chess.parse_square(from_sq)
            legal_captures = [
                m for m in self.board.legal_moves
                if m.from_square == from_square_idx and self.board.is_capture(m)
            ]
            if len(legal_captures) == 1:
                move = legal_captures[0]
                return move.uci(), f"Capture: {move.uci()}"
            elif len(legal_captures) == 0:
                return None, f"No legal capture from {from_sq}"
            else:
                uci_list = [m.uci() for m in legal_captures]
                return None, f"Ambiguous capture from {from_sq}: {uci_list}"

        elif result["type"] == "no_change":
            return None, "No sensor change detected"

        else:
            return None, (
                f"Ambiguous: {len(result['became_empty'])} squares emptied, "
                f"{len(result['became_occupied'])} squares filled"
            )
