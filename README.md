# Othello — AI Based Game

A desktop Reversi (Othello) game built with Pygame that supports Human vs Human, Human vs AI and AI vs AI modes. Includes three AI algorithms (Greedy, Minimax with Alpha-Beta, and Monte Carlo Tree Search), configurable board sizes and visual/audio assets.

Authors
- Robiul Islam Ryad
- Faruk

Overview
--------
This project is a Pygame implementation of Othello (Reversi). It provides:
- A friendly GUI with menus to choose game mode and board size (4x4, 6x6, 8x8).
- Multiple AI algorithms for different difficulty/behavior.
- Visual animations and audio feedback for moves and UI interactions.
- An option to switch mid-game to watch AI vs AI battles.

Features and explanation
------------------------
- Game Modes
  - Human vs Human: Two players take turns on the same computer.
  - Human vs AI: Play against one of the built-in AIs. You can choose to play white or black and select an AI algorithm.
  - AI vs AI: Watch two algorithms play each other for demonstration or testing.

- Board sizes
  - 4x4, 6x6, 8x8 supported. Default is 8x8. The board initialization and rules adapt to the chosen grid size.

- AI Algorithms
  - Greedy
    - Chooses the move that maximizes immediate heuristic (coin count plus positional value).
    - Fast and simple; suitable for easier difficulty or quick tests.
  - Minimax (with alpha-beta pruning)
    - Recursively searches moves to a limited depth and evaluates positions with a combined coin-count and positional heuristic.
    - Uses alpha-beta pruning to reduce the search space.
    - Balanced play and configurable depth.
  - MCTS (Monte Carlo Tree Search)
    - Builds a search tree using selection, expansion, simulation (random playouts), and backpropagation.
    - Simulations use random playouts (with heuristic evaluation if a depth limit is reached).
    - Controlled by iterations and simulation depth parameters; generally stronger but slower.

- Heuristics & Positioning
  - The game uses a positional weighting function that values corners and edges more than center squares.
  - Heuristics are combined with coin advantage to produce evaluation scores used by Minimax and optionally in playout evaluations.

- Visual & Audio
  - Piece flipping animation.
  - Sound effects on moves and UI interactions.
  - On-screen valid-move hints for human players (can be hidden during AI vs AI).

Configuration (in main_game.py)
-------------------------------
Key constants you may want to tune:
- FPS — game loop frame rate.
- MCTS_ITERATIONS — number of iterations used per MCTS decision (higher → stronger but slower).
- MCTS_SIMULATION_DEPTH — max depth per random playout.
- Minimax depths and cutoffs are set in the minimax call; adjust for strength/performance tradeoffs.
- Assets paths: images under `Image/`, sounds under `music/`.

Installation
------------
1. Ensure Python 3.8+ is installed.
2. Install dependencies:
   - pip install pygame
3. Place required asset folders/files:
   - Image/ (tile and piece images, UI images)
   - music/ (game_music2.mp3, user_move.wav)
   The code includes fallbacks if images are missing but for the intended look include the assets.

Running
-------
From project root:
- python main_game.py

Gameplay Controls
-----------------
- Use the mouse to click menu options and board squares.
- On board: click a highlighted/valid tile to place your piece.
- In menus: click buttons to select mode, colors, and algorithms.
- A "Watch AI Battle" / "Switch to AI vs AI" button lets you convert a human-enabled game into an AI-only match.

Important files & layout
------------------------
- main_game.py — Main application, UI, game loop, AI implementations.
- Image/ — expected images for board, pieces, UI.
- music/ — audio resources.
- README.md — this file.

Notes on AI behavior and tuning
------------------------------
- Greedy: deterministic, very quick.
- Minimax: adjust maximum search depth to control strength and speed. The evaluation is a mix of coin count and positional heuristics.
- MCTS: controlled by MCTS_ITERATIONS and simulation depth. Increase iterations to improve move quality; runtime increases linearly with iterations.
- MCTS uses purely random playouts with a fallback heuristic if depth limits are reached. You can improve playout quality by adding heuristic-guided move selection.

Known issues & tips
-------------------
- Performance: increasing MCTS iterations or Minimax depth will slow down decisions. For smoother gameplay on slower machines, lower those values.
- Assets: if images or music are missing the program will fall back to plain surfaces and still run.
- Valid move hints: shown only for human players by default; AI-vs-AI hides hints to keep visuals clean.

Contributing
------------
- Fork the repository, make changes and open a pull request.
- To add features: prefer modular changes in main_game.py and add supporting modules for complex additions.

License
-------
Include a license of your choice (e.g., MIT). Add LICENSE file if you want to open-source.

Credits
-------
Developed by Robiul Islam Ryad and Faruk.

Contact
-------
For questions or collaboration, add a contact email or open an issue in your source host (GitHub, etc.).
