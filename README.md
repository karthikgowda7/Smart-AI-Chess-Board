# Smart AI Chess Board

Final-year engineering project: A physical chess board with Hall-effect sensors,
ESP32 microcontroller, and AI-powered move recommendations using Stockfish.

DETAILS - 

## Project Status

- [x] Task 1: Development environment setup
- [ ] Task 2: Board-state tracking and move detection
- [ ] Task 3: ESP32 serial communication
- [ ] Task 4: LED control
- [ ] Task 5: Full system integration

## Setup

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run verification
python verify_setup.py
```

## Technology Stack

- Python 3.12
- python-chess
- Stockfish chess engine
- pyserial (for ESP32 communication)
- pytest (testing)
