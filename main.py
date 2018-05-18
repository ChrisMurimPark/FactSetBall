import sqlite3
import sys
import time

import distance_sensor

import functools
import pygame
import sqlite_interface
import game_states

GAME_STATE = game_states.HOMESCREEN

pygame.init()

# window dimensions
size = width, height = 800, 480

# colors
BG_COLOR = (24, 41, 84)
BUTTON_COLOR = (0, 175, 235)
FONT_COLOR = (0, 0, 0)

# fonts
DEFAULT_FONT = pygame.font.SysFont('Courier New', 150)
ALPHABET_FONT = pygame.font.SysFont('Courier New', 25)

# homescreen objects
HOMESCREEN_START_BUTTON = pygame.Rect(150, 140, 500, 200)
HOMESCREEN_START_TEXT = DEFAULT_FONT.render('START', True, FONT_COLOR)
HOMESCREEN_START_TEXT_LOCATION = (175, 150)

# playing mode globals
SCORE = 0
START_TIME = None
GAME_TIMER = TIME_REMAINING = 5

# playing screen objects
PLAYING_BOX_SIZE = (300, 200)
TIMER_BOX = pygame.Rect(50, 140, *PLAYING_BOX_SIZE)
TIME_TEXT_LOCATION = (125, 150)
SCORE_BOX = pygame.Rect(450, 140, *PLAYING_BOX_SIZE)
SCORE_TEXT_LOCATION = (525, 150)


# victory screen globals
NAME = ''

# alphabet objects
SCORE_DISPLAY_BOX = pygame.Rect(10, 10, 300, 150)
NAME_BOX = pygame.Rect(490, 10, 300, 150)

x_start, y_start = 30, 200
x_size, y_size = 65, 65
x_increment, y_increment = 75, 75
text_x_offset, text_y_offset = 25, 15
Q_BUTTON = pygame.Rect(x_start + x_increment * 0, y_start + y_increment * 0, x_size, y_size)
Q_TEXT = ALPHABET_FONT.render('Q', True, FONT_COLOR)
Q_TEXT_LOCATION = (x_start + x_increment * 0 + text_x_offset, y_start + y_increment * 0 + text_y_offset)
W_BUTTON = pygame.Rect(x_start + x_increment * 1, y_start + y_increment * 0, x_size, y_size)
W_TEXT = ALPHABET_FONT.render('W', True, FONT_COLOR)
W_TEXT_LOCATION = (x_start + x_increment * 1 + text_x_offset, y_start + y_increment * 0 + text_y_offset)
E_BUTTON = pygame.Rect(x_start + x_increment * 2, y_start + y_increment * 0, x_size, y_size)
E_TEXT = ALPHABET_FONT.render('E', True, FONT_COLOR)
E_TEXT_LOCATION = (x_start + x_increment * 2 + text_x_offset, y_start + y_increment * 0 + text_y_offset)
R_BUTTON = pygame.Rect(x_start + x_increment * 3, y_start + y_increment * 0, x_size, y_size)
R_TEXT = ALPHABET_FONT.render('R', True, FONT_COLOR)
R_TEXT_LOCATION = (x_start + x_increment * 3 + text_x_offset, y_start + y_increment * 0 + text_y_offset)
T_BUTTON = pygame.Rect(x_start + x_increment * 4, y_start + y_increment * 0, x_size, y_size)
T_TEXT = ALPHABET_FONT.render('T', True, FONT_COLOR)
T_TEXT_LOCATION = (x_start + x_increment * 4 + text_x_offset, y_start + y_increment * 0 + text_y_offset)
Y_BUTTON = pygame.Rect(x_start + x_increment * 5, y_start + y_increment * 0, x_size, y_size)
Y_TEXT = ALPHABET_FONT.render('Y', True, FONT_COLOR)
Y_TEXT_LOCATION = (x_start + x_increment * 5 + text_x_offset, y_start + y_increment * 0 + text_y_offset)
U_BUTTON = pygame.Rect(x_start + x_increment * 6, y_start + y_increment * 0, x_size, y_size)
U_TEXT = ALPHABET_FONT.render('U', True, FONT_COLOR)
U_TEXT_LOCATION = (x_start + x_increment * 6 + text_x_offset, y_start + y_increment * 0 + text_y_offset)
I_BUTTON = pygame.Rect(x_start + x_increment * 7, y_start + y_increment * 0, x_size, y_size)
I_TEXT = ALPHABET_FONT.render('I', True, FONT_COLOR)
I_TEXT_LOCATION = (x_start + x_increment * 7 + text_x_offset, y_start + y_increment * 0 + text_y_offset)
O_BUTTON = pygame.Rect(x_start + x_increment * 8, y_start + y_increment * 0, x_size, y_size)
O_TEXT = ALPHABET_FONT.render('O', True, FONT_COLOR)
O_TEXT_LOCATION = (x_start + x_increment * 8 + text_x_offset, y_start + y_increment * 0 + text_y_offset)
P_BUTTON = pygame.Rect(x_start + x_increment * 9, y_start + y_increment * 0, x_size, y_size)
P_TEXT = ALPHABET_FONT.render('P', True, FONT_COLOR)
P_TEXT_LOCATION = (x_start + x_increment * 9 + text_x_offset, y_start + y_increment * 0 + text_y_offset)
A_BUTTON = pygame.Rect(x_start + x_increment * 0.5, y_start + y_increment * 1, x_size, y_size)
A_TEXT = ALPHABET_FONT.render('A', True, FONT_COLOR)
A_TEXT_LOCATION = (x_start + x_increment * 0.5 + text_x_offset, y_start + y_increment * 1 + text_y_offset)
S_BUTTON = pygame.Rect(x_start + x_increment * 1.5, y_start + y_increment * 1, x_size, y_size)
S_TEXT = ALPHABET_FONT.render('S', True, FONT_COLOR)
S_TEXT_LOCATION = (x_start + x_increment * 1.5 + text_x_offset, y_start + y_increment * 1 + text_y_offset)
D_BUTTON = pygame.Rect(x_start + x_increment * 2.5, y_start + y_increment * 1, x_size, y_size)
D_TEXT = ALPHABET_FONT.render('D', True, FONT_COLOR)
D_TEXT_LOCATION = (x_start + x_increment * 2.5 + text_x_offset, y_start + y_increment * 1 + text_y_offset)
F_BUTTON = pygame.Rect(x_start + x_increment * 3.5, y_start + y_increment * 1, x_size, y_size)
F_TEXT = ALPHABET_FONT.render('F', True, FONT_COLOR)
F_TEXT_LOCATION = (x_start + x_increment * 3.5 + text_x_offset, y_start + y_increment * 1 + text_y_offset)
G_BUTTON = pygame.Rect(x_start + x_increment * 4.5, y_start + y_increment * 1, x_size, y_size)
G_TEXT = ALPHABET_FONT.render('G', True, FONT_COLOR)
G_TEXT_LOCATION = (x_start + x_increment * 4.5 + text_x_offset, y_start + y_increment * 1 + text_y_offset)
H_BUTTON = pygame.Rect(x_start + x_increment * 5.5, y_start + y_increment * 1, x_size, y_size)
H_TEXT = ALPHABET_FONT.render('H', True, FONT_COLOR)
H_TEXT_LOCATION = (x_start + x_increment * 5.5 + text_x_offset, y_start + y_increment * 1 + text_y_offset)
J_BUTTON = pygame.Rect(x_start + x_increment * 6.5, y_start + y_increment * 1, x_size, y_size)
J_TEXT = ALPHABET_FONT.render('J', True, FONT_COLOR)
J_TEXT_LOCATION = (x_start + x_increment * 6.5 + text_x_offset, y_start + y_increment * 1 + text_y_offset)
K_BUTTON = pygame.Rect(x_start + x_increment * 7.5, y_start + y_increment * 1, x_size, y_size)
K_TEXT = ALPHABET_FONT.render('K', True, FONT_COLOR)
K_TEXT_LOCATION = (x_start + x_increment * 7.5 + text_x_offset, y_start + y_increment * 1 + text_y_offset)
L_BUTTON = pygame.Rect(x_start + x_increment * 8.5, y_start + y_increment * 1, x_size, y_size)
L_TEXT = ALPHABET_FONT.render('L', True, FONT_COLOR)
L_TEXT_LOCATION = (x_start + x_increment * 8.5 + text_x_offset, y_start + y_increment * 1 + text_y_offset)
Z_BUTTON = pygame.Rect(x_start + x_increment * 1, y_start + y_increment * 2, x_size, y_size)
Z_TEXT = ALPHABET_FONT.render('Z', True, FONT_COLOR)
Z_TEXT_LOCATION = (x_start + x_increment * 1 + text_x_offset, y_start + y_increment * 2 + text_y_offset)
X_BUTTON = pygame.Rect(x_start + x_increment * 2, y_start + y_increment * 2, x_size, y_size)
X_TEXT = ALPHABET_FONT.render('X', True, FONT_COLOR)
X_TEXT_LOCATION = (x_start + x_increment * 2 + text_x_offset, y_start + y_increment * 2 + text_y_offset)
C_BUTTON = pygame.Rect(x_start + x_increment * 3, y_start + y_increment * 2, x_size, y_size)
C_TEXT = ALPHABET_FONT.render('C', True, FONT_COLOR)
C_TEXT_LOCATION = (x_start + x_increment * 3 + text_x_offset, y_start + y_increment * 2 + text_y_offset)
V_BUTTON = pygame.Rect(x_start + x_increment * 4, y_start + y_increment * 2, x_size, y_size)
V_TEXT = ALPHABET_FONT.render('V', True, FONT_COLOR)
V_TEXT_LOCATION = (x_start + x_increment * 4 + text_x_offset, y_start + y_increment * 2 + text_y_offset)
B_BUTTON = pygame.Rect(x_start + x_increment * 5, y_start + y_increment * 2, x_size, y_size)
B_TEXT = ALPHABET_FONT.render('B', True, FONT_COLOR)
B_TEXT_LOCATION = (x_start + x_increment * 5 + text_x_offset, y_start + y_increment * 2 + text_y_offset)
N_BUTTON = pygame.Rect(x_start + x_increment * 6, y_start + y_increment * 2, x_size, y_size)
N_TEXT = ALPHABET_FONT.render('N', True, FONT_COLOR)
N_TEXT_LOCATION = (x_start + x_increment * 6 + text_x_offset, y_start + y_increment * 2 + text_y_offset)
M_BUTTON = pygame.Rect(x_start + x_increment * 7, y_start + y_increment * 2, x_size, y_size)
M_TEXT = ALPHABET_FONT.render('M', True, FONT_COLOR)
M_TEXT_LOCATION = (x_start + x_increment * 7 + text_x_offset, y_start + y_increment * 2 + text_y_offset)


# high score screen shit



# screen object
SCREEN = pygame.display.set_mode(size)


def write_score(score):
    print('FINAL SCORE: {}'.format(score))


def handle_homescreen(event):
    global GAME_STATE

    if event and event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos  # gets mouse position

        if HOMESCREEN_START_BUTTON.collidepoint(*mouse_pos):
            # prints current location of mouse
            print('button was pressed at {0}'.format(mouse_pos))
            GAME_STATE = game_states.WAITING

    draw_events = [
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, HOMESCREEN_START_BUTTON),
        functools.partial(SCREEN.blit, HOMESCREEN_START_TEXT, HOMESCREEN_START_TEXT_LOCATION)
    ]
    return draw_events


def handle_waiting():
    global GAME_STATE

    if distance_sensor.check_distance():
        print('Starting game! GLHFBBGURL')
        GAME_STATE = game_states.PLAYING

    draw_events = [
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, TIMER_BOX),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, SCORE_BOX)
    ]
    return draw_events


def handle_playing():
    global GAME_STATE, GAME_TIMER, START_TIME, SCORE, TIME_REMAINING

    if START_TIME is None:
        START_TIME = time.time()
        TIME_REMAINING = GAME_TIMER
    else:
        TIME_REMAINING = GAME_TIMER - (time.time() - START_TIME)

    if TIME_REMAINING <= 0:
        START_TIME = None
        write_score(SCORE)
        GAME_STATE = game_states.VICTORY_CLAIMING
    else:
        if distance_sensor.check_distance():
            SCORE += 1

    time_text = DEFAULT_FONT.render(str(int(TIME_REMAINING)), True, FONT_COLOR)
    score_text = DEFAULT_FONT.render(str(SCORE), True, FONT_COLOR)

    draw_events = [
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, TIMER_BOX),
        functools.partial(SCREEN.blit, time_text, TIME_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, SCORE_BOX),
        functools.partial(SCREEN.blit, score_text, SCORE_TEXT_LOCATION)
    ]
    return draw_events


def handle_victory_claiming(cnxn, event):
    global GAME_STATE, NAME, SCORE

    button_val = ''

    if event and event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos  # gets mouse position

        button_val = ''

        if A_BUTTON.collidepoint(*mouse_pos):
            button_val = 'A'
        elif B_BUTTON.collidepoint(*mouse_pos):
            button_val = 'B'
        elif C_BUTTON.collidepoint(*mouse_pos):
            button_val = 'C'
        elif D_BUTTON.collidepoint(*mouse_pos):
            button_val = 'D'
        elif E_BUTTON.collidepoint(*mouse_pos):
            button_val = 'E'
        elif F_BUTTON.collidepoint(*mouse_pos):
            button_val = 'F'
        elif G_BUTTON.collidepoint(*mouse_pos):
            button_val = 'G'
        elif H_BUTTON.collidepoint(*mouse_pos):
            button_val = 'H'
        elif I_BUTTON.collidepoint(*mouse_pos):
            button_val = 'I'
        elif J_BUTTON.collidepoint(*mouse_pos):
            button_val = 'J'
        elif K_BUTTON.collidepoint(*mouse_pos):
            button_val = 'K'
        elif L_BUTTON.collidepoint(*mouse_pos):
            button_val = 'L'
        elif M_BUTTON.collidepoint(*mouse_pos):
            button_val = 'M'
        elif N_BUTTON.collidepoint(*mouse_pos):
            button_val = 'N'
        elif O_BUTTON.collidepoint(*mouse_pos):
            button_val = 'O'
        elif P_BUTTON.collidepoint(*mouse_pos):
            button_val = 'P'
        elif Q_BUTTON.collidepoint(*mouse_pos):
            button_val = 'Q'
        elif R_BUTTON.collidepoint(*mouse_pos):
            button_val = 'R'
        elif S_BUTTON.collidepoint(*mouse_pos):
            button_val = 'S'
        elif T_BUTTON.collidepoint(*mouse_pos):
            button_val = 'T'
        elif U_BUTTON.collidepoint(*mouse_pos):
            button_val = 'U'
        elif V_BUTTON.collidepoint(*mouse_pos):
            button_val = 'V'
        elif W_BUTTON.collidepoint(*mouse_pos):
            button_val = 'W'
        elif X_BUTTON.collidepoint(*mouse_pos):
            button_val = 'X'
        elif Y_BUTTON.collidepoint(*mouse_pos):
            button_val = 'Y'
        elif Z_BUTTON.collidepoint(*mouse_pos):
            button_val = 'Z'

        print('{} PRESSED'.format(button_val))

    NAME += button_val

    draw_events = [
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, SCORE_DISPLAY_BOX),
        functools.partial(SCREEN.blit, DEFAULT_FONT.render(str(SCORE), True, FONT_COLOR), SCORE_DISPLAY_BOX),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, NAME_BOX),
        functools.partial(SCREEN.blit, DEFAULT_FONT.render(NAME, True, FONT_COLOR), NAME_BOX),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, Q_BUTTON),
        functools.partial(SCREEN.blit, Q_TEXT, Q_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, W_BUTTON),
        functools.partial(SCREEN.blit, W_TEXT, W_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, E_BUTTON),
        functools.partial(SCREEN.blit, E_TEXT, E_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, R_BUTTON),
        functools.partial(SCREEN.blit, R_TEXT, R_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, T_BUTTON),
        functools.partial(SCREEN.blit, T_TEXT, T_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, Y_BUTTON),
        functools.partial(SCREEN.blit, Y_TEXT, Y_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, U_BUTTON),
        functools.partial(SCREEN.blit, U_TEXT, U_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, I_BUTTON),
        functools.partial(SCREEN.blit, I_TEXT, I_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, O_BUTTON),
        functools.partial(SCREEN.blit, O_TEXT, O_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, P_BUTTON),
        functools.partial(SCREEN.blit, P_TEXT, P_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, A_BUTTON),
        functools.partial(SCREEN.blit, A_TEXT, A_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, S_BUTTON),
        functools.partial(SCREEN.blit, S_TEXT, S_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, D_BUTTON),
        functools.partial(SCREEN.blit, D_TEXT, D_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, F_BUTTON),
        functools.partial(SCREEN.blit, F_TEXT, F_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, G_BUTTON),
        functools.partial(SCREEN.blit, G_TEXT, G_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, H_BUTTON),
        functools.partial(SCREEN.blit, H_TEXT, H_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, J_BUTTON),
        functools.partial(SCREEN.blit, J_TEXT, J_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, K_BUTTON),
        functools.partial(SCREEN.blit, K_TEXT, K_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, L_BUTTON),
        functools.partial(SCREEN.blit, L_TEXT, L_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, Z_BUTTON),
        functools.partial(SCREEN.blit, Z_TEXT, Z_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, X_BUTTON),
        functools.partial(SCREEN.blit, X_TEXT, X_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, C_BUTTON),
        functools.partial(SCREEN.blit, C_TEXT, C_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, V_BUTTON),
        functools.partial(SCREEN.blit, V_TEXT, V_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, B_BUTTON),
        functools.partial(SCREEN.blit, B_TEXT, B_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, N_BUTTON),
        functools.partial(SCREEN.blit, N_TEXT, N_TEXT_LOCATION),
        functools.partial(pygame.draw.rect, SCREEN, BUTTON_COLOR, M_BUTTON),
        functools.partial(SCREEN.blit, M_TEXT, M_TEXT_LOCATION)
    ]

    if len(NAME) >= 3:
        GAME_STATE = game_states.VICTORY_CLAIMED
        sqlite_interface.add_score(cnxn, NAME, 0, SCORE)
        draw_everything(draw_events)
        time.sleep(3)
        SCORE, NAME = 0, ''  # reset SCORE and NAME globals

    return draw_events


def handle_high_scores(cnxn, event):
    draw_events = []
    return draw_events


def handle_game_state(game_state, cnxn, event=None):
    if game_state == game_states.HOMESCREEN:
        return handle_homescreen(event)
    elif game_state == game_states.WAITING:
        return handle_waiting()
    elif game_state == game_states.PLAYING:
        return handle_playing()
    elif game_state == game_states.VICTORY_CLAIMING:
        return handle_victory_claiming(cnxn, event)
    elif game_state == game_states.VICTORY_CLAIMED:
        return handle_high_scores(cnxn, event)


def draw_everything(draw_events):
    SCREEN.fill(BG_COLOR)
    for draw_event in draw_events:
        draw_event()

    pygame.display.flip()


def main(cnxn):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            draw_events = handle_game_state(GAME_STATE, cnxn, event)
            draw_everything(draw_events)

        draw_events = handle_game_state(GAME_STATE, cnxn)
        draw_everything(draw_events)


if __name__ == '__main__':
    main(sqlite3.connect('FSB.DB'))
