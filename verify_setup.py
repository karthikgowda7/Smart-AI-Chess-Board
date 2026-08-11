"""
verify_setup.py - Smart AI Chess Board
Development environment verification script.

Verifies:
  1. python-chess imports correctly
  2. A starting board is valid
  3. Stockfish starts and responds via UCI
  4. Stockfish returns a recommended move
"""

import os
import sys
import chess
import chess.engine


def get_stockfish_path():
    """Return the path to the Stockfish executable."""
    # Path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stockfish_path = os.path.join(
        script_dir, "stockfish", "stockfish",
        "stockfish-windows-x86-64-sse41-popcnt.exe"
    )
    if not os.path.isfile(stockfish_path):
        print(f"ERROR: Stockfish not found at: {stockfish_path}")
        sys.exit(1)
    return stockfish_path


def main():
    print("=" * 50)
    print("Smart AI Chess Board - Setup Verification")
    print("=" * 50)
    print()

    # Step 1: Verify python-chess
    print(f"[1] python-chess version: {chess.__version__}")
    print("    OK - python-chess imported successfully")
    print()

    # Step 2: Create and validate a starting board
    board = chess.Board()
    print("[2] Starting board created:")
    print(board)
    print()
    assert board.is_valid(), "Board is not valid!"
    print("    OK - Board is valid")
    print(f"    FEN: {board.fen()}")
    print()

    # Step 3: Start Stockfish via UCI
    stockfish_path = get_stockfish_path()
    print(f"[3] Starting Stockfish from: {stockfish_path}")
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    print(f"    OK - Stockfish started successfully")
    print(f"    Engine: {engine.id.get('name', 'unknown')}")
    print()

    # Step 4: Ask Stockfish for a move
    print("[4] Asking Stockfish for best move from starting position...")
    result = engine.play(board, chess.engine.Limit(time=2.0))
    best_move = result.move
    print(f"    Recommended move: {best_move}")
    print(f"    Move in SAN: {board.san(best_move)}")
    print()

    # Step 5: Clean shutdown
    engine.quit()
    print("[5] Stockfish shut down cleanly")
    print()

    print("=" * 50)
    print("ALL CHECKS PASSED - Environment is ready!")
    print("=" * 50)


if __name__ == "__main__":
    main()
