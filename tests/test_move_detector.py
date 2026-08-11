"""
test_move_detector.py - Smart AI Chess Board
Tests for move detection from sensor states.
"""

import chess
import pytest
from src.move_detector import (
    SQUARE_NAMES,
    board_to_sensor_state,
    detect_changes,
    detect_move,
)
from src.chess_game import ChessGame


# --- Helpers ---

def make_empty_state():
    """All squares empty."""
    return {sq: False for sq in SQUARE_NAMES}


def make_starting_state():
    """Sensor state matching the standard starting position."""
    return board_to_sensor_state(chess.Board())


# --- Tests for board_to_sensor_state ---

class TestBoardToSensorState:

    def test_starting_position_has_32_occupied(self):
        state = make_starting_state()
        occupied = sum(1 for v in state.values() if v)
        assert occupied == 32

    def test_starting_position_has_32_empty(self):
        state = make_starting_state()
        empty = sum(1 for v in state.values() if not v)
        assert empty == 32

    def test_e2_is_occupied_at_start(self):
        state = make_starting_state()
        assert state["e2"] is True

    def test_e4_is_empty_at_start(self):
        state = make_starting_state()
        assert state["e4"] is False


# --- Tests for detect_changes ---

class TestDetectChanges:

    def test_no_changes(self):
        state = make_starting_state()
        became_empty, became_occupied = detect_changes(state, state)
        assert became_empty == []
        assert became_occupied == []

    def test_one_square_emptied(self):
        prev = make_starting_state()
        curr = dict(prev)
        curr["e2"] = False
        became_empty, became_occupied = detect_changes(prev, curr)
        assert became_empty == ["e2"]
        assert became_occupied == []

    def test_one_square_occupied(self):
        prev = make_starting_state()
        curr = dict(prev)
        curr["e4"] = True
        became_empty, became_occupied = detect_changes(prev, curr)
        assert became_empty == []
        assert became_occupied == ["e4"]


# --- Tests for detect_move ---

class TestDetectMoveNormal:
    """Normal moves: 1 square emptied + 1 square occupied."""

    def test_pawn_e2_to_e4(self):
        prev = make_starting_state()
        curr = dict(prev)
        curr["e2"] = False
        curr["e4"] = True

        result = detect_move(prev, curr)
        assert result["type"] == "normal"
        assert result["move"] == "e2e4"
        assert result["from_square"] == "e2"
        assert result["to_square"] == "e4"

    def test_knight_g1_to_f3(self):
        prev = make_starting_state()
        curr = dict(prev)
        curr["g1"] = False
        curr["f3"] = True

        result = detect_move(prev, curr)
        assert result["type"] == "normal"
        assert result["move"] == "g1f3"
        assert result["from_square"] == "g1"
        assert result["to_square"] == "f3"

    def test_pawn_d7_to_d5(self):
        prev = make_starting_state()
        curr = dict(prev)
        curr["d7"] = False
        curr["d5"] = True

        result = detect_move(prev, curr)
        assert result["type"] == "normal"
        assert result["move"] == "d7d5"


class TestDetectMoveCapture:
    """Capture: from_square empties, to_square stays occupied (different piece)."""

    def test_capture_detected(self):
        """
        Simulate a capture: white pawn on e4 takes black pawn on d5.
        Sensor sees: e4 True→False, d5 stays True (occupied by capturing piece).
        """
        # Set up a board with pieces on e4 and d5
        prev = make_empty_state()
        prev["e4"] = True  # white pawn
        prev["d5"] = True  # black pawn

        # After capture: e4 empty, d5 still occupied (now white pawn)
        curr = dict(prev)
        curr["e4"] = False

        result = detect_move(prev, curr)
        assert result["type"] == "capture"
        assert result["from_square"] == "e4"
        assert result["move"] is None  # sensor can't determine to_square


class TestDetectMoveNoChange:
    """No change: same state passed twice."""

    def test_no_change(self):
        state = make_starting_state()
        result = detect_move(state, state)
        assert result["type"] == "no_change"
        assert result["move"] is None

    def test_no_change_empty_board(self):
        state = make_empty_state()
        result = detect_move(state, state)
        assert result["type"] == "no_change"


class TestDetectMoveAmbiguous:
    """Ambiguous: unexpected number of changes."""

    def test_three_squares_changed_is_ambiguous(self):
        prev = make_starting_state()
        curr = dict(prev)
        curr["e2"] = False
        curr["d2"] = False
        curr["e4"] = True

        result = detect_move(prev, curr)
        assert result["type"] == "ambiguous"
        assert result["move"] is None

    def test_two_empty_one_occupied_is_ambiguous(self):
        prev = make_starting_state()
        curr = dict(prev)
        curr["a2"] = False
        curr["b2"] = False
        curr["a4"] = True

        result = detect_move(prev, curr)
        assert result["type"] == "ambiguous"


# --- Tests for detect_sensor_move (ChessGame integration) ---

class TestDetectSensorMove:
    """Tests for the full sensor → chess pipeline."""

    def test_normal_move_through_pipeline(self):
        game = ChessGame()
        prev = board_to_sensor_state(game.board)
        curr = dict(prev)
        curr["e2"] = False
        curr["e4"] = True

        uci, desc = game.detect_sensor_move(prev, curr)
        assert uci == "e2e4"
        assert "Normal" in desc

    def test_capture_resolved_through_pipeline(self):
        """
        Set up a position where e4 pawn can capture d5 pawn,
        then verify the sensor capture is resolved via chess logic.
        """
        game = ChessGame()
        # Set up: 1.e4 d5 → white pawn on e4, black pawn on d5
        game.player_move("e2e4")
        game.player_move("d7d5")

        prev = board_to_sensor_state(game.board)
        # Simulate capture: e4 pawn takes d5 pawn
        curr = dict(prev)
        curr["e4"] = False  # pawn leaves e4
        # d5 stays True (capturing piece now occupies it)

        uci, desc = game.detect_sensor_move(prev, curr)
        assert uci == "e4d5"
        assert "Capture" in desc

    def test_no_change_through_pipeline(self):
        game = ChessGame()
        state = board_to_sensor_state(game.board)
        uci, desc = game.detect_sensor_move(state, state)
        assert uci is None
        assert "No sensor change" in desc
