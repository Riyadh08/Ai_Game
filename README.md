# Reversi Game (Othello) 🎮

**Developed By: Ryad & Faruk**  
*A comprehensive implementation of the classic board game with multiple AI opponents and beautiful UI*

---

## 📋 Table of Contents
- [Features](#-features)
- [Game Modes](#-game-modes)
- [AI Algorithms](#-ai-algorithms)
- [Installation](#-installation)
- [How to Play](#-how-to-play)
- [Screenshots](#-screenshots)
- [Technical Details](#-technical-details)
- [Contributors](#-contributors)

---

## ✨ Features

### 🎯 Multiple Game Modes
- **Human vs Human** - Two players on same device
- **Human vs AI** - Challenge computer opponents
- **AI vs AI** - Watch algorithms battle each other

### 🧠 Smart AI Opponents
- **Greedy Algorithm** 🟢 (Easy) - Immediate gains focus
- **Minimax Algorithm** 🟡 (Medium) - 3-4 moves ahead planning
- **MCTS Algorithm** 🔴 (Hard) - Monte Carlo Tree Search

### 🎨 Beautiful Interface
- Smooth animations and transitions
- Visual move hints and highlights
- Real-time score tracking
- Responsive button designs with hover effects

### 🔊 Immersive Experience
- Background music during gameplay
- Sound effects for moves and clicks
- Piece flipping animations

### ⚙️ Customization
- **Grid Sizes**: 4×4, 6×6, 8×8
- **Player Colors**: Choose black or white
- **Algorithm Selection**: Mix and match AI opponents

---

## 🎮 Game Modes

### Human vs Human
Perfect for two players sharing one device. Take turns placing pieces and outsmart your opponent!

### Human vs AI
Challenge computer opponents with selectable difficulty:
- **Easy**: Greedy algorithm
- **Medium**: Minimax with heuristic evaluation  
- **Hard**: MCTS with 500 iterations per move

### AI vs AI
Watch different algorithms compete! Perfect for learning strategies or enjoying the game passively.

---

## 🧠 AI Algorithms

### Greedy Algorithm
```python
# Chooses move with immediate best score
def greedy_move(board, player):
    valid_moves = get_valid_moves(board, player)
    best_score = -infinity
    for move in valid_moves:
        score = evaluate_move(board, move, player)
        if score > best_score:
            best_move = move
            best_score = score
    return best_move
