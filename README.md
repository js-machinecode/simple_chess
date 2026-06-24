# Simple Chess ♟️

A two-player chess game written in Python featuring a custom-built chess engine and a graphical interface powered by pygame-ce.

---

Installation

Clone the repository:

git clone git@github.com:js-machinecode/simple_chess.git
cd simple_chess

Create and activate a virtual environment:

Windows
python -m venv .venv
.venv\Scripts\activate
Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install pygame-ce
Running the Game
python main.py
Running Tests
python -m unittest test_engine.py

or discover all tests:

python -m unittest discover
Learning Objectives

This project was created to strengthen understanding of:

Object-oriented programming
Software testing
Game development
Chess rules and move validation
State management
Python project organization
Future Improvements
Castling
En passant
Move history
Undo functionality
PGN export
AI opponent
Network multiplayer

---

## Features

- Legal move validation for all standard pieces
- Check detection
- Checkmate detection
- Stalemate detection
- Pawn promotion
- Turn-based gameplay
- Graphical interface using pygame-ce
- Unit test suite for engine functionality

---

## Technologies Used

- Python 3
- pygame-ce
- unittest

---

## Project Structure

```text
simple_chess/
│
├── assets/
│   └── Piece images and game assets
│
├── engine.py
│   └── Chess engine and game logic
│
├── gui.py
│   └── Graphical user interface
│
├── main.py
│   └── Program entry point
│
├── test_engine.py
│   └── Unit tests
│
└── .gitignore




