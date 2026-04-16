#!/usr/bin/env python3
from peg_solitaire import *
from peg_duotaire import *
from peg_board import *
from visualize_search import *
from search4e import *
from games4e import *
from utils import *
import time


def play_peg_solitaire(visualize=True):
    menu_options = "\n".join([f"{k}. {v['name']}" for k, v in PEG_BOARDS.items()])
    shape = int(input(f"Select peg board shape: \n{menu_options}\n"))

    peg_sol = PegSolitaire(shape=PEG_BOARDS[shape]['method'])

    menu_options = "\n".join([f"{k}. {v['name']}" for k, v in SEARCH_ALGORITHMS.items()])
    searchType = int(input(f"Select search type: \n{menu_options}\n"))

    startTime = time.time_ns()

    #search_methods.get(searchType) is a function, so we need to call it with the arguments
    pathStates = path_states(search_methods.get(searchType)(peg_sol))
        
    timeTaken = (time.time_ns() - startTime) / 1_000_000

    if visualize:
        plot_board_states(pathStates)
        # visualize_search_matlab(searchType, timeTaken, pathStates)

    return

def play_peg_duotaire():
    menu_options = "\n".join([f"{k}. {v['name']}" for k, v in PEG_BOARDS.items()])
    shape = int(input(f"Select peg board shape: \n{menu_options}\n"))

    peg_duo = PegDuotaire(shape=PEG_BOARDS[shape]['method'])

    menu_options = "\n".join([f"{k}. {v['name']}" for k, v in GAME_PLAYERS.items()])
    player1 = int(input(f"Select player #1: \n{menu_options}\n"))
    player2 = int(input(f"Select player #2: \n{menu_options}\n"))

    final_board = play_game(peg_duo, dict(X=GAME_PLAYERS[player1]['method'],
                                          O=GAME_PLAYERS[player2]['method']), verbose=True)

    print(f'Utility of X is: {peg_duo.utility(final_board, "X")}')

def test_peg_solitaire():
    menu_options = "\n".join([f"{k}. {v['name']}" for k, v in TESTING_MENUS.items()])
    testType = int(input(f"Select test type: \n{menu_options}\n"))

    match testType:
        case 1:
            test_performance(
                (depth_first_bfs, greedy_bfs, astar_search,
                 peg_bidirectional_astar_search, mcts_search),
                ('Triangle', 'English', 'French'), verbose=True)
            # test_performance(
            #     (astar_search, peg_bidirectional_astar_search),
            #     ('Triangle', 'English', 'French'), verbose=True)

        case 2:
            test_data_structures()

        case 3:
            test_directions(depth_first_bfs, 'English')

        case 4:
            compare_search_algorithms()

def main():
    userInput = int(input("Enter 1 to play Peg Solitaire, or 2 to play Peg Duotaire, or 3 to run test bench: "))
    match userInput:
        case 1:
            # Generate menu from SEARCH_ALGORITHMS in utils.py
            play_peg_solitaire(visualize=True)

        case 2:
            play_peg_duotaire()

        case 3:
            test_peg_solitaire()

        case _:
            print("Invalid input. Please enter 1 or 2.")

if __name__ == "__main__":
    main()