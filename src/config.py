"""
config.py - Smart AI Chess Board
Single location for project configuration.
"""

import os

# Project root is one level up from this file (src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STOCKFISH_PATH = os.path.join(
    PROJECT_ROOT, "stockfish", "stockfish",
    "stockfish-windows-x86-64-sse41-popcnt.exe"
)

# Stockfish thinking time in seconds (keep short for fast development)
STOCKFISH_TIME_LIMIT = 0.3
