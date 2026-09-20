import pygame
from globals import *
from storage import Store
from mainMenu import Main_menu
import ai
import engine
import time
import sys
import os
import subprocess
import threading
from copy import deepcopy

DETAILS = {
    'user': 'root',
    'host': 'localhost',
    'password': '123456789'
}

ai_thread = None
ai_lock = threading.Lock()
pending_cpu_move = None
# game_logger = setup_logger('game', 'game.log')
# ai_logger = setup_logger('ai', 'ai.log')

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Chess")
def text_input(event,text,active,x,y,width,height):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            input_rect = pygame.Rect(x,y,width, height)
            active = input_rect.collidepoint(pos)
        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            elif event.key == pygame.K_RETURN:
                active = False
            else:
                text += event.unicode
        return text, active

    
for piece in ['wP','wR','wN','wB','wQ','wK','bP','bR','bN','bB','bQ','bK']:
    IMAGES[piece] = pygame.transform.scale(pygame.image.load(f'src/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE))
black_resign_image = pygame.transform.scale(pygame.image.load('src/resign.png'), (PADDING-5,PADDING-5))
white_resign_image = pygame.transform.scale(pygame.image.load('src/resign.png'), (PADDING-5,PADDING-5))
draw_image = pygame.transform.scale(pygame.image.load('src/draw.png'),(PADDING-5,PADDING-5))
save_image = pygame.transform.scale(pygame.image.load('src/save.png'),(PADDING-5,PADDING-5))
def get_ingame_icon_rects():
    black_resign_image_rect = black_resign_image.get_rect(center = (WIN_WIDTH-PADDING//2,WIN_HEIGHT//2 - draw_image.get_height()-50))
    white_resign_image_rect = white_resign_image.get_rect(center = (WIN_WIDTH-PADDING//2,WIN_HEIGHT//2 + draw_image.get_height()+50))
    draw_image_rect = draw_image.get_rect(center = (WIN_WIDTH - PADDING//2, WIN_HEIGHT//2))
    save_image_rect = save_image.get_rect(center = (PADDING//2, WIN_HEIGHT//2))
    return (black_resign_image_rect,white_resign_image_rect,draw_image_rect,save_image_rect)
def draw_ingame_icons(win):
    black_resign_image_rect = black_resign_image.get_rect(center = (WIN_WIDTH-PADDING//2,WIN_HEIGHT//2 - draw_image.get_height()-50))
    white_resign_image_rect = white_resign_image.get_rect(center = (WIN_WIDTH-PADDING//2,WIN_HEIGHT//2 + draw_image.get_height()+50))
    draw_image_rect = draw_image.get_rect(center = (WIN_WIDTH - PADDING//2, WIN_HEIGHT//2))
    save_image_rect = save_image.get_rect(center = (PADDING//2, WIN_HEIGHT//2))
    win.blit(black_resign_image,black_resign_image_rect)
    win.blit(white_resign_image,white_resign_image_rect)
    win.blit(draw_image,draw_image_rect)
    win.blit(save_image,save_image_rect)

def draw_board(win):
    for row in range(DIMENTION):
        for col in range(DIMENTION):
            color = WHITE if (row+col)%2==0 else CHESSDOTCOM_GREEN
            pygame.draw.rect(win, color, pygame.Rect(col*SQUARE_SIZE+PADDING, row*SQUARE_SIZE+PADDING, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(win, board):
    for row in range(DIMENTION):
        for col in range(DIMENTION):
            piece = board[row][col]
            if piece != '--':
                win.blit(IMAGES[piece],pygame.Rect(col*SQUARE_SIZE+PADDING, row*SQUARE_SIZE+PADDING, SQUARE_SIZE, SQUARE_SIZE))
def heighlight_square(win,gs,valid_moves,square_selected,move_log):
    if square_selected != ():
        row,col = square_selected
        if gs.board[row][col][0] == ('w' if gs.white_to_move else 'b'):
            s = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE))
            s2 = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE))
            s3 = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE))
            s2.fill(POPPY_RED)
            s.set_alpha(100)
            s.fill(BLUE)
            win.blit(s,(col*SQUARE_SIZE+PADDING, row*SQUARE_SIZE+PADDING))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col and gs.board[move.end_row][move.end_col] == '--':
                    pygame.draw.circle(WIN, LIGHT_GRAY, (move.end_col*SQUARE_SIZE+PADDING+SQUARE_SIZE//2, move.end_row*SQUARE_SIZE+PADDING+SQUARE_SIZE//2), 10)
                    # win.blit(s,(move.end_col*SQUARE_SIZE+PADDING, move.end_row*SQUARE_SIZE+PADDING))
                elif move.start_row == row and move.start_col == col:
                    win.blit(s2,(move.end_col*SQUARE_SIZE+PADDING, move.end_row*SQUARE_SIZE+PADDING))
    if len(move_log) != 0:
        s = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(BLUE)
        move = move_log[-1]
        win.blit(s,(move.start_col*SQUARE_SIZE+PADDING, move.start_row*SQUARE_SIZE+PADDING))
        win.blit(s,(move.end_col*SQUARE_SIZE+PADDING, move.end_row*SQUARE_SIZE+PADDING))
def draw_win_screen(win,game_state, player1_name,player2_name,loaded_save_id,store):
    if game_state.checkmate or game_state.stalemate or game_state.three_fold:
            if game_state.white_to_move and game_state.checkmate:
                winner_text = Main_menu.FONT1.render(f"{player2_name} WINS",1,WHITE)
                store.update_win(player2_name,player1_name)
            elif not game_state.white_to_move and game_state.checkmate:
                winner_text = Main_menu.FONT1.render(f"{player1_name} WINS",1,WHITE)
                store.update_win(player1_name,player2_name)
            else:
                winner_text = Main_menu.FONT1.render(f"DRAW",1,WHITE)
                store.update_draw(player1_name,player2_name)
            winner_text_rect = winner_text.get_rect(center = (WIN_WIDTH//2,WIN_HEIGHT//2))
            s = pygame.Surface((winner_text.get_width()+50,winner_text.get_height()+50))
            s.fill(BLACK)
            win.blit(s,(WIN_WIDTH//2-s.get_width()//2,WIN_HEIGHT//2 - s.get_height()//2))
            win.blit(winner_text,winner_text_rect)
        
            pygame.display.update()
            if loaded_save_id != None:
                store.delete_game(loaded_save_id)
            time.sleep(5)
            pygame.quit()
            script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            subprocess.run([sys.executable] + sys.argv, cwd=script_dir)
            sys.exit(0)
def draw_game_state(win,game_state,player1_name,player2_name,valid_moves,square_selected,loaded_save_id,store):
    win.fill(BLACK)
    player1_label = Main_menu.FONT3.render(player1_name, 1, WHITE)
    player2_label = Main_menu.FONT3.render(player2_name, 1, WHITE)
    player2_rect = player2_label.get_rect(topleft=(PADDING + 2, PADDING/2))
    player1_rect = player1_label.get_rect(topleft=(PADDING + 2, WIN_HEIGHT - PADDING/2 - player1_label.get_height()))
    win.blit(player1_label, player1_rect)
    win.blit(player2_label, player2_rect)
    draw_board(win)
    heighlight_square(win,game_state,valid_moves,square_selected,game_state.move_log)
    draw_pieces(win, game_state.board)
    draw_ingame_icons(win)
    if game_state.checkmate or game_state.stalemate or game_state.three_fold:
        draw_win_screen(win,game_state,player1_name,player2_name,loaded_save_id, store)
def run_ai(gamestate, valid_moves):
    global pending_cpu_move
    # ai_logger.info(f"AI thread started. white_to_move={gamestate.white_to_move}, material_count={gamestate.material_count}")
    try:
        move = ai.choose_move(deepcopy(gamestate), deepcopy(valid_moves))
        # ai_logger.info(f"AI returned move: {move.get_chess_notation() if move else None}")
    except Exception:
        # ai_logger.exception("AI thread crashed during choose_move")
        move = None
    with ai_lock:
        pending_cpu_move = move

def main():
    current_window = 'main menu'
    run = True
    Clock = pygame.time.Clock()
    main_menu = Main_menu()
    gamestate = engine.gameState()
    valid_moves = gamestate.get_valid_moves()
    black_resign_image_rect, white_resign_image_rect, draw_image_rect, save_image_rect = get_ingame_icon_rects()
    move_made = False
    store = Store(DETAILS)

    input_text = ''
    input_active = False
    status_text = 'Enter a player name to search or add.'
    search_rect = None  
    action_rect = None
    delete_all_status_text = ''
    back_rect = None
    start_rect = None
    info_rect = None
    info_active = False
    close_rect = None
    current_player = None
    wins_text = ''
    losses_text = ''
    draws_text = ''
    wins_active = False
    losses_active = False
    draws_active = False
    save_rect = None 
    player1_text = ''
    player1_active = False
    player2_text = ''
    player2_active = False
    player1_name = None
    player2_name = None
    play_status_text = 'Enter both player names and click Start Game.'
    saved_games = []
    save_buttons = []
    loaded_save_id = None
    
    square_selected = ()
    player_clicks = []
    
    white_is_cpu = False
    black_is_cpu = False

    global ai_thread, pending_cpu_move
    while run:
        frame = 0
        Clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                continue
            if current_window != 'game':
                if current_window in ('view specific data', 'add data', 'delete data','delete game data', 'change data', 'edit player stats', 'play'):
                    if current_window in ('view specific data', 'add data', 'delete data','delete game data', 'change data'):
                        input_text, input_active = text_input(event, input_text, input_active, 220, 260, 360, 40)                
                    if current_window == 'edit player stats':
                        wins_text, wins_active = text_input(event, wins_text, wins_active, 350, 200, 100, 40)
                        losses_text, losses_active = text_input(event, losses_text, losses_active, 350, 270, 100, 40)
                        draws_text, draws_active = text_input(event, draws_text, draws_active, 350, 340, 100, 40)
                        
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                            if wins_active:
                                wins_active = False
                                losses_active = True
                            elif losses_active:
                                losses_active = False
                                draws_active = True
                            elif draws_active:
                                draws_active = False
                                wins_active = True
                    if current_window == 'play':
                        player1_text, player1_active = text_input(event, player1_text, player1_active, 350, 200, 200, 40)
                        player2_text, player2_active = text_input(event, player2_text, player2_active, 350, 270, 200, 40)
                        
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                            if player1_active:
                                player1_active = False
                                player2_active = True
                            elif player2_active:
                                player2_active = False
                                player1_active = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos
                        if current_window == 'view specific data':
                            if search_rect and search_rect.collidepoint(pos):
                                name = input_text.strip()
                                result = store.fetch_user(name)
                                if result and result[0]:
                                    row = result[0]
                                    status_text = f"{row[0]} | Wins: {row[1]} | Losses: {row[2]} | Draws: {row[3]}"
                                else:
                                    status_text = 'No player found.'
                            elif back_rect and back_rect.collidepoint(pos):
                                current_window = 'data menu'
                                input_text = ''
                                input_active = False
                                status_text = 'Enter a player name to search or add.'
                        elif current_window == 'add data':
                            if action_rect and action_rect.collidepoint(pos):
                                name = input_text.strip()
                                if name:
                                    added = store.store_user(name)
                                    status_text = 'Player added successfully.' if added else 'That player already exists.'
                                else:
                                    status_text = 'Please enter a name first.'
                            elif back_rect and back_rect.collidepoint(pos):
                                current_window = 'modify data'
                                input_text = ''
                                input_active = False
                                status_text = 'Enter a player name to search or add.'
                        elif current_window == 'delete data':
                            if action_rect and action_rect.collidepoint(pos):
                                name = input_text.strip()
                                if name:
                                    deleted = store.delete_user(name)
                                    status_text = 'Player deleted successfully.' if deleted else 'That player does not exist.'
                                else:
                                    status_text = 'Please enter a name first.'
                            elif back_rect and back_rect.collidepoint(pos):
                                current_window = 'modify data'
                                input_text = ''
                                input_active = False
                                status_text = 'Enter a player name to search or add.'
                        elif current_window == 'delete game data':
                            if status_text == 'Enter a player name to search or add.':
                                status_text = 'Enter game id of the game to delete'
                            if action_rect and action_rect.collidepoint(pos):
                                id = input_text.strip()
                                if id:
                                    deleted = store.delete_game(id)
                                    status_text = 'Game deleted successfully.' if deleted else 'That game does not exist.'
                                else:
                                    status_text = 'Please enter game id first.'
                            elif back_rect and back_rect.collidepoint(pos):
                                current_window = 'modify data'
                                input_text = ''
                                input_active = False
                                status_text = 'Enter a player name to search or add.'
                        elif current_window == 'change data':
                            if search_rect and search_rect.collidepoint(pos):
                                name = input_text.strip()
                                result = store.fetch_user(name)
                                if result and result[0]:
                                    row = result[0]
                                    current_player = row[0]
                                    wins_text = str(row[1])
                                    losses_text = str(row[2])
                                    draws_text = str(row[3])
                                    current_window = 'edit player stats'
                                    input_text = ''
                                    wins_active = True
                                    losses_active = False
                                    draws_active = False
                                    status_text = 'Edit the player stats and click Save.'
                                else:
                                    status_text = 'No player found.'
                            elif back_rect and back_rect.collidepoint(pos):
                                current_window = 'modify data'
                                input_text = ''
                                input_active = False
                                status_text = 'Enter a player name to search or add.'
                        elif current_window == 'edit player stats':
                            pos = event.pos
                            if save_rect and save_rect.collidepoint(pos):
                                try:
                                    wins = int(wins_text)
                                    losses = int(losses_text)
                                    draws = int(draws_text)
                                    updated = store.update_user_stats(current_player, wins, losses, draws)
                                    if updated:
                                        status_text = 'Player stats updated successfully.'
                                        current_window = 'modify data'
                                        input_text = ''
                                        wins_text = ''
                                        losses_text = ''
                                        draws_text = ''
                                        wins_active = False
                                        losses_active = False
                                        draws_active = False
                                    else:
                                        status_text = 'Could not update player stats.'
                                except ValueError:
                                    status_text = 'Please enter valid numbers for stats.'
                            elif back_rect and back_rect.collidepoint(pos):
                                current_window = 'change data'
                                input_text = ''
                                wins_text = ''
                                losses_text = ''
                                draws_text = ''
                                wins_active = False
                                losses_active = False
                                draws_active = False
                                status_text = 'Enter a player name to search or add.'
                        elif current_window == 'play':
                            if start_rect and start_rect.collidepoint(pos):
                                name1 = player1_text.strip()
                                name2 = player2_text.strip()
                                if name1 == name2 and name1:
                                    play_status_text = 'Players must have different names.'
                                elif name1 and name2:
                                    store.store_user(name1)
                                    store.store_user(name2)
                                    player1_name = name1
                                    player2_name = name2
                                    white_is_cpu = player1_name.lower() == 'cpu'
                                    black_is_cpu = player2_name.lower() == 'cpu'
                                    play_status_text = f'Ready! {name1} vs {name2}'
                                    current_window = 'game'
                                else:
                                    play_status_text = 'Please enter both player names.'
                            elif back_rect and back_rect.collidepoint(pos):
                                current_window = 'main menu'
                                player1_text = ''
                                player2_text = ''
                                player1_active = False
                                player2_active = False
                                play_status_text = 'Enter both player names and click Start Game.'
                            elif info_rect and info_rect.collidepoint(pos):
                                info_active = True
                            elif close_rect and close_rect.collidepoint(pos) and info_active:
                                info_active = False
                    if event.type == pygame.MOUSEMOTION:
                        pos = event.pos
                        if current_window == 'view specific data':
                            hover = (search_rect and search_rect.collidepoint(pos)) or (back_rect and back_rect.collidepoint(pos))
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW)
                        elif current_window == 'add data':
                            hover = (action_rect and action_rect.collidepoint(pos)) or (back_rect and back_rect.collidepoint(pos))
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW)
                        elif current_window == 'delete data':
                            hover = (action_rect and action_rect.collidepoint(pos)) or (back_rect and back_rect.collidepoint(pos))
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW)
                        elif current_window == 'delete game data':
                            hover = (action_rect and action_rect.collidepoint(pos)) or (back_rect and back_rect.collidepoint(pos))
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW)
                        elif current_window == 'change data':
                            hover = (search_rect and search_rect.collidepoint(pos)) or (back_rect and back_rect.collidepoint(pos))
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW)
                        elif current_window == 'edit player stats':
                            hover = (save_rect and save_rect.collidepoint(pos)) or (back_rect and back_rect.collidepoint(pos))
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW)
                        elif current_window == 'play':
                            hover = (start_rect and start_rect.collidepoint(pos)) or (back_rect and back_rect.collidepoint(pos)) or \
                            (info_rect and info_rect.collidepoint(pos)) or (info_active and close_rect and close_rect.collidepoint(pos))
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW)
                    continue

                if current_window == 'view all data' and event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect and back_rect.collidepoint(event.pos):
                        current_window = 'data menu'
                        continue
                if current_window == 'load game' and event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect and back_rect.collidepoint(event.pos):
                        current_window = 'main menu'
                        continue
                    for button,id in save_buttons:
                        if button.collidepoint(event.pos):
                            gamestate = store.load_game(id)
                            valid_moves = gamestate.get_valid_moves()
                            loaded_save_id = id
                            for save in saved_games:
                                if save[0] == id:
                                    player1_name = save[2]
                                    player2_name = save[3]
                                    white_is_cpu = player1_name.lower() == 'cpu'
                                    black_is_cpu = player2_name.lower() == 'cpu'
                                    break
                            current_window = 'game'
                if current_window == 'delete all data' and event.type == pygame.MOUSEBUTTONDOWN:
                    if action_rect and action_rect.collidepoint(event.pos):
                        deleted = store.delete_all_users()
                        delete_all_status_text = 'All player data deleted successfully.' if deleted else 'Could not delete all player data.'
                    elif back_rect and back_rect.collidepoint(event.pos):
                        current_window = 'modify data'
                        delete_all_status_text = ''
                    continue
                if current_window == "delete all game data" and event.type == pygame.MOUSEBUTTONDOWN:
                    if action_rect and action_rect.collidepoint(event.pos):
                        deleted = store.delete_all_games()
                        delete_all_status_text = 'All game data deleted successfully.' if deleted else 'Could not delete all game data.'
                    elif back_rect and back_rect.collidepoint(event.pos):
                        current_window = 'modify data'
                        delete_all_status_text = ''
                    continue
                if current_window == 'view all data' and event.type == pygame.MOUSEMOTION:
                    hover = back_rect and back_rect.collidepoint(event.pos)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW)

                if current_window == 'load game' and event.type == pygame.MOUSEMOTION:
                    hover = (back_rect and back_rect.collidepoint(event.pos)) or any(button.collidepoint(event.pos) for button, id in save_buttons)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW)

                if current_window == 'delete all data' and event.type == pygame.MOUSEMOTION:
                    hover = (action_rect and action_rect.collidepoint(event.pos)) or (back_rect and back_rect.collidepoint(event.pos))
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW)

                if current_window == "delete all game data" and event.type == pygame.MOUSEMOTION:
                    hover = (action_rect and action_rect.collidepoint(event.pos)) or (back_rect and back_rect.collidepoint(event.pos))
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW)

                if current_window in ('main menu', 'data menu', 'modify data') and event.type == pygame.MOUSEMOTION:
                    main_menu.set_cursor(current_window, event.pos)

                current_window = main_menu.clicks(event, current_window)
                if current_window == 'exit':
                    run = False
            elif current_window == 'game':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if BOARD_WIDTH+PADDING > pos[0] > PADDING and BOARD_HEIGHT+PADDING > pos[1] > PADDING and ai_thread is None:
                        col = (pos[0]-PADDING)//SQUARE_SIZE
                        row = (pos[1]-PADDING)//SQUARE_SIZE
                        if square_selected == (row,col):
                            square_selected = ()
                            player_clicks = []
                        else:
                            square_selected = (row, col)
                            player_clicks.append(square_selected)
                        if len(player_clicks) == 2: #after second click
                            move = engine.Move(player_clicks[0], player_clicks[1], gamestate.board) 
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    print(move.get_chess_notation())
                                    # game_logger.info(f"Move applied (human): {move.get_chess_notation()} | white_to_move was {gamestate.white_to_move}")
                                    gamestate.make_move(valid_moves[i])
                                    move_made = True
                                    player_clicks = [] 
                                    square_selected = ()
                                    frame = 15
                            if not move_made:
                                player_clicks = [square_selected]
                    else:
                        if black_resign_image_rect.collidepoint(pos):
                            gamestate.checkmate = True
                            gamestate.white_to_move = False
                        elif white_resign_image_rect.collidepoint(pos):
                            gamestate.checkmate = True
                            gamestate.white_to_move = True
                        elif draw_image_rect.collidepoint(pos):
                            gamestate.stalemate = True
                        elif save_image_rect.collidepoint(pos):
                            store.save_game(player1_name,player2_name, gamestate)
                                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z and ai_thread is None:
                    # game_logger.info(f"Undo triggered by user. ai_thread_alive={ai_thread is not None}")
                    gamestate.undo_move()
                    if black_is_cpu or white_is_cpu:
                        gamestate.undo_move()
                    move_made = True
                
        if move_made:
            valid_moves = gamestate.get_valid_moves()
            move_made = False
        if current_window == 'game' and not gamestate.checkmate and not gamestate.stalemate:
            cpu_to_move = (gamestate.white_to_move and white_is_cpu) or (not gamestate.white_to_move and black_is_cpu)
            if cpu_to_move and valid_moves and ai_thread is None:
                ai_thread = threading.Thread(target=run_ai, args=(gamestate, valid_moves), daemon=True)
                ai_thread.start()
            if ai_thread is not None and not ai_thread.is_alive():
                with ai_lock:
                    move_to_make = pending_cpu_move
                    pending_cpu_move = None
                ai_thread = None
                if move_to_make is not None:
                    # game_logger.info(f"Move applied (AI): {move_to_make.get_chess_notation()} | white_to_move was {gamestate.white_to_move}")
                    gamestate.make_move(move_to_make)
                    valid_moves = gamestate.get_valid_moves()
                    move_made = True
                else:
                    # game_logger.warning("AI thread finished but returned no move (pending_cpu_move was None)")
                    ...
        if current_window == 'main menu':
            main_menu.draw_main_menu(WIN, main_menu.main_menu_text())
        elif current_window == 'data menu':
            main_menu.draw_main_menu(WIN, main_menu.view_data_select())
        elif current_window == 'modify data':
            main_menu.draw_main_menu(WIN, main_menu.modify_data_select())
        elif current_window == 'view specific data':
            search_rect, back_rect = main_menu.draw_view_specific_data(WIN, input_text, input_active, status_text)
        elif current_window == 'add data':
            action_rect, back_rect = main_menu.draw_add_data(WIN, input_text, input_active, status_text)
        elif current_window == 'delete data':
            action_rect, back_rect = main_menu.draw_delete_data(WIN, input_text, input_active, status_text)
        elif current_window == 'delete game data':
            action_rect, back_rect = main_menu.draw_delete_game_data(WIN,input_text,input_active,status_text)
        elif current_window == 'delete all game data':
            action_rect, back_rect = main_menu.draw_delete_all_game_data(WIN, delete_all_status_text)
        elif current_window == 'delete all data':
            action_rect, back_rect = main_menu.draw_delete_all_data(WIN, delete_all_status_text)
        elif current_window == 'change data':
            search_rect, back_rect = main_menu.draw_change_data(WIN, input_text, input_active, status_text)
        elif current_window == 'edit player stats':
            save_rect, back_rect = main_menu.draw_edit_player_stats(WIN, current_player, wins_text, losses_text, draws_text, wins_active, losses_active, draws_active, status_text)
        elif current_window == 'view all data':
            try:
                rows = store.fetchall()
                back_rect = main_menu.draw_view_all_data(WIN, rows)
            except Exception:
                back_rect = main_menu.draw_view_all_data(WIN, [])
        elif current_window == 'load game':
            try:
                saved_games = store.get_saved_games()
                save_buttons, back_rect = main_menu.draw_saved_games(WIN,saved_games)
            except Exception:
                save_buttons, back_rect = main_menu.draw_saved_games(WIN,[])
        elif current_window == 'play':
            if not info_active:
                start_rect, back_rect, info_rect = main_menu.draw_enter_players_name(WIN, player1_text, player2_text, play_status_text, 'player1' if player1_active else 'player2' if player2_active else None)
            else:
                start_rect, back_rect, info_rect, close_rect = main_menu.draw_enter_players_name(WIN, player1_text, player2_text, play_status_text, 'player1' if player1_active else 'player2' if player2_active else None,True)
        elif current_window == 'game':
            draw_game_state(WIN, gamestate, player1_name, player2_name,valid_moves,square_selected,loaded_save_id,store)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
