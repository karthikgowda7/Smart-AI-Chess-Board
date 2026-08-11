"""
move_detector.py - Smart AI Chess Board
Detects chess moves by comparing physical board sensor states.

Sensor state: dict mapping square names ("a1" through "h8") to bool.
  True  = piece physically present on that square
  False = square is empty

The core detection logic (detect_changes, detect_move) works purely
on sensor booleans — no chess rules needed. The helper function
board_to_sensor_state bridges between python-chess and the sensor layer.
"""

import chess


# All 64 square names in standard chess order (a1, b1, ..., h1, a2, ..., h8)
SQUARE_NAMES = [chess.square_name(i) for i in range(64)]


def board_to_sensor_state(board):
    """
    Convert a python-chess Board to a sensor state dict.
    This is the bridge between the chess logic layer and the sensor layer.
    """
    return {
        chess.square_name(sq): board.piece_at(sq) is not None
        for sq in range(64)
    }


def detect_changes(prev_state, curr_state):
    """
    Compare two sensor states and find which squares changed.

    Returns:
        (became_empty, became_occupied)
        became_empty:    squares that went True → False (piece lifted)
        became_occupied: squares that went False → True (piece placed)
    """
    became_empty = []
    became_occupied = []

    for square in SQUARE_NAMES:
        was_occupied = prev_state[square]
        is_occupied = curr_state[square]

        if was_occupied and not is_occupied:
            became_empty.append(square)
        elif not was_occupied and is_occupied:
            became_occupied.append(square)

    return became_empty, became_occupied


def detect_move(prev_state, curr_state):
    """
    Detect a chess move from the difference between two sensor states.

    Returns a dict:
        "type":            "normal" | "capture" | "no_change" | "ambiguous"
        "move":            UCI string (e.g. "e2e4") or None
        "from_square":     square the piece left, or None
        "to_square":       square the piece arrived at, or None
        "became_empty":    list of squares that lost a piece
        "became_occupied": list of squares that gained a piece

    Move types:
        normal   — 1 square emptied + 1 square filled  → full UCI move
        capture  — 1 square emptied + 0 squares filled  → from_square known,
                   to_square needs chess logic to resolve
        no_change — nothing changed
        ambiguous — unexpected number of changes
    """
    became_empty, became_occupied = detect_changes(prev_state, curr_state)

    result = {
        "type": "no_change",
        "move": None,
        "from_square": None,
        "to_square": None,
        "became_empty": became_empty,
        "became_occupied": became_occupied,
    }

    if not became_empty and not became_occupied:
        result["type"] = "no_change"

    elif len(became_empty) == 1 and len(became_occupied) == 1:
        # Normal move: piece left one square, arrived at another
        from_sq = became_empty[0]
        to_sq = became_occupied[0]
        result["type"] = "normal"
        result["move"] = from_sq + to_sq
        result["from_square"] = from_sq
        result["to_square"] = to_sq

    elif len(became_empty) == 1 and len(became_occupied) == 0:
        # Capture: piece left from_square, landed on an already-occupied square.
        # Sensor can't tell which occupied square — needs chess logic.
        result["type"] = "capture"
        result["from_square"] = became_empty[0]

    else:
        result["type"] = "ambiguous"

    return result
