"""
interactive_game.py - Smart AI Chess Board
Interactive terminal chess game allowing user input against Stockfish.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chess_game import ChessGame


def main():
    print("=" * 55)
    print("  Smart AI Chess Board - Interactive Terminal Game")
    print("=" * 55)
    print("Commands:")
    print("  - Enter move in UCI format (e.g. 'e2e4', 'g1f3')")
    print("  - Type 'fen' to see current FEN string")
    print("  - Type 'board' to reprint the board")
    print("  - Type 'quit' or 'exit' to end the game")
    print("=" * 55)
    print()

    game = ChessGame()
    try:
        print("Starting Stockfish engine...")
        game.start_engine()
        print("Stockfish engine connected!\n")
    except Exception as e:
        print(f"Error starting Stockfish: {e}")
        return

    print("Initial Board Position:")
    print(game.get_board_display())
    print()

    while not game.is_game_over():
        try:
            user_input = input("Your move (White) > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting game...")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Quitting game...")
            break

        if user_input.lower() == "fen":
            print(f"FEN: {game.get_fen()}\n")
            continue

        if user_input.lower() == "board":
            print(game.get_board_display())
            print()
            continue

        # Process player move
        success, message = game.player_move(user_input)
        if not success:
            print(f"  [!] {message}")
            print("  Please enter a valid legal move in UCI format (e.g. 'e2e4').\n")
            continue

        print(f"  ✓ {message}\n")
        print(game.get_board_display())
        print()

        if game.is_game_over():
            print("Game over!")
            break

        # Stockfish response
        print("Stockfish is thinking...")
        engine_uci, engine_san = game.engine_move()
        print(f"  Stockfish (Black) played: {engine_san} ({engine_uci})\n")
        print(game.get_board_display())
        print()

    # Final outcome
    print("=" * 55)
    print("Game summary:")
    print(f"Final FEN: {game.get_fen()}")
    outcome = game.board.outcome()
    if outcome:
        print(f"Result: {outcome.result()} (Termination: {outcome.termination.name})")
    print("=" * 55)

    game.stop_engine()
    print("Engine closed cleanly. Goodbye!")


if __name__ == "__main__":
    main()
