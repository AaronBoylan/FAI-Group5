from utils import *
import pygame
import pygame.gfxdraw
import sys
import os


def pygame_init():
    pygame.init()
    os.environ['ApplePersistenceIgnoreState'] = 'YES'
    screen = pygame.display.set_mode((1000, 550))
    pygame.display.set_caption('Peg Game Portal (AI801 Spring 2026, Group #5)')
    pygame.event.clear()
    return screen


def main_gui():
    screen = pygame_init()
    clock = pygame.time.Clock()

    # Default Selections
    states = {
        'sol_board': 'English',
        'sol_alg': 'A*',
        'duo_board': 'English',
        'duo_p1': 'User',
        'duo_p2': 'MCTS',
        'sys_test': 'Peg Solitaire Search Performance'
    }

    while True:
        screen.fill((30, 30, 30))
        events = pygame.event.get()

        draw_section_header(screen, 'Peg Solitaire', (50, 30))

        draw_text(screen, 'Board Type:', (80, 80))
        sol_board_rects = {}
        for i, b_name in enumerate([v['short_name'] for v in PEG_BOARDS.values()]):
            color = (50, 120, 50) if states['sol_board'] == b_name else (60, 60, 60)
            sol_board_rects[b_name] = draw_button(screen, b_name, (200 + (i * 140), 75), width=130, color=color)

        draw_text(screen, 'Algorithm:', (80, 130))
        sol_alg_rects = {}
        for i, a_name in enumerate([v['short_name'] for v in SEARCH_ALGORITHMS.values()]):
            color = (50, 120, 50) if states['sol_alg'] == a_name else (60, 60, 60)
            sol_alg_rects[a_name] = draw_button(screen, a_name, (200 + (i * 140), 125), width=130, color=color)

        launch_sol = draw_button(screen, 'LAUNCH SOLITAIRE', (200, 175), width=250, color=(150, 50, 50))

        pygame.draw.line(screen, (80, 80, 80), (50, 240), (1050, 240), 1)

        draw_section_header(screen, 'Peg Duotaire', (50, 270))

        draw_text(screen, 'Board Type:', (80, 320))
        duo_board_rects = {}
        for i, b_name in enumerate([v['short_name'] for v in PEG_BOARDS.values()]):
            color = (50, 50, 120) if states['duo_board'] == b_name else (60, 60, 60)
            duo_board_rects[b_name] = draw_button(screen, b_name, (200 + (i * 140), 315), width=130, color=color)

        draw_text(screen, 'Player 1:', (80, 370))
        p1_rects = {}
        for i, p_name in enumerate([v['short_name'] for v in GAME_PLAYERS.values()]):
            color = (50, 50, 120) if states['duo_p1'] == p_name else (60, 60, 60)
            p1_rects[p_name] = draw_button(screen, p_name, (200 + (i * 140), 365), width=130, color=color)

        draw_text(screen, 'Player 2:', (80, 420))
        p2_rects = {}
        for i, p_name in enumerate([v['short_name'] for v in GAME_PLAYERS.values()]):
            color = (50, 50, 120) if states['duo_p2'] == p_name else (60, 60, 60)
            p2_rects[p_name] = draw_button(screen, p_name, (200 + (i * 140), 415), width=130, color=color)

        launch_duo = draw_button(screen, 'LAUNCH DUOTAIRE', (200, 465), width=250, color=(150, 50, 50))

        # pygame.draw.line(screen, (80, 80, 80), (50, 550), (1050, 550), 1)

        # SECTION 3: TESTING
        # draw_section_header(screen, 'System Testing', (50, 580))
        #
        # draw_text(screen, 'Suite:', (80, 630))
        # test_rects = {}
        #
        # for i, t_name in enumerate([v['short_name'] for v in TESTING_MENUS.values()][:2]):
        #     color = (120, 100, 40) if states['sys_test'] == t_name else (60, 60, 60)
        #     test_rects[t_name] = draw_button(screen, t_name, (200 + (i * 320), 625), width=300, color=color)
        #
        # for i, t_name in enumerate([v['short_name'] for v in TESTING_MENUS.values()][2:]):
        #     color = (120, 100, 40) if states['sys_test'] == t_name else (60, 60, 60)
        #     test_rects[t_name] = draw_button(screen, t_name, (200 + (i * 320), 675), width=300, color=color)
        #
        # launch_test = draw_button(screen, 'START TESTING', (200, 735), width=250, color=(150, 50, 50))

        # EVENT HANDLING
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Solitaire logic
                for name, rect in sol_board_rects.items():
                    if rect.collidepoint(event.pos): states['sol_board'] = name
                for name, rect in sol_alg_rects.items():
                    if rect.collidepoint(event.pos): states['sol_alg'] = name

                # Duotaire logic
                for name, rect in duo_board_rects.items():
                    if rect.collidepoint(event.pos): states['duo_board'] = name
                for name, rect in p1_rects.items():
                    if rect.collidepoint(event.pos): states['duo_p1'] = name
                for name, rect in p2_rects.items():
                    if rect.collidepoint(event.pos): states['duo_p2'] = name

                # Testing logic
                # for name, rect in test_rects.items():
                #     if rect.collidepoint(event.pos): states['sys_test'] = name

                # Execution
                if launch_sol.collidepoint(event.pos):
                    # print(f'Launch Solitaire: {states["sol_board"]} / {states["sol_alg"]}')
                    peg_sol = PegSolitaire(shape=states['sol_board'])
                    search_method = next((v['method'] for v in SEARCH_ALGORITHMS.values() if v['short_name'] == states["sol_alg"]), None)
                    if search_method:
                        pathStates = path_states(search_method(peg_sol))
                        plot_board_states(pathStates)

                if launch_duo.collidepoint(event.pos):
                    # print(f'Launch Duotaire: {states["duo_board"]} / {states["duo_p1"]} / {states["duo_p2"]}')
                    has_user_player = (states['duo_p1'] == 'User') or (states['duo_p2'] == 'User')
                    if has_user_player and (states['duo_board'] != 'English'):
                        draw_warning_overlay(screen, "Interactive play is only supported on the English Board.")
                        continue

                    peg_duo = PegDuotaire(shape=states['duo_board'])

                    def get_logic(player_key):
                        short_name = states[player_key]
                        if short_name == 'User':
                            return lambda g, s: user_player_gui(g, s, screen)
                        return next((v['method'] for v in GAME_PLAYERS.values()
                                     if v['short_name'] == short_name), None)

                    p1, p2 = get_logic('duo_p1'), get_logic('duo_p2')
                    if not (p1 and p2):
                        continue

                    if has_user_player:
                        final_board = play_game(peg_duo, {'X': p1, 'O': p2}, verbose=False, screen=screen, draw_board=draw_board)
                    else:
                        pathStates = []
                        final_board = play_game(peg_duo, {'X': p1, 'O': p2}, verbose=False, pathState=pathStates)
                        plot_board_states(pathStates, duo=True, player1=states['duo_p1'], player2=states['duo_p2'])

                    winner = states['duo_p1'] if peg_duo.utility(final_board, 'X') == 1 else states['duo_p2']
                    draw_warning_overlay(screen, f"Winner: {winner}")

                # if launch_test.collidepoint(event.pos):
                #
                #     def run_test():
                #         match states["sys_test"]:
                #             case "Peg Solitaire Search Performance":
                #                 test_performance((depth_first_bfs, greedy_bfs, astar_search, peg_bidirectional_astar_search, mcts_search),
                #                                  ('Triangle', 'English', 'French'), verbose=True)
                #
                #             case "Peg Duotaire Game Performance":
                #                 pass
                #
                #             case "Peg Board Bitwise Performance":
                #                 test_data_structures()
                #
                #             case "DFS Search Direction Comparison":
                #                 test_directions(depth_first_bfs, 'English')
                #
                #     execute_with_ui(screen, states["sys_test"], run_test)

        pygame.display.flip()
        clock.tick(30)


def user_player_gui(game, state, screen):
    selected_idx = None

    while True:
        draw_board(screen, state.state, selected_idx)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                idx = get_bit_index_from_mouse(event.pos)

                if idx is not None:
                    if selected_idx is None:
                        if (state.state >> idx) & 1:
                            selected_idx = idx
                    else:
                        target_move = None
                        for action in game.actions(state):
                            f, o, t, _ = action
                            f_idx = f.bit_length() - 1
                            t_idx = t.bit_length() - 1

                            if f_idx == selected_idx and t_idx == idx:
                                target_move = action
                                break

                        if target_move:
                            return target_move
                        elif (state.state >> idx) & 1:
                            selected_idx = idx
                        else:
                            selected_idx = None


def draw_section_header(screen, message, pos):
    font = pygame.font.SysFont('Arial', 28, bold=True)
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, pos)


def draw_text(screen, message, pos, size=24, color=(255, 255, 255)):
    font = pygame.font.SysFont('Arial', 18)
    text = font.render(message, True, (180, 180, 180))
    screen.blit(text, pos)


def draw_button(screen, message, position, width=250, height=35, color=(70, 70, 70)):
    font = pygame.font.SysFont('Arial', 16)

    bx, by = position
    bw, bh = int(width), int(height)
    button_rect = pygame.Rect(bx, by, bw, bh)

    mouse_pos = pygame.mouse.get_pos()
    draw_color = tuple(min(c + 25, 255) for c in color) if button_rect.collidepoint(mouse_pos) else color

    pygame.draw.rect(screen, draw_color, button_rect, border_radius=4)
    pygame.draw.rect(screen, (150, 150, 150), button_rect, 1, border_radius=4)

    text_surf = font.render(message, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

    return button_rect


CELL_SIZE = 48
OFFSET_X = 220
OFFSET_Y = 150
PEG_RADIUS = 14
HOLE_RADIUS = 16


def draw_board(screen, state, selected_idx=None):
    screen.fill((25, 25, 28))

    for (r, c), bit_idx in EnglishPegBoardInt.INDEX_MAP.items():
        x, y = int(c * CELL_SIZE + OFFSET_X), int(r * CELL_SIZE + OFFSET_Y)

        # Draw Hole
        pygame.gfxdraw.aacircle(screen, x, y, HOLE_RADIUS, (15, 15, 18))
        pygame.gfxdraw.filled_circle(screen, x, y, HOLE_RADIUS, (15, 15, 18))

        # Draw Peg
        if (state >> bit_idx) & 1:
            peg_color = (200, 200, 205)
            pygame.gfxdraw.aacircle(screen, x, y, PEG_RADIUS, peg_color)
            pygame.gfxdraw.filled_circle(screen, x, y, PEG_RADIUS, peg_color)

            # Draw Highlight
            if bit_idx == selected_idx:
                for r_offset in range(2):
                    pygame.gfxdraw.aacircle(screen, x, y, HOLE_RADIUS + r_offset, (0, 255, 200))

    pygame.display.flip()


def get_bit_index_from_mouse(pos):
    mx, my = pos  # Mouse coordinates

    col = round((mx - OFFSET_X) / CELL_SIZE)
    row = round((my - OFFSET_Y) / CELL_SIZE)

    for (r, c), bit_idx in EnglishPegBoardInt.INDEX_MAP.items():
        if r == row and c == col:
            target_x = c * CELL_SIZE + OFFSET_X
            target_y = r * CELL_SIZE + OFFSET_Y

            distance = ((mx - target_x) ** 2 + (my - target_y) ** 2) ** 0.5

            if distance < 20:
                return bit_idx

    return None


def wrap_text(text, font, max_width):
    """Correctly splits text into multiple lines based on pixel width."""
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        # FIX: Added because font.size returns (width, height)
        if font.size(test_line)[0] < max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    lines.append(' '.join(current_line))
    return lines


def draw_warning_overlay(screen, message):
    # Setup Fonts & Colors
    title_font = pygame.font.SysFont('Arial', 18, bold=True)
    msg_font = pygame.font.SysFont('Arial', 16)

    # UI Colors
    bg_color = (255, 255, 255)
    border_color = (200, 200, 200)
    text_color = (40, 40, 40)
    button_color = (0, 122, 255)  # macOS Blue

    # Dimensions & Centering
    width, height = 320, 150  # Increased height slightly for better spacing
    rect = pygame.Rect((screen.get_width() - width) // 2, (screen.get_height() - height) // 2, width, height)

    # Background Dimming (This makes it look much better/less "ugly")
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))  # Semi-transparent black
    screen.blit(overlay, (0, 0))

    # Draw Shadow
    pygame.draw.rect(screen, (0, 0, 0, 40), rect.move(3, 3), border_radius=10)
    # Main Surface
    pygame.draw.rect(screen, bg_color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, width=1, border_radius=10)

    # Render Header
    # title_surf = title_font.render("Unsupported Mode", True, (0, 0, 0))
    # screen.blit(title_surf, (rect.x + 25, rect.y + 25))

    # Render Wrapped Message
    wrapped_lines = wrap_text(message, msg_font, width - 30)
    for i, line in enumerate(wrapped_lines):
        line_surf = msg_font.render(line, True, text_color)
        screen.blit(line_surf, (rect.x + 15, rect.y + 30 + (i * 22)))

    # Draw "OK" Button
    btn_rect = pygame.Rect(rect.centerx - 35, rect.bottom - 45, 70, 28)
    pygame.draw.rect(screen, button_color, btn_rect, border_radius=6)
    btn_text = title_font.render("OK", True, (255, 255, 255))
    screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))

    pygame.display.flip()

    # Modal Loop (Wait for OK click)
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_rect.collidepoint(event.pos):
                break  # Close the warning


# def execute_with_ui(screen, title, task_func):
#     screen.fill((30, 30, 30))
#     draw_section_header(screen, f"Processing: {title}...", (50, 40))
#     draw_text(screen, "Running algorithm... Please wait.", (80, 100), color=(200, 200, 0))
#     pygame.display.flip()
#     pygame.event.pump()
#
#     # Redirect IO
#     output_buffer = io.StringIO()
#     sys.stdout = output_buffer
#     # output_buffer = None
#
#     try:
#         task_func()
#     except Exception as e:
#         print(f"\nCRASH ERROR: {e}")
#     finally:
#         sys.stdout = sys.__stdout__ # Restore IO
#
#     if output_buffer:
#         show_output_page(screen, title, output_buffer.getvalue())
#
#
# def show_output_page(screen, title, text_content):
#     running = True
#     lines = text_content.split('\n')
#
#     while running:
#         screen.fill((20, 20, 20))
#         draw_section_header(screen, f"Results: {title}", (50, 40))
#
#         for i, line in enumerate(lines[:28]):
#             draw_text(screen, line, (60, 100 + (i * 22)), size=16, color=(220, 220, 220))
#
#         back_btn = draw_button(screen, "BACK TO MENU", (50, 820), width=200, color=(150, 50, 50))
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit();
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if back_btn.collidepoint(event.pos):
#                     running = False
#
#         pygame.display.flip()