"""
test_chess_game.py - Smart AI Chess Board
Pytest tests for the chess game controller.
"""

import chess
import pytest
from src.chess_game import ChessGame


class TestBoardSetup:
    """Tests for initial board state."""

    def test_starting_board_is_valid(self):
        game = ChessGame()
        assert game.board.is_valid()

    def test_starting_fen_is_standard(self):
        game = ChessGame()
        assert game.get_fen() == chess.STARTING_FEN


class TestMoveValidation:
    """Tests for move validation without engine."""

    def test_legal_move_e2e4_is_accepted(self):
        game = ChessGame()
        assert game.is_legal_move("e2e4") is True

    def test_legal_move_d2d4_is_accepted(self):
        game = ChessGame()
        assert game.is_legal_move("d2d4") is True

    def test_illegal_move_e1e5_is_rejected(self):
        game = ChessGame()
        assert game.is_legal_move("e1e5") is False

    def test_nonsense_move_is_rejected(self):
        game = ChessGame()
        assert game.is_legal_move("z9z9") is False

    def test_empty_string_is_rejected(self):
        game = ChessGame()
        assert game.is_legal_move("") is False


class TestPlayerMove:
    """Tests for making player moves."""

    def test_legal_move_returns_success(self):
        game = ChessGame()
        success, message = game.player_move("e2e4")
        assert success is True
        assert "e4" in message

    def test_illegal_move_returns_failure(self):
        game = ChessGame()
        success, message = game.player_move("e1e5")
        assert success is False
        assert "Illegal" in message

    def test_invalid_format_returns_failure(self):
        game = ChessGame()
        success, message = game.player_move("xyz")
        assert success is False

    def test_legal_move_updates_board(self):
        game = ChessGame()
        game.player_move("e2e4")
        # After e2e4, the pawn should be on e4, not e2
        assert game.board.piece_at(chess.E4) == chess.Piece(chess.PAWN, chess.WHITE)
        assert game.board.piece_at(chess.E2) is None

    def test_legal_move_changes_turn(self):
        game = ChessGame()
        assert game.board.turn == chess.WHITE
        game.player_move("e2e4")
        assert game.board.turn == chess.BLACK

    def test_illegal_move_does_not_change_board(self):
        game = ChessGame()
        fen_before = game.get_fen()
        game.player_move("e1e5")
        assert game.get_fen() == fen_before


class TestEngineIntegration:
    """Tests that require Stockfish. Grouped so the engine is started once."""

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        self.game = ChessGame()
        self.game.start_engine()
        yield
        self.game.stop_engine()

    def test_engine_responds_with_move(self):
        self.game.player_move("e2e4")
        uci, san = self.game.engine_move()
        assert len(uci) >= 4  # e.g. "e7e5"
        assert len(san) >= 2  # e.g. "e5"

    def test_engine_move_updates_board(self):
        self.game.player_move("e2e4")
        fen_before = self.game.get_fen()
        self.game.engine_move()
        assert self.game.get_fen() != fen_before

    def test_engine_move_returns_to_white_turn(self):
        self.game.player_move("e2e4")  # white plays
        self.game.engine_move()  # black plays
        assert self.game.board.turn == chess.WHITE
