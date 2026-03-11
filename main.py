#!/usr/bin/env python3

from peg_solitaire import *
from peg_duotaire import *
from peg_board import *
from search4e import *
from games4e import *
import time


def play_peg_solitaire(searchType: int):
    peg_sol = PegSolitaire()

    startTime = time.time()
    pathStates = []
    match searchType:
        case 1:
            print(f'Running BFS...')
            pathStates = path_states(breadth_first_bfs(peg_sol)) 
        case 2:
            print(f'Running DFS...')
            pathStates = path_states(depth_first_bfs(peg_sol))
        case 3:
            print(f'Running Iterative Deepening...')                
            pathStates = path_states(iterative_deepening_search(peg_sol))
        case 4:
            print(f'Running A* Search...')
            pathStates = path_states(astar_search(peg_sol))
        case 5:
            print(f'Running Greedy BFS...')
            pathStates = path_states(greedy_bfs(peg_sol))
        case _:
            print("Invalid input.")
    
    counter = 0
    for s in pathStates:
        print(f'Step {counter}:')
        print(s)
        print("\n")
        counter += 1
    timeTaken = time.time() - startTime
    print(f"Turns taken: {len(pathStates)}")
    print(f"Time taken: {timeTaken:.2f} seconds")

def play_peg_duotaire():
    peg_duo = PegDuotaire()
    final_board = play_game(peg_duo, dict(X=random_player, O=random_player), verbose=True)
    #final_board = play_game(peg_duo, dict(X=random_player, O=player(alphabeta_search)), verbose=True)  # take very long time for one step
    print(f'Utility of X is: {peg_duo.utility(final_board, "X")}')

def main():
    userInput = int(input("Enter 1 to play Peg Solitaire, or 2 to play Peg Duotaire: "))
    match userInput:
        case 1:
            searchType = int(input("Select search type: \n" \
                                    "1. Breadth-First Search\n" \
                                    "2. Depth-First Search\n" \
                                    "3. Iterative Deepening Search\n" \
                                    "4. A* Search\n" \
                                    "5. Greedy Best-First Search\n"))
            play_peg_solitaire(searchType)
        case 2:
            play_peg_duotaire()
        case _:
            print("Invalid input. Please enter 1 or 2.")

if __name__ == "__main__":
    main()