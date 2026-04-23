# FAI-Group5 — Peg Game Portal

Foundations of Artificial Intelligence (AI801, Spring 2026) — Group 5.

This project includes:
- **Peg Solitaire** (single-player puzzle) solved via AI search algorithms (DFS, Greedy Best-First, A*, Bidirectional A*, MCTS).
- **Peg Duotaire** (two-player impartial game variant) playable as AI vs AI or Human vs AI (GUI supports human play on the English board).
- **Visualization** of solution/game state progress using Matplotlib.

## Requirements

- **Python**: 3.10+ recommended
- **Core packages**:
  - `matplotlib` (visualizations for both CLI and GUI launches)
  - `pygame` (GUI mode)
  - `pympler` (used by the “data structure memory/performance” test)

## Install

From the project folder:

```bash
python -m pip install --upgrade pip
python -m pip install matplotlib pygame
python -m pip install pympler
```


## Run (CLI)

Launch the command-line menu:

```bash
python main.py
```

You’ll be prompted to select one of the following:
- **Simulate Peg Solitaire**
  - Choose a **board**: Triangle (15), English (33), or French (37)
  - Choose a **search algorithm**: DFS, Greedy BFS, A*, Bidirectional A*, or MCTS
  - The program runs the search and then opens a Matplotlib window that visualizes the board states.
- **Simulate Peg Duotaire**
  - Choose a **board**: Triangle, English, or French
  - Choose **Player 1** and **Player 2**: Random, AlphaBeta, MCTS, or User (CLI user player)
  - The program plays the game and visualizes the move-by-move state sequence.
- **Run Test Bench**
  - Search algorithm performance comparisons
  - Duotaire matchup experiments (plots win counts)
  - Data structure comparison 
  - Direction-order comparisons for DFS
- **User Plays Peg Duotaire**
  - Lets you play against a selected AI opponent (text/terminal interaction)

## Run (GUI)

Launch the graphical menu (Pygame):

```bash
python main.py --gui
or
python gui.py
```

From the GUI you can:
- **Peg Solitaire**: pick a board + algorithm, then run and visualize results.
- **Peg Duotaire**: pick a board + players.
  - **Interactive human play is only supported on the English board** in the GUI.
  - If you choose AI vs AI, the game will run and the state sequence will be visualized.


## Notes / troubleshooting

- **Matplotlib windows**: visualizations open in separate windows; close the window to continue/exit cleanly.
- **Long runs**: DFS on the French board can take a long time; the GUI shows a warning before starting that configuration.
