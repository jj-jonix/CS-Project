import pygame
from globals import *
from storage import Store
from mainMenu import Main_menu
import ai
import engine
import threading
import traceback
from copy import deepcopy

DETAILS = {
    'user': 'root',
    'host': 'localhost',
    'password': '123456789'
}

ai_thread = None
ai_lock = threading.Lock()
pending_cpu_move = None
game_number = 0

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Chess")

for piece in ['wP','wR','wN','wB','wQ','wK','bP','bR','bN','bB','bQ','bK']:
    IMAGES[piece] = pygame.transform.smoothscale(pygame.image.load(f'src/{piece}.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))
icon_size = PADDING - 5
black_resign_image = pygame.transform.smoothscale(pygame.image.load('src/resign.png').convert_alpha(), (icon_size, icon_size))
white_resign_image = black_resign_image
draw_image = pygame.transform.smoothscale(pygame.image.load('src/draw.png').convert_alpha(), (icon_size, icon_size))
save_image = pygame.transform.smoothscale(pygame.image.load('src/save.png').convert_alpha(), (icon_size, icon_size))
black_resign_image_rect = black_resign_image.get_rect(center = (WIN_WIDTH-PADDING//2, WIN_HEIGHT//2 - icon_size - 50))
white_resign_image_rect = white_resign_image.get_rect(center = (WIN_WIDTH-PADDING//2, WIN_HEIGHT//2 + icon_size + 50))
draw_image_rect = draw_image.get_rect(center = (WIN_WIDTH-PADDING//2, WIN_HEIGHT//2))
save_image_rect = save_image.get_rect(center = (PADDING//2, WIN_HEIGHT//2))
ingame_icons = [('black resign', black_resign_image_rect, black_resign_image, 'Resign as Black'),('white resign', white_resign_image_rect, white_resign_image, 'Resign as White'),
                ('draw', draw_image_rect, draw_image, 'Agree a draw'),('save', save_image_rect, save_image, 'Save game')]

last_move_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
last_move_surface.fill(LAST_MOVE_COLOR)
selected_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
selected_surface.fill(SELECTED_COLOR)
dot_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
pygame.draw.circle(dot_surface, (20, 20, 20, 60), (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//6)
capture_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
pygame.draw.circle(capture_surface, (20, 20, 20, 60), (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//2 - 2, 7)
coord_font = pygame.font.SysFont('segoeui,helvetica,arial', 15, bold=True)

BACK_PAGES = {'data menu':'main menu','modify data':'main menu','load game':'main menu','play':'main menu','view all data':'data menu','view specific data':'data menu','add data':'modify data',
              'delete data':'modify data','change data':'modify data','delete game data':'modify data','delete all data':'modify data','delete all game data':'modify data','edit player stats':'change data'}
SINGLE_INPUT_WINDOWS = ('view specific data','add data','delete data','change data','delete game data')


def text_input(event, text, max_length=24,digits_only=False):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        elif event.unicode != '' and event.unicode.isprintable() and len(text) < max_length:
            if event.unicode.isdigit() or not digits_only:
                text += event.unicode
    return text

def draw_board(win):
    for row in range(DIMENTION):
        for col in range(DIMENTION):
            is_light = (row+col)%2==0
            square = pygame.Rect(col*SQUARE_SIZE+PADDING,row*SQUARE_SIZE+PADDING, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, LIGHT_SQUARE if is_light else DARK_SQUARE, square)
            label_color = DARK_SQUARE if is_light else LIGHT_SQUARE
            if col == 0:
                number = coord_font.render(str(8-row), True, label_color)
                win.blit(number, (square.x+4, square.y+3))
            if row == 7:
                letter = coord_font.render(chr(97+col), True, label_color)
                win.blit(letter, (square.right-letter.get_width()-4,square.bottom-letter.get_height()-2))

def draw_pieces(win, board):
    for row in range(DIMENTION):
        for col in range(DIMENTION):
            piece = board[row][col]
            if piece != '--':
                win.blit(IMAGES[piece], (col*SQUARE_SIZE+PADDING, row*SQUARE_SIZE+PADDING))

def highlight_squares(win, gs, valid_moves, square_selected, move_log):
    if len(move_log) != 0:
        move = move_log[-1]
        win.blit(last_move_surface, (move.start_col*SQUARE_SIZE+PADDING, move.start_row*SQUARE_SIZE+PADDING))
        win.blit(last_move_surface, (move.end_col*SQUARE_SIZE+PADDING, move.end_row*SQUARE_SIZE+PADDING))
    if square_selected != ():
        row, col = square_selected
        if gs.board[row][col][0] == ('w' if gs.white_to_move else 'b'):
            win.blit(selected_surface,(col*SQUARE_SIZE+PADDING, row*SQUARE_SIZE+PADDING))
            targets = set()
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    targets.add((move.end_row, move.end_col))
            for end_row, end_col in targets:
                marker = dot_surface if gs.board[end_row][end_col] == '--' else capture_surface
                win.blit(marker,(end_col*SQUARE_SIZE+PADDING, end_row*SQUARE_SIZE+PADDING))

def draw_game_state(win, gs, player1_name, player2_name, valid_moves, square_selected, thinking, temp_msg, main_menu):
    win.fill(BACKGROUND)
    for name, is_white, mid_y in ((player2_name, False, PADDING//2), (player1_name, True, WIN_HEIGHT-PADDING//2)):
        turn = gs.white_to_move == is_white
        icon = pygame.Rect(0, 0, 14, 14)
        icon.center = (PADDING+9, mid_y)
        pygame.draw.rect(win, (245, 245, 240) if is_white else (18, 18, 17), icon, border_radius=3)
        pygame.draw.rect(win, GREEN if turn else BORDER, icon, 2 if turn else 1, border_radius=3)
        name_text = main_menu.FONT3.render(name, True, OFF_WHITE if turn else MUTED_GRAY)
        win.blit(name_text, name_text.get_rect(midleft=(PADDING+26, mid_y)))
        note, note_color = '', MUTED_GRAY
        if turn and thinking:
            note, note_color = 'Thinking...', GREEN
        elif is_white:
            note = 'Z: undo'
        if note != '':
            note_text = main_menu.FONT4.render(note, True, note_color)
            win.blit(note_text, note_text.get_rect(midright=(WIN_WIDTH-PADDING-2, mid_y)))
    if temp_msg != '':
        temp_msg = main_menu.FONT4.render(temp_msg, True, GREEN)
        win.blit(temp_msg, temp_msg.get_rect(center=(WIN_WIDTH//2+60, WIN_HEIGHT-PADDING//2)))
    draw_board(win)
    highlight_squares(win, gs, valid_moves, square_selected, gs.move_log)
    draw_pieces(win, gs.board)

def draw_ingame_icons(win, main_menu, confirm_action, confirm_until, clickable):
    mouse_pos = pygame.mouse.get_pos()
    hovered = None
    for name, rect, image, msg in ingame_icons:
        if clickable:
            main_menu.clickable.append(rect)
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(win, PANEL_LIGHT, rect.inflate(6, 6), border_radius=6)
                hovered = (name, rect, msg)
        win.blit(image, rect)
    if hovered:
        name, rect, msg = hovered
        if confirm_action == name and pygame.time.get_ticks() < confirm_until:
            msg = 'Click again to confirm'
        msg_text = main_menu.FONT4.render(msg, True, OFF_WHITE)
        box = msg_text.get_rect().inflate(20,12)
        if name == 'save':
            box.midleft = (rect.right+10,rect.centery)
        else:
            box.midright = (rect.left-10,rect.centery)
        pygame.draw.rect(win, PANEL, box, border_radius=6)
        pygame.draw.rect(win, BORDER, box, 1, border_radius=6)
        win.blit(msg_text, msg_text.get_rect(center=box.center))

def draw_game_over(win, main_menu, headline, reason):
    dim = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
    dim.fill((18, 17, 15, 175))
    win.blit(dim, (0, 0))
    box = pygame.Rect(0, 0, 440, 240)
    box.center = (WIN_WIDTH//2, WIN_HEIGHT//2)
    pygame.draw.rect(win, PANEL, box, border_radius=10)
    pygame.draw.rect(win, BORDER, box, 1, border_radius=10)
    headline_text = main_menu.FONT2.render(headline, True, OFF_WHITE)
    win.blit(headline_text, headline_text.get_rect(center=(box.centerx, box.y+70)))
    reason_text = main_menu.FONT3.render(reason, True, MUTED_GRAY)
    win.blit(reason_text, reason_text.get_rect(center=(box.centerx, box.y+114)))
    rematch_rect = main_menu.draw_button(win, 'Rematch', pygame.Rect(box.x+28, box.bottom-76, 180, 46), 'important')
    menu_button_rect = main_menu.draw_button(win, 'Main menu', pygame.Rect(box.right-28-180, box.bottom-76, 180, 46))
    return rematch_rect, menu_button_rect

def run_ai(gamestate, valid_moves, depth, token):
    global pending_cpu_move
    try:
        move = ai.choose_move(gamestate, valid_moves, depth)
    except Exception:
        traceback.print_exc()
        move = None
    with ai_lock:
        pending_cpu_move = (token, move)


def main():
    global ai_thread, pending_cpu_move, game_number
    current_window = 'main menu'
    previous_window = 'main menu'
    run = True
    Clock = pygame.time.Clock()
    main_menu = Main_menu()
    store = Store(DETAILS)

    input_text = ''
    status_text = ''
    message_after_switch = ''
    stats_text = ['','','']
    player_names = ['','']
    focused_field = 0
    current_player = None
    player_rows = []
    saved_games = []
    save_buttons = []
    action_rect = None
    back_rect = None
    white_cpu_rect = None
    black_cpu_rect = None

    player1_name = ''
    player2_name = ''
    white_is_cpu = False
    black_is_cpu = False
    white_difficulty = ''
    black_difficulty = ''

    gamestate = engine.gameState()
    valid_moves = gamestate.get_valid_moves()
    square_selected = ()
    player_clicks = []
    loaded_save_id = None
    start_new_game = False
    loaded_gamestate = None
    loaded_save_choice = None
    result_shown = False
    result_headline = ''
    result_reason = ''
    end_reason = None
    confirm_action = None
    confirm_until = 0
    temp_msg = ''
    temp_msg_until = 0
    rematch_rect = None
    menu_button_rect = None

    while run:
        Clock.tick(30)
        clicked = False
        pressed_enter = False
        pressed_escape = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                continue
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    pressed_enter = True
                if event.key == pygame.K_ESCAPE:
                    pressed_escape = True

            if current_window == 'game':
                #end screen
                if result_shown:
                    if clicked and rematch_rect and rematch_rect.collidepoint(event.pos):
                        start_new_game = True
                    elif clicked and menu_button_rect and menu_button_rect.collidepoint(event.pos):
                        start_new_game = True
                        current_window = 'main menu'
                    continue

                cpu_move = (gamestate.white_to_move and white_is_cpu) or (not gamestate.white_to_move and black_is_cpu)
                #in game clicks
                if clicked:
                    pos = event.pos
                    if BOARD_WIDTH + PADDING > pos[0] > PADDING and BOARD_HEIGHT + PADDING > pos[1] > PADDING:
                        if ai_thread is None and not cpu_move:
                            col = (pos[0]-PADDING)//SQUARE_SIZE
                            row = (pos[1]-PADDING)//SQUARE_SIZE
                            if square_selected == (row, col): #double click
                                square_selected = ()
                                player_clicks = []
                            else:
                                square_selected = (row, col)
                                player_clicks.append(square_selected)
                            #second click
                            if len(player_clicks) == 2:
                                move = engine.Move(player_clicks[0], player_clicks[1], gamestate.board)
                                move_made = False
                                for valid_move in valid_moves:
                                    if move == valid_move:
                                        gamestate.make_move(valid_move)
                                        valid_moves = gamestate.get_valid_moves()
                                        move_made = True
                                        break
                                if move_made:
                                    square_selected = ()
                                    player_clicks = []
                                else:
                                    player_clicks = [square_selected]
                    else:
                        for icon_name,icon_rect,icon_image,icon_msg in ingame_icons:
                            if not icon_rect.collidepoint(pos):
                                continue
                            if icon_name == 'save':
                                try:
                                    store.save_game(player1_name, player2_name, gamestate, white_difficulty, black_difficulty)
                                    temp_msg = 'Game saved'
                                except:
                                    temp_msg = 'Could not save'
                                temp_msg_until = pygame.time.get_ticks() + 2000
                            elif confirm_action == icon_name and pygame.time.get_ticks() < confirm_until:
                                confirm_action = None
                                if icon_name == 'black resign':
                                    gamestate.checkmate = True
                                    gamestate.white_to_move = False
                                    end_reason = 'Black resigned'
                                elif icon_name == 'white resign':
                                    gamestate.checkmate = True
                                    gamestate.white_to_move = True
                                    end_reason = 'White resigned'
                                else:
                                    gamestate.stalemate = True
                                    end_reason = 'Draw agreed'
                            else:
                                confirm_action = icon_name
                                confirm_until = pygame.time.get_ticks() + 3000

                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_z) and (ai_thread is None) and (len(gamestate.move_log) != 0):
                    gamestate.undo_move()
                    if (white_is_cpu or black_is_cpu) and len(gamestate.move_log) != 0:
                        gamestate.undo_move()
                    valid_moves = gamestate.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                continue

            if event.type == pygame.MOUSEWHEEL and current_window in ('view all data','load game'):
                main_menu.scroll = max(0, main_menu.scroll-event.y)
                continue
            if current_window in BACK_PAGES and (pressed_escape or (clicked and back_rect and back_rect.collidepoint(event.pos))):
                current_window = BACK_PAGES[current_window]
                continue

            submit = pressed_enter or (clicked and action_rect and action_rect.collidepoint(event.pos))
            if current_window in SINGLE_INPUT_WINDOWS:
                if current_window == 'delete game data':
                    input_text = text_input(event,input_text,9,True)
                else:
                    input_text = text_input(event,input_text)
                if submit:
                    #all windows which take imputs from user and use sql
                    name = input_text.strip()
                    if name == '':
                        if current_window == 'delete game data':
                            status_text = 'Please enter a game number first.' 
                        else:
                            status_text = 'Please enter a name first.'
                    else:
                        try:
                            if current_window == 'view specific data':
                                result = store.fetch_user(name)
                                if result and result[0]:
                                    row = result[0]
                                    status_text = f'{row[0]} | Wins {row[1]} | Losses {row[2]} | Draws {row[3]}'
                                else:
                                    status_text = 'No player found.'
                            elif current_window == 'add data':
                                added = store.store_user(name)
                                if added:
                                    status_text = 'Player added successfully.' 
                                else:
                                    status_text = 'That player already exists.'
                            elif current_window == 'delete data':
                                deleted = store.delete_user(name)
                                if deleted:
                                    status_text = 'Player deleted successfully.' 
                                else:
                                    status_text = 'That player does not exist.'
                            elif current_window == 'delete game data':
                                deleted = store.delete_game(int(name))
                                if deleted:
                                    status_text = 'Game deleted successfully.' 
                                else:
                                    status_text = 'That game does not exist.'
                            elif current_window == 'change data':
                                result = store.fetch_user(name)
                                if result:
                                    row = result[0]
                                    current_player = row[0]
                                    stats_text = [str(row[1]),str(row[2]),str(row[3])]
                                    message_after_switch = 'Edit the record, then save.'
                                    current_window = 'edit player stats'
                                else:
                                    status_text = 'No player found.'
                        except:
                            status_text = 'Could not reach the database.'

            elif current_window == 'edit player stats':
                stats_text[focused_field] = text_input(event,stats_text[focused_field],  6,True)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    focused_field = (focused_field+1)%3
                if clicked:
                    for i in range(3):
                        if Main_menu.STATS_INPUT_RECTS[i].collidepoint(event.pos):
                            focused_field = i
                if submit:
                    try:
                        wins = int(stats_text[0])
                        losses = int(stats_text[1])
                        draws = int(stats_text[2])
                    except ValueError:
                        status_text = 'Please enter a number in every field.'
                    else:
                        try:
                            updated = store.update_user_stats(current_player, wins, losses, draws)
                        except:
                            updated = False
                        if updated:
                            message_after_switch = 'Player stats updated successfully.'
                            current_window = 'change data'
                        else:
                            status_text = 'Could not update player stats.'

            elif current_window == 'play':
                player_names[focused_field] = text_input(event, player_names[focused_field], 20)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    focused_field = (focused_field + 1) % 2
                if clicked:
                    for i in range(2):
                        if Main_menu.PLAYER_INPUT_RECTS[i].collidepoint(event.pos):
                            focused_field = i
                    for i, cpu_rect in enumerate((white_cpu_rect, black_cpu_rect)):
                        if cpu_rect and cpu_rect.collidepoint(event.pos):
                            focused_field = i
                            name = player_names[i].strip().lower()
                            if not name.startswith('cpu') or name == 'cpu':
                                player_names[i] = 'cpu1'
                            elif name[3:].isdigit() and int(name[3:]) < 6:
                                player_names[i] = 'cpu' + str(int(name[3:]) + 1)
                            else:
                                player_names[i] = ''
                if submit:
                    name1 = player_names[0].strip()
                    name2 = player_names[1].strip()
                    if name1 == '' or name2 == '':
                        status_text = 'Please enter both player names.'
                    elif name1.lower() == name2.lower() and not name1.lower().startswith('cpu'):
                        status_text = 'Players must have different names.'
                    else:
                        try:
                            store.store_user(name1)
                            store.store_user(name2)
                        except Exception as e:
                            print(e)
                        player1_name = name1
                        player2_name = name2
                        white_is_cpu = name1.lower().startswith('cpu')
                        black_is_cpu = name2.lower().startswith('cpu')
                        white_difficulty = int(name1[3:]) if white_is_cpu and name1[3:].isdigit() else ''
                        black_difficulty = int(name2[3:]) if black_is_cpu and name2[3:].isdigit() else ''
                        if white_is_cpu and white_difficulty == '':
                            white_difficulty = None
                        if black_is_cpu and black_difficulty == '':
                            black_difficulty = None
                        start_new_game = True
                        current_window = 'game'

            elif current_window in ('delete all data', 'delete all game data'):
                if submit:
                    try:
                        if current_window == 'delete all data':
                            deleted = store.delete_all_users()
                            status_text = 'All player data deleted successfully.' if deleted else 'Could not delete all player data.'
                        else:
                            deleted = store.delete_all_games()
                            status_text = 'All game data deleted successfully.' if deleted else 'Could not delete all game data.'
                    except Exception as error:
                        print(error)
                        status_text = 'Could not reach the database.'

            elif current_window == 'load game':
                if clicked:
                    for button, game_id in save_buttons:
                        if button.collidepoint(event.pos):
                            loaded_gamestate = store.load_game(game_id)
                            if loaded_gamestate is None:
                                break
                            for save in saved_games:
                                if save[0] == game_id:
                                    player1_name = save[2]
                                    player2_name = save[3]
                                    white_is_cpu = player1_name.lower().startswith('cpu')
                                    black_is_cpu = player2_name.lower().startswith('cpu')
                                    white_difficulty = int(save[4]) if str(save[4]).isdigit() else None
                                    black_difficulty = int(save[5]) if str(save[5]).isdigit() else None
                                    break
                            loaded_save_choice = game_id
                            start_new_game = True
                            current_window = 'game'
                            break

            elif current_window in ('main menu', 'data menu', 'modify data'):
                current_window = main_menu.clicks(event, current_window)
                if current_window == 'exit':
                    run = False

        if start_new_game:
            start_new_game = False
            game_number += 1
            gamestate = loaded_gamestate if loaded_gamestate is not None else engine.gameState()
            loaded_save_id = loaded_save_choice
            loaded_gamestate = None
            loaded_save_choice = None
            valid_moves = gamestate.get_valid_moves()
            square_selected = ()
            player_clicks = []
            result_shown = False
            end_reason = None
            confirm_action = None
            temp_msg = ''
            rematch_rect = None
            menu_button_rect = None

        if current_window != previous_window:
            previous_window = current_window
            status_text = message_after_switch
            message_after_switch = ''
            focused_field = 0
            main_menu.scroll = 0
            action_rect = None
            back_rect = None
            save_buttons = []
            if current_window in SINGLE_INPUT_WINDOWS:
                input_text = ''
            try:
                if current_window == 'view all data':
                    player_rows = store.fetchall()
                elif current_window == 'load game':
                    saved_games = store.get_saved_games()
            except Exception as error:
                print(error)

        if current_window == 'game':
            game_ended = gamestate.checkmate or gamestate.stalemate or gamestate.three_fold
            cpu_move = (gamestate.white_to_move and white_is_cpu) or (not gamestate.white_to_move and black_is_cpu)
            if ai_thread is not None and not ai_thread.is_alive():
                with ai_lock:
                    cpu_result = pending_cpu_move
                    pending_cpu_move = None
                ai_thread = None
                if cpu_result and cpu_result[0] == game_number and cpu_result[1] is not None and not game_ended:
                    gamestate.make_move(cpu_result[1])
                    valid_moves = gamestate.get_valid_moves()
                    game_ended = gamestate.checkmate or gamestate.stalemate or gamestate.three_fold
                    cpu_move = (gamestate.white_to_move and white_is_cpu) or (not gamestate.white_to_move and black_is_cpu)
            if game_ended and not result_shown:
                result_shown = True
                winner = None
                if gamestate.checkmate:
                    winner, loser = (player2_name, player1_name) if gamestate.white_to_move else (player1_name, player2_name)
                    result_headline = f'{winner} wins'
                    result_reason = end_reason or 'Checkmate'
                else:
                    result_headline = 'Draw'
                    result_reason = end_reason or ('Stalemate' if gamestate.stalemate else 'Threefold repetition')
                try:
                    if winner:
                        store.update_win(winner, loser)
                    else:
                        store.update_draw(player1_name, player2_name)
                    if loaded_save_id is not None:
                        store.delete_game(loaded_save_id)
                        loaded_save_id = None
                except Exception as error:
                    print(error)
            elif not game_ended and cpu_move and valid_moves and ai_thread is None:
                depth = white_difficulty if gamestate.white_to_move else black_difficulty
                ai_thread = threading.Thread(target=run_ai, args=(deepcopy(gamestate), deepcopy(valid_moves), depth, game_number), daemon=True)
                ai_thread.start()

        if current_window == 'main menu':
            main_menu.draw_menu(WIN, main_menu.main_menu_text(), 'Chess', True)
        elif current_window == 'data menu':
            main_menu.draw_menu(WIN, main_menu.view_data_select(), 'Player stats')
        elif current_window == 'modify data':
            main_menu.draw_menu(WIN, main_menu.modify_data_select(), 'Manage data')
        elif current_window == 'view specific data':
            action_rect, back_rect = main_menu.draw_view_specific_data(WIN, input_text, status_text)
        elif current_window == 'add data':
            action_rect, back_rect = main_menu.draw_add_data(WIN, input_text, status_text)
        elif current_window == 'delete data':
            action_rect, back_rect = main_menu.draw_delete_data(WIN, input_text, status_text)
        elif current_window == 'delete game data':
            action_rect, back_rect = main_menu.draw_delete_game_data(WIN, input_text, status_text)
        elif current_window == 'change data':
            action_rect, back_rect = main_menu.draw_change_data(WIN, input_text, status_text)
        elif current_window == 'delete all data':
            action_rect, back_rect = main_menu.draw_delete_all_data(WIN, status_text)
        elif current_window == 'delete all game data':
            action_rect, back_rect = main_menu.draw_delete_all_game_data(WIN, status_text)
        elif current_window == 'edit player stats':
            action_rect, back_rect = main_menu.draw_edit_player_stats(WIN, current_player, stats_text, focused_field, status_text)
        elif current_window == 'view all data':
            back_rect = main_menu.draw_view_all_data(WIN, player_rows)
        elif current_window == 'load game':
            save_buttons, back_rect = main_menu.draw_saved_games(WIN, saved_games)
        elif current_window == 'play':
            action_rect, back_rect, white_cpu_rect, black_cpu_rect = main_menu.draw_enter_players_name(WIN, player_names, focused_field, status_text)
        elif current_window == 'game':
            main_menu.clickable = []
            if pygame.time.get_ticks() > temp_msg_until:
                temp_msg = ''
            draw_game_state(WIN, gamestate, player1_name, player2_name, valid_moves, square_selected, ai_thread is not None and not result_shown, temp_msg, main_menu)
            draw_ingame_icons(WIN, main_menu, confirm_action, confirm_until, not result_shown)
            if result_shown:
                rematch_rect, menu_button_rect = draw_game_over(WIN, main_menu, result_headline, result_reason)
        main_menu.update_cursor()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()