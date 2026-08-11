"""
simulate_sensor_game.py - Smart AI Chess Board
Full pipeline: simulated sensor states -> move detection -> chess validation -> Stockfish.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chess_game import ChessGame
from src.move_detector import board_to_sensor_state, detect_move


def print_changes(result):
    """Print human-readable description of sensor changes."""
    for sq in result["became_empty"]:
        print(f"    {sq}: occupied -> empty")
    for sq in result["became_occupied"]:
        print(f"    {sq}: empty -> occupied")


def main():
    print("=" * 55)
    print("Smart AI Chess Board - Sensor Pipeline Simulation")
    print("=" * 55)
    print()

    game = ChessGame()
    game.start_engine()

    # Generate initial sensor state from the starting position
    sensor_state = board_to_sensor_state(game.board)

    # --- Turn 1: Player moves pawn e2 -> e4 (normal move) ---
    print("--- Turn 1: Player pawn e2 -> e4 ---")
    print()

    prev_state = dict(sensor_state)
    sensor_state["e2"] = False
    sensor_state["e4"] = True

    result = detect_move(prev_state, sensor_state)
    print("  Sensor changes:")
    print_changes(result)
    print(f"  Detected: type={result['type']}, move={result['move']}")
    print()

    success, msg = game.player_move(result["move"])
    print(f"  python-chess: {msg}")
    print()
    print(game.get_board_display())
    print()

    if not game.is_game_over():
        engine_uci, engine_san = game.engine_move()
        print(f"  Stockfish responds: {engine_san} ({engine_uci})")
        sensor_state = board_to_sensor_state(game.board)
        print()
        print(game.get_board_display())
        print()

    # --- Turn 2: Player moves knight g1 -> f3 (normal move) ---
    print("--- Turn 2: Player knight g1 -> f3 ---")
    print()

    prev_state = dict(sensor_state)
    sensor_state["g1"] = False
    sensor_state["f3"] = True

    result = detect_move(prev_state, sensor_state)
    print("  Sensor changes:")
    print_changes(result)
    print(f"  Detected: type={result['type']}, move={result['move']}")
    print()

    success, msg = game.player_move(result["move"])
    print(f"  python-chess: {msg}")
    print()
    print(game.get_board_display())
    print()

    if not game.is_game_over():
        engine_uci, engine_san = game.engine_move()
        print(f"  Stockfish responds: {engine_san} ({engine_uci})")
        sensor_state = board_to_sensor_state(game.board)
        print()
        print(game.get_board_display())
        print()

    # --- Turn 3: Player pawn d2 -> d4 (via detect_sensor_move bridge) ---
    print("--- Turn 3: Player pawn d2 -> d4 (via detect_sensor_move) ---")
    print()

    prev_state = dict(sensor_state)
    sensor_state["d2"] = False
    sensor_state["d4"] = True

    uci, desc = game.detect_sensor_move(prev_state, sensor_state)
    print(f"  detect_sensor_move: {desc}")

    if uci:
        success, msg = game.player_move(uci)
        print(f"  python-chess: {msg}")
        print()
        print(game.get_board_display())
        print()

        if not game.is_game_over():
            engine_uci, engine_san = game.engine_move()
            print(f"  Stockfish responds: {engine_san} ({engine_uci})")
            sensor_state = board_to_sensor_state(game.board)
            print()
            print(game.get_board_display())
            print()

    # --- No-change test ---
    print("--- No-Change Test ---")
    print()
    prev_state = dict(sensor_state)
    result = detect_move(prev_state, sensor_state)
    print(f"  Same state passed twice: type={result['type']}")
    print()

    # --- Final state ---
    print("--- Final Board ---")
    print()
    print(game.get_board_display())
    print(f"  FEN: {game.get_fen()}")
    print()

    game.stop_engine()
    print("Engine shut down cleanly.")
    print()
    print("=" * 55)
    print("Sensor pipeline simulation complete!")
    print("=" * 55)


if __name__ == "__main__":
    main()
