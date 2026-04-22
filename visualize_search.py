#!/usr/bin/env python3

import math
import matplotlib.pyplot as plt

# def visualize_search_matlab(searchType: int):
def visualize_search_matlab(searchType, timeTaken, pathStates):

    """ Visualize the peg solitaire search results using MATLAB-style plots.
    Returns time taken, path states, and solution for further analysis.
    """
    # Function-local import avoids circular imports at module load:
    from utils import SEARCH_ALGORITHMS
    search_names = {k: v['short_name'] for k, v in SEARCH_ALGORITHMS.items()}
    # timeTaken, pathStates, solution = play_peg_solitaire(searchType, test=True, visualize=True)

    if not pathStates:
        print("No solution found!")
        return

    print(f"\nVisualization for {search_names.get(searchType)}")
    print(f"Total steps: {len(pathStates)}")
    print(f"Time taken: {timeTaken:.2f} milliseconds")

    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

    # Search progress over time (steps)
    steps = range(len(pathStates))
    peg_counts = [state.state.bit_count() for state in pathStates]

    ax1.plot(steps, peg_counts, 'b-o', linewidth=2, markersize=4)
    ax1.set_xlabel('Search Steps')
    ax1.set_ylabel('Number of Pegs Remaining')
    ax1.set_title(f'Peg Reduction Over Search Steps ({search_names.get(searchType)})')
    ax1.grid(True, alpha=0.3)

    # Search tree exploration (if available)
    #
    ax2.scatter(steps, peg_counts, c=steps, cmap='viridis', s=50, alpha=0.7)
    ax2.plot(steps, peg_counts, 'r--', alpha=0.5)
    ax2.set_xlabel('Search Steps')
    ax2.set_ylabel('Number of Pegs Remaining')
    ax2.set_title('Search Tree Exploration')
    ax2.grid(True, alpha=0.3)

    # Board state visualization at key points
    key_steps = [0, len(pathStates)//4, len(pathStates)//2, 3*len(pathStates)//4, len(pathStates)-1]
    key_steps = list(set(key_steps))  # Remove duplicates

    colors = ['red', 'orange', 'yellow', 'green', 'blue']
    for i, step_idx in enumerate(key_steps):
        if step_idx < len(pathStates):
            peg_count = pathStates[step_idx].state.bit_count()
            ax3.bar(step_idx, peg_count, color=colors[i % len(colors)],
                   label=f'Step {step_idx}', alpha=0.7)

    ax3.set_xlabel('Step Number')
    ax3.set_ylabel('Pegs Remaining')
    ax3.set_title('Key Search Steps Analysis')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Solution path cost analysis
    # if hasattr(solution, 'path_cost'):
    #     # show path info if available
    #     path_costs = []
    #     current_cost = 0
    #     for i, state in enumerate(pathStates):
    #         path_costs.append(current_cost)
    #         if i < len(pathStates) - 1:
    #             current_cost += 1  # Each move costs 1
    #
    #     ax4.plot(steps, path_costs, 'g-s', linewidth=2, markersize=4)
    #     ax4.set_xlabel('Search Steps')
    #     ax4.set_ylabel('Path Cost')
    #     ax4.set_title('Cumulative Path Cost')
    #     ax4.grid(True, alpha=0.3)
    # else:
    #     # Alternative: show peg reduction rate
    #     peg_reduction_rate = []
    #     for i in range(1, len(peg_counts)):
    #         rate = peg_counts[i-1] - peg_counts[i]
    #         peg_reduction_rate.append(rate)
    #
    #     ax4.plot(range(1, len(peg_counts)), peg_reduction_rate, 'm-^', linewidth=2, markersize=4)
    #     ax4.set_xlabel('Search Steps')
    #     ax4.set_ylabel('Pegs Removed per Step')
    #     ax4.set_title('Peg Removal Rate')
    #     ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # return timeTaken, pathStates, solution

def plot_board_states(pathStates, max_states=2, duo=False, player1=None, player2=None):
    # Plot actual board states at different steps using ASCII-like visualization.
    def _format_board_for_display(state):
        board_str = str(state)
        # Use circle glyphs for display only (do not change game-state encoding).
        board_str = board_str.replace("X", "●").replace("O", "○")
        if "Triangle" not in type(state).__name__:
            return board_str

        # Rows from __repr__ are left-aligned in a fixed grid with trailing spaces.
        # Strip trailing padding, then center each row in the base width so the triangle is centered.
        trimmed = [line.rstrip() for line in board_str.splitlines()] #strip all trailing spaces from each line
        max_width = max((len(line) for line in trimmed), default=0)  #find max of all lines, or default to 0
        centered = [line.center(max_width) for line in trimmed]  #center all lines, .center pads both sides of line to max with.
        return "\n".join(centered)
    
    if not pathStates:
        print("No states to visualize!")
        return

    # Select key states to show
    n_states = len(pathStates)
    #indices = np.linspace(0, len(pathStates)-1, n_states, dtype=int)
    indices = range(0, n_states)

    n_cols = 4
    n_rows = math.ceil(n_states / n_cols)

    # Keep the overall figure at a 16:9 aspect ratio. to fit laptop screen
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 9))
    axes = axes.flatten()
    if n_states == 1:
        axes = [axes]

    for i, idx in enumerate(indices):

        state = pathStates[idx]
        board_str = _format_board_for_display(state)

        # Clear the axis
        axes[i].clear()
        axes[i].axis('off')
        if i == 0:
            axes[i].set_title('Initial State')
        else:
            if not duo:
                axes[i].set_title(f'Step {idx}')
            else:
                if idx % 2 == 1:
                    player_name = 'Player 1:' + player1
                else:
                    player_name = 'Player 2:' + player2
                axes[i].set_title(player_name)

        # Display the board as text
        axes[i].text(0.5, 0.5, board_str,
                    transform=axes[i].transAxes,
                    fontsize=8,
                    verticalalignment='center',
                    horizontalalignment='center',
                    fontfamily='monospace')
        
    #len(axes) is a little too big, so ignore the extra ones
    for extra_indices in range(len(indices), len(axes)):
            axes[extra_indices].axis('off')

    #Detect if game is over and display winner
    if duo and player1 and player2 and hasattr(pathStates[-1], "to_move"):
        loser = pathStates[-1].to_move
        winner = "O" if loser == "X" else "X"
        winner_name = f'Player 1:{player1}' if winner == "X" else f'Player 2:{player2}'
        
        fig.text(
            0.5,
            0.02,
            f"Winner: ({winner_name})",
            ha="center",
            va="bottom",
            fontsize=14,
            fontweight="bold",
        )
        plt.tight_layout(rect=[0, 0.05, 1, 1])
    else: #playing a solitaire game
        plt.tight_layout() #just display the results
    plt.show()

def compare_search_algorithms(results):
    #Compare different search algorithms using MATLAB-style plots.
    
    # algorithms = list(SEARCH_ALGORITHMS.keys())  # Use all available algorithms
    # results = {}
    #
    # for alg in algorithms:
    #     print(f"Running {search_names.get(alg)}...")
    #     try:
    #         time_taken, path_states, solution = play_peg_solitaire(alg, test=True, visualize=True)
    #         results[alg] = {
    #             'time': time_taken,
    #             'steps': len(path_states),
    #             'pegs_remaining': path_states[-1].state.bit_count() if path_states else 0
    #         }
    #     except Exception as e:
    #         print(f"Error with {search_names.get(alg)}: {e}")
    #         results[alg] = {'time': float('inf'), 'steps': float('inf'), 'pegs_remaining': float('inf')}

    # Create comparison plots
    fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(2, 4, figsize=(20, 10))

    plot_one_searcher('A*', results, ax1, ax5)
    plot_one_board('Triangle', results, ax2, ax6)
    plot_one_board('English', results, ax3, ax7)
    plot_one_board('French', results, ax4, ax8)

    # alg_names = [SEARCH_ALGORITHMS[alg]['short_name'] for alg in algorithms]

    # Time comparison
    # times = [results[alg]['time'] for alg in algorithms]
    # ax1.bar(alg_names, times, color='skyblue')
    # ax1.set_ylabel('Time (seconds)')
    # ax1.set_title('Search Time Comparison')
    # ax1.tick_params(axis='x', rotation=45)

    # Steps comparison
    # steps = [results[alg]['steps'] for alg in algorithms]
    # ax2.bar(alg_names, steps, color='lightgreen')
    # ax2.set_ylabel('Number of Steps')
    # ax2.set_title('Solution Steps Comparison')
    # ax2.tick_params(axis='x', rotation=45)

    # Final pegs comparison
    # pegs = [results[alg]['pegs_remaining'] for alg in algorithms]
    # ax3.bar(alg_names, pegs, color='salmon')
    # ax3.set_ylabel('Final Pegs Remaining')
    # ax3.set_title('Solution Quality (Lower is Better)')
    # ax3.tick_params(axis='x', rotation=45)

    # Efficiency plot (steps vs time)
    # ax4.scatter(times, steps, s=100, c=range(len(algorithms)), cmap='viridis')
    # for i, alg in enumerate(algorithms):
    #     ax4.annotate(search_names.get(alg), (times[i], steps[i]),
    #                 xytext=(5, 5), textcoords='offset points')
    # ax4.set_xlabel('Time (seconds)')
    # ax4.set_ylabel('Steps')
    # ax4.set_title('Efficiency: Time vs Steps')
    # ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return results


def plot_duotaire_results(results, title="Peg Duotaire results"):
    """Plot duotaire win counts.
    `results` format: {(shape, p1_name, p2_name): [p1_wins, p2_wins], ...}
    """
    if not results:
        print("No results to plot.")
        return

    # Group by board shape
    shapes = sorted({k[0] for k in results.keys()})
    fig, axes = plt.subplots(len(shapes), 1, figsize=(12, 4 * len(shapes)), sharex=False)
    if len(shapes) == 1:
        axes = [axes]

    # If trials are consistent, show once as a footer note.
    any_wins = next(iter(results.values()))
    total_trials = any_wins[0] + any_wins[1] if isinstance(any_wins, (list, tuple)) and len(any_wins) == 2 else None

    for ax, shape in zip(axes, shapes):
        matchups = [(p1, p2, wins) for (s, p1, p2), wins in results.items() if s == shape]
        matchups.sort(key=lambda x: (x[0], x[1]))

        p1_wins = [wins[0] for (_, _, wins) in matchups]
        p2_wins = [wins[1] for (_, _, wins) in matchups]

        x = list(range(len(matchups)))
        width = 0.38
        p1_bars = ax.bar([i - width / 2 for i in x], p1_wins, width=width, label="P1 wins")
        p2_bars = ax.bar([i + width / 2 for i in x], p2_wins, width=width, label="P2 wins")

        ax.set_title(shape)
        ax.set_xticks(x)
        ax.set_ylabel("Win count")
        ax.grid(axis="y", alpha=0.25)
        ax.legend()

        # per-bar algorithm labels below x-axis (and optional per-match totals)
        for i, (w1, w2) in enumerate(zip(p1_wins, p2_wins)):
            p1, p2, _ = matchups[i]
            ax.text(
                i - width / 2,
                -0.06,
                p1,
                transform=ax.get_xaxis_transform(),
                ha="center",
                va="top",
                fontsize=8,
                clip_on=False,
            )
            ax.text(
                i + width / 2,
                -0.06,
                p2,
                transform=ax.get_xaxis_transform(),
                ha="center",
                va="top",
                fontsize=8,
                clip_on=False,
            )

    fig.suptitle(title, fontweight="bold")
    if total_trials is not None:
        fig.text(0.5, 0.01, f"Trials per matchup: n={total_trials}", ha="center", va="bottom", fontsize=10)
        plt.tight_layout(rect=[0, 0.08, 1, 0.96])
    else:
        plt.tight_layout(rect=[0, 0.08, 1, 0.96])
    plt.show()

def plot_one_board(shape, results, ax1, ax2):
    algs = list(results.keys())

    times = [results[a][shape]['time_ms'] for a in algs if shape in results[a]]
    nodes = [results[a][shape]['counts']['result'] for a in algs if shape in results[a]]

    # Time
    ax1.bar(algs, times)
    ax1.set_title(f'Search Time ({shape})')
    ax1.set_ylabel('Time (ms)')
    ax1.tick_params(axis='x', rotation=45)

    # Nodes
    ax2.bar(algs, nodes)
    ax2.set_title(f'Node Expansion ({shape})')
    ax2.set_ylabel('Nodes')
    ax2.tick_params(axis='x', rotation=45)

    ax1.set_yscale('log')
    ax2.set_yscale('log')

    return ax1, ax2

def plot_one_searcher(searcher, results, ax1, ax2):
    shapes = results[searcher].keys()

    times = [results[searcher][s]['time_ms'] for s in shapes]
    nodes = [results[searcher][s]['counts']['result'] for s in shapes]

    # Time
    ax1.bar(shapes, times)
    ax1.set_title(f'Search Time ({searcher})')
    ax1.set_ylabel('Time (ms)')
    ax1.tick_params(axis='x', rotation=45)

    # Nodes
    ax2.bar(shapes, nodes)
    ax2.set_title(f'Node Expansion ({searcher})')
    ax2.set_ylabel('Nodes')
    ax2.tick_params(axis='x', rotation=45)

    ax1.set_yscale('log')
    ax2.set_yscale('log')

    return ax1, ax2

# if __name__ == "__main__":
#     print("Peg Solitaire Search Visualization")
#     print("==================================")
#
#     # Ask user which visualization to run
#     choice = input("Choose visualization:\n"
#                   "1. Visualize single search algorithm\n"
#                   "2. Compare all search algorithms\n"
#                   "3. Show board states progression\n"
#                   "Enter choice (1-3): ")
#
#     if choice == '1':
#         # Generate menu from SEARCH_ALGORITHMS in utils.py
#         menu_options = "\n".join([f"{k}. {v['name']}" for k, v in SEARCH_ALGORITHMS.items()])
#         alg_choice = int(input(f"Choose algorithm:\n{menu_options}\n"))
#         visualize_search_matlab(alg_choice)
#     elif choice == '2':
#         compare_search_algorithms()
#     elif choice == '3':
#         # Generate menu from SEARCH_ALGORITHMS in utils.py
#         menu_options = "\n".join([f"{k}. {v['name']}" for k, v in SEARCH_ALGORITHMS.items()])
#         alg_choice = int(input(f"Choose algorithm:\n{menu_options}\n"))
#         time_taken, path_states, solution = play_peg_solitaire(alg_choice, board_shape='French',  test=True, visualize=True)
#         plot_board_states(path_states)
#     else:
#         print("Invalid choice!")