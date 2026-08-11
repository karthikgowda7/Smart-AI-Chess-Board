"""
simulate_game.py - Smart AI Chess Board
Simulates a short game: player makes moves, Stockfish responds.
"""

import sys
import os

# Add project root to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chess_game import ChessGame


def main():
    print("=" * 50)
    print("Smart AI Chess Board - Game Simulation")
    print("=" * 50)
    print()

    game = ChessGame()
    game.start_engine()

    # Simulated player moves
    player_moves = ["e2e4", "d2d4", "g1f3"]

    for i, move_uci in enumerate(player_moves, 1):
        print(f"--- Turn {i} ---")
        print()

        # Player move
        success, message = game.player_move(move_uci)
        if not success:
            print(f"  ERROR: {message}")
            continue
        print(f"  {message}")

        # Show board after player move
        print()
        print(game.get_board_display())
        print()

        # Check if game is over
        if game.is_game_over():
            print("  Game over!")
            break

        # Stockfish responds
        engine_uci, engine_san = game.engine_move()
        print(f"  Stockfish: {engine_san} ({engine_uci})")
        print()
        print(game.get_board_display())
        print()

        # Check if game is over
        if game.is_game_over():
            print("  Game over!")
            break

    # Also demonstrate illegal move rejection
    print("--- Illegal Move Test ---")
    print()
    success, message = game.player_move("e1e5")
    print(f"  Tried 'e1e5': {message}")
    print()

    # Final state
    print("--- Final Board State ---")
    print()
    print(game.get_board_display())
    print(f"  FEN: {game.get_fen()}")
    print()

    game.stop_engine()
    print("Engine shut down cleanly.")
    print()
    print("=" * 50)
    print("Simulation complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
