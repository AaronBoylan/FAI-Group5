#!/usr/bin/env python3
import time
from utils import PEG_BOARDS, SEARCH_ALGORITHMS, GAME_PLAYERS,TESTING_MENUS
from peg_solitaire import PegSolitaire, peg_bidirectional_astar_search
from peg_duotaire import PegDuotaire, test_duotaire
from visualize_search import plot_board_states, plot_duotaire_results
from search4e import path_states, depth_first_bfs, greedy_bfs, astar_search, mcts_search
from games4e import play_game, user_player
from gui import main_gui
from peg_solitaire import  test_performance, test_data_structures, test_directions
from os import sys
from pathlib import Path





# Backward compatibility - maintain existing dictionaries
search_methods = {k: v['method'] for k, v in SEARCH_ALGORITHMS.items()}
search_names = {k: v['short_name'] for k, v in SEARCH_ALGORITHMS.items()}

def play_startup_audio():
    """Play the startup audio clip when the CLI starts (best-effort)."""
    audio_path = Path(__file__).with_name("shall-we-play-a-game.mp3")
    if not audio_path.exists():
        return
    try:
        #  pygame mixer plays mp3 files
        import pygame
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(str(audio_path))
        pygame.mixer.music.play()
        # delay to allow audio start.
        time.sleep(0.25)
    except Exception:
        # Audio is non-critical; ignore failures (no audio device/codec issues, etc.)
        return

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

def play_peg_duotaire(visualize=True):
    menu_options = "\n".join([f"{k}. {v['name']}" for k, v in PEG_BOARDS.items()])
    shape = int(input(f"Select peg board shape: \n{menu_options}\n"))

    peg_duo = PegDuotaire(shape=PEG_BOARDS[shape]['method'])

    menu_options = "\n".join([f"{k}. {v['name']}" for k, v in GAME_PLAYERS.items()])
    player1 = int(input(f"Select player #1: \n{menu_options}\n"))
    player2 = int(input(f"Select player #2: \n{menu_options}\n"))

    state_history = [] if visualize else None
    final_board = play_game(peg_duo, dict(X=GAME_PLAYERS[player1]['method'],
                                          O=GAME_PLAYERS[player2]['method']), verbose=True, pathState=state_history)
    if peg_duo.utility(final_board, "X") == 1:
        print(f"Player X ({GAME_PLAYERS[player1]['name']}) wins!")
    else:
        print(f"Player O ({GAME_PLAYERS[player2]['name']}) wins!")
    if visualize:
        print(f"Visualizing {GAME_PLAYERS[player1]['name']} vs {GAME_PLAYERS[player2]['name']}...")
        plot_board_states(state_history,
                          duo=True, 
                          player1=GAME_PLAYERS[player1]['name'], 
                          player2=GAME_PLAYERS[player2]['name'], 
                          )

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
            results = test_duotaire(('Random', 'AlphaBeta', 'MCTS'), ('Triangle', 'English', 'French'), 100, verbose=True)
            plot_duotaire_results(results)
        case 3:
            results = test_data_structures()

        case 4:
            test_directions(depth_first_bfs, 'Triangle')
            test_directions(depth_first_bfs, 'English')
            test_directions(depth_first_bfs, 'French')

def user_plays():
    menu_options = "\n".join([f"{k}. {v['name']}" for k, v in PEG_BOARDS.items()])
    shape = int(input(f"Select peg board shape: \n{menu_options}\n"))

    peg_duo = PegDuotaire(shape=PEG_BOARDS[shape]['method'])

    menu_options = "\n".join([f"{k}. {v['name']}" for k, v in GAME_PLAYERS.items()])
    cpu_player = int(input(f"Select your opponent: \n{menu_options}\n"))

    final_board = play_game(peg_duo, dict(X=user_player, O=GAME_PLAYERS[cpu_player]['method']), verbose=True, user_player=True)

    if peg_duo.utility(final_board, "X") == 1:
        print("The other player has no available moves. You win!")
    else:           
        print("There are no more available moves for you. Better luck next time!")
    


def main():
    play_startup_audio()
    print("\n==========Welcome to the Peg Solirtaire Simulator==========")
    print(  "              2026 AI 801 Section 001: Group 5\n")
    print("SHALL WE PLAY A GAME?"   )
    print("1. Simulate Peg Solitaire")
    print("2. Simulate Peg Duotaire")
    print("3. Run Test Bench")
    print("4. User Plays Peg Duotaire")
    print("5. Launch GUI")
    userInput = int(input("Your choice: "))
    match userInput:
        case 1:
            # Generate menu from SEARCH_ALGORITHMS in utils.py
            print("Simulating Peg Solitaire...")
            play_peg_solitaire(visualize=True)

        case 2:
            print("Simulating Peg Duotaire...")
            play_peg_duotaire(visualize=True)

        case 3:
            print("Running Test Bench...")
            test_peg_solitaire()
        
        case 4:
            print("Playing Peg Duotaire...")
            user_plays()

        case 5:
            print("Launching GUI...")
            main_gui()

        case _:
            print("Invalid input. Please enter 1-5.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--gui':
        main_gui()
    else:
        main()