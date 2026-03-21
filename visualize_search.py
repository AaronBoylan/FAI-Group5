#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from main import play_peg_solitaire
from peg_solitaire import PegSolitaire
from search4e import path_states
from utils import SEARCH_ALGORITHMS, search_methods, search_names

def visualize_search_matlab(searchType: int):
    """ Visualize the peg solitaire search results using MATLAB-style plots.
    Returns time taken, path states, and solution for further analysis.
    """
    timeTaken, pathStates, solution = play_peg_solitaire(searchType, test=True, visualize=True)

    if not pathStates:
        print("No solution found!")
        return

    print(f"\nVisualization for {search_names.get(searchType)}")
    print(f"Total steps: {len(pathStates)}")
    print(f"Time taken: {timeTaken:.2f} seconds")

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
    if hasattr(solution, 'path_cost'):
        # show path info if available
        path_costs = []
        current_cost = 0
        for i, state in enumerate(pathStates):
            path_costs.append(current_cost)
            if i < len(pathStates) - 1:
                current_cost += 1  # Each move costs 1

        ax4.plot(steps, path_costs, 'g-s', linewidth=2, markersize=4)
        ax4.set_xlabel('Search Steps')
        ax4.set_ylabel('Path Cost')
        ax4.set_title('Cumulative Path Cost')
        ax4.grid(True, alpha=0.3)
    else:
        # Alternative: show peg reduction rate
        peg_reduction_rate = []
        for i in range(1, len(peg_counts)):
            rate = peg_counts[i-1] - peg_counts[i]
            peg_reduction_rate.append(rate)

        ax4.plot(range(1, len(peg_counts)), peg_reduction_rate, 'm-^', linewidth=2, markersize=4)
        ax4.set_xlabel('Search Steps')
        ax4.set_ylabel('Pegs Removed per Step')
        ax4.set_title('Peg Removal Rate')
        ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return timeTaken, pathStates, solution

def plot_board_states(pathStates, max_states=6):
    # Plot actual board states at different steps using ASCII-like visualization.
    
    if not pathStates:
        print("No states to visualize!")
        return

    # Select key states to show
    n_states = min(max_states, len(pathStates))
    indices = np.linspace(0, len(pathStates)-1, n_states, dtype=int)

    fig, axes = plt.subplots(1, n_states, figsize=(4*n_states, 4))
    if n_states == 1:
        axes = [axes]

    for i, idx in enumerate(indices):
        state = pathStates[idx]
        board_str = str(state)

        # Clear the axis
        axes[i].clear()
        axes[i].axis('off')
        axes[i].set_title(f'Step {idx}')

        # Display the board as text
        axes[i].text(0.5, 0.5, board_str,
                    transform=axes[i].transAxes,
                    fontsize=10,
                    verticalalignment='center',
                    horizontalalignment='center',
                    fontfamily='monospace')

    plt.tight_layout()
    plt.show()

def compare_search_algorithms():
    #Compare different search algorithms using MATLAB-style plots.
    
    algorithms = list(SEARCH_ALGORITHMS.keys())  # Use all available algorithms
    results = {}

    for alg in algorithms:
        print(f"Running {search_names.get(alg)}...")
        try:
            time_taken, path_states, solution = play_peg_solitaire(alg, test=True, visualize=True)
            results[alg] = {
                'time': time_taken,
                'steps': len(path_states),
                'pegs_remaining': path_states[-1].state.bit_count() if path_states else 0
            }
        except Exception as e:
            print(f"Error with {search_names.get(alg)}: {e}")
            results[alg] = {'time': float('inf'), 'steps': float('inf'), 'pegs_remaining': float('inf')}

    # Create comparison plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

    alg_names = [SEARCH_ALGORITHMS[alg]['short_name'] for alg in algorithms]

    # Time comparison
    times = [results[alg]['time'] for alg in algorithms]
    ax1.bar(alg_names, times, color='skyblue')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Search Time Comparison')
    ax1.tick_params(axis='x', rotation=45)

    # Steps comparison
    steps = [results[alg]['steps'] for alg in algorithms]
    ax2.bar(alg_names, steps, color='lightgreen')
    ax2.set_ylabel('Number of Steps')
    ax2.set_title('Solution Steps Comparison')
    ax2.tick_params(axis='x', rotation=45)

    # Final pegs comparison
    pegs = [results[alg]['pegs_remaining'] for alg in algorithms]
    ax3.bar(alg_names, pegs, color='salmon')
    ax3.set_ylabel('Final Pegs Remaining')
    ax3.set_title('Solution Quality (Lower is Better)')
    ax3.tick_params(axis='x', rotation=45)

    # Efficiency plot (steps vs time)
    ax4.scatter(times, steps, s=100, c=range(len(algorithms)), cmap='viridis')
    for i, alg in enumerate(algorithms):
        ax4.annotate(search_names.get(alg), (times[i], steps[i]),
                    xytext=(5, 5), textcoords='offset points')
    ax4.set_xlabel('Time (seconds)')
    ax4.set_ylabel('Steps')
    ax4.set_title('Efficiency: Time vs Steps')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return results

if __name__ == "__main__":
    print("Peg Solitaire Search Visualization")
    print("==================================")

    # Ask user which visualization to run
    choice = input("Choose visualization:\n"
                  "1. Visualize single search algorithm\n"
                  "2. Compare all search algorithms\n"
                  "3. Show board states progression\n"
                  "Enter choice (1-3): ")

    if choice == '1':
        # Generate menu from SEARCH_ALGORITHMS in utils.py
        menu_options = "\n".join([f"{k}. {v['name']}" for k, v in SEARCH_ALGORITHMS.items()])
        alg_choice = int(input(f"Choose algorithm:\n{menu_options}\n"))
        visualize_search_matlab(alg_choice)
    elif choice == '2':
        compare_search_algorithms()
    elif choice == '3':
        # Generate menu from SEARCH_ALGORITHMS in utils.py
        menu_options = "\n".join([f"{k}. {v['name']}" for k, v in SEARCH_ALGORITHMS.items()])
        alg_choice = int(input(f"Choose algorithm:\n{menu_options}\n"))
        time_taken, path_states, solution = play_peg_solitaire(alg_choice, test=True, visualize=True)
        plot_board_states(path_states)
    else:
        print("Invalid choice!")