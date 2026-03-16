#!/usr/bin/env python3

from peg_solitaire import *
from peg_duotaire import *
from peg_board import *
from search4e import *
from games4e import *
from utils import *
import time


def play_peg_solitaire(searchType: int, test=False, visualize=False) -> tuple:
    #return tuple for compatiblity with multiple return values
    peg_sol = PegSolitaire(shape='Triangle')

    startTime = time.time()
    pathStates = []
    
    pathStates = path_states(search_methods.get(searchType)(peg_sol))        
        
    if not test:
        print(f"Running {search_names.get(searchType)}...")

    if not test:
        counter = 0
        for s in pathStates:
            print(f'Step {counter}:')
            print(s)
            print("\n")
            counter += 1
    timeTaken = time.time() - startTime
    #print(f"Turns taken: {len(pathStates)}")
    if not test:
        print(f"Time taken: {timeTaken:.2f} seconds")

    #if visualize value return the tuple with additional data elments for plots
    if visualize:
        return timeTaken, pathStates, search_methods.get(searchType)(peg_sol)
    #standard return of time    
    return timeTaken

def play_peg_duotaire():
    peg_duo = PegDuotaire()
    final_board = play_game(peg_duo, dict(X=random_player, O=random_player), verbose=True)
    #final_board = play_game(peg_duo, dict(X=random_player, O=player(alphabeta_search)), verbose=True)  # take very long time for one step
    print(f'Utility of X is: {peg_duo.utility(final_board, "X")}')

def main():
    userInput = int(input("Enter 1 to play Peg Solitaire, or 2 to play Peg Duotaire, or 3 to run test bench: "))
    match userInput:
        case 1:
            #Replaced below with the menu from SEARCH_ALGORITHMS in utils.py
            #            searchType = int(input("Select search type: \n" \
            #                       "1. Depth-First Search\n" \
            #                        "2. A* Search\n" \
            #                        "3. Greedy Best-First Search\n" \
            #                        "4. Bidirectional A* Search\n"))

            # Generate menu from SEARCH_ALGORITHMS in utils.py
            menu_options = "\n".join([f"{k}. {v['name']}" for k, v in SEARCH_ALGORITHMS.items()])
            searchType = int(input(f"Select search type: \n{menu_options}\n"))
            play_peg_solitaire(searchType)
        case 2:
            play_peg_duotaire()
        case 3:
            from testBench import testBench
            testBench()
        case _:
            print("Invalid input. Please enter 1 or 2.")

if __name__ == "__main__":
    main()