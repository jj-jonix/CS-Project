from globals import *

class Main_menu:
    FONT1 = pygame.font.SysFont('cinzel', 140)
    FONT2 = pygame.font.SysFont('cinzel', 50)
    FONT3 = pygame.font.SysFont('cinzel', 30)
    FONT4 = pygame.font.SysFont('cinzel', 25)

    def __init__(self):
        self.play_text_rect = None
        self.data_text_rect = None
        self.modify_data_text_rect = None
        self.exit_text_rect = None
        self.load_game_text_rect = None
        self.all_data_text_rect = None
        self.specific_data_text_rect = None
        self.back_text_rect = None
        self.add_data_text_rect = None
        self.delete_data_text_rect = None
        self.change_data_text_rect = None
        self.delete_all_data_text_rect = None
        self.delete_game_data_text_rect = None
        self.delete_all_game_data_text_rect = None
        

    def draw_text_input_box(self, win, font, text, x, y, width, height, prompt='', active=False):
        input_rect = pygame.Rect(x, y, width, height)
        border_color = WHITE if active else GRAY 
        pygame.draw.rect(win, border_color, input_rect, 2)
        display_text = text if text else prompt
        text_color = WHITE if text else LIGHT_GRAY
        rendered_text = font.render(display_text, 1, text_color)
        text_rect = rendered_text.get_rect(topleft=(x+5,y+10))
        win.blit(rendered_text, text_rect)
        if active:
            cursor_x = text_rect.right+2
            pygame.draw.line(win,WHITE,(cursor_x,y+5),(cursor_x,y+height-5), 2)
            
    def main_menu_text(self):
        self.chess_text = self.FONT1.render('CHESS!',1,WHITE,)
        self.chess_text_rect = self.chess_text.get_rect(center = (WIN_WIDTH//2,200))
        self.play_text = self.FONT2.render('Play',1,WHITE)
        self.play_text_rect = self.play_text.get_rect(center = (WIN_WIDTH//2,350))
        self.data_text = self.FONT2.render('View Player Data',1,WHITE)
        self.data_text_rect = self.data_text.get_rect(center = (WIN_WIDTH//2,430))
        self.modify_data_text = self.FONT2.render('Modify Data',1,WHITE)
        self.modify_data_text_rect = self.modify_data_text.get_rect(center = (WIN_WIDTH//2,510))
        self.exit_text = self.FONT2.render('Exit',1,WHITE)
        self.exit_text_rect = self.exit_text.get_rect(center = (WIN_WIDTH//2,670))
        self.load_game_text = self.FONT2.render('Load Saved Game',1,WHITE)
        self.load_game_text_rect = self.load_game_text.get_rect(center=(WIN_WIDTH//2,590))
        return [(self.chess_text,self.chess_text_rect),(self.play_text,self.play_text_rect),(self.data_text,self.data_text_rect),
                (self.modify_data_text,self.modify_data_text_rect),(self.exit_text,self.exit_text_rect),(self.load_game_text,self.load_game_text_rect)]
    
    def draw_main_menu(self,win,options):
        win.fill(BLACK)
        for text in options:
            win.blit(text[0],text[1])

    def clicks(self, event, cur):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return cur

        pos = event.pos

        if cur == 'main menu':
            if self.play_text_rect.collidepoint(pos):
                return 'play'
            elif self.data_text_rect.collidepoint(pos):
                return 'data menu'
            elif self.modify_data_text_rect.collidepoint(pos):
                return 'modify data'
            elif self.exit_text_rect.collidepoint(pos):
                return 'exit'
            elif self.load_game_text_rect.collidepoint(pos):
                return 'load game'
        elif cur == 'data menu':
            if self.all_data_text_rect.collidepoint(pos):
                return 'view all data'
            elif self.specific_data_text_rect.collidepoint(pos):
                return 'view specific data'
            elif self.back_text_rect.collidepoint(pos):
                return 'main menu'
        elif cur == 'modify data':
            if self.add_data_text_rect.collidepoint(pos):
                return 'add data'
            elif self.delete_data_text_rect.collidepoint(pos):
                return 'delete data'
            elif self.change_data_text_rect.collidepoint(pos):
                return 'change data'
            elif self.back_text_rect.collidepoint(pos):
                return 'main menu'
            elif self.delete_all_data_text_rect.collidepoint(pos):
                return 'delete all data'
            elif self.delete_game_data_text_rect.collidepoint(pos):
                return 'delete game data'
            elif self.delete_all_game_data_text_rect.collidepoint(pos):
                return 'delete all game data'
        return cur
    def set_cursor(self, cur, mouse_pos):
        rects = []
        if cur == 'main menu':
            rects = [self.play_text_rect, self.data_text_rect, self.modify_data_text_rect,
                      self.exit_text_rect, self.load_game_text_rect]
        elif cur == 'data menu':
            rects = [self.all_data_text_rect, self.specific_data_text_rect, self.back_text_rect]
        elif cur == 'modify data':
            rects = [self.add_data_text_rect, self.delete_data_text_rect, self.change_data_text_rect,
                      self.back_text_rect, self.delete_all_data_text_rect, self.delete_game_data_text_rect,
                      self.delete_all_game_data_text_rect]
        hover = any(r and r.collidepoint(mouse_pos) for r in rects)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW)
    def view_data_select(self):
        all_data_text = self.FONT2.render('View All Player Data',1,WHITE)
        self.all_data_text_rect = all_data_text.get_rect(center = (WIN_WIDTH//2,350))
        specific_data_text = self.FONT2.render('View Specific Player Data',1,WHITE)
        self.specific_data_text_rect = specific_data_text.get_rect(center = (WIN_WIDTH//2,430))
        back_text = self.FONT2.render('Back',1,WHITE)
        self.back_text_rect = back_text.get_rect(center = (WIN_WIDTH//2,510))
        return [(all_data_text,self.all_data_text_rect),(specific_data_text,self.specific_data_text_rect),(back_text,self.back_text_rect)]


    def modify_data_select(self):
        add_data_text = self.FONT2.render('Add Player Data',1,WHITE)
        self.add_data_text_rect = add_data_text.get_rect(center = (WIN_WIDTH//2,250))
        delete_data_text = self.FONT2.render('Delete Player Data',1,WHITE)
        self.delete_data_text_rect = delete_data_text.get_rect(center = (WIN_WIDTH//2,320))
        change_data_text = self.FONT2.render('Change Player Data',1,WHITE)
        self.change_data_text_rect = change_data_text.get_rect(center = (WIN_WIDTH//2,390))
        back_text = self.FONT2.render('Back',1,WHITE)
        self.back_text_rect = back_text.get_rect(center = (WIN_WIDTH//2,680))
        self.delete_all_data_text = self.FONT2.render('Delete All Player Data',1,WHITE)
        self.delete_all_data_text_rect = self.delete_all_data_text.get_rect(center = (WIN_WIDTH//2,460))
        self.delete_game_data_text = self.FONT2.render('Delete Game Data',1,WHITE)
        self.delete_game_data_text_rect = self.delete_game_data_text.get_rect(center = (WIN_WIDTH//2,530))
        self.delete_all_game_data_text = self.FONT2.render('Delete All Game Data',1,WHITE)
        self.delete_all_game_data_text_rect = self.delete_all_game_data_text.get_rect(center = (WIN_WIDTH//2, 600))
        return [(add_data_text,self.add_data_text_rect),(delete_data_text,self.delete_data_text_rect),
        (change_data_text,self.change_data_text_rect),(back_text,self.back_text_rect),(self.delete_all_data_text,self.delete_all_data_text_rect),
        (self.delete_game_data_text,self.delete_game_data_text_rect),(self.delete_all_game_data_text,self.delete_all_game_data_text_rect)]
        
    def draw_view_data(self,win):
        win.fill(BLACK)
        for text in self.view_data_select():
            win.blit(text[0],text[1])

    def draw_modify_data(self,win):
        win.fill(BLACK)
        for text in self.modify_data_select():
            win.blit(text[0],text[1])

    def draw_button(self, win, font, text, x, y, width, height, color=None):
        label = font.render(text, 1, color if color else WHITE )
        rect = label.get_rect(center=(x + width // 2, y + height // 2))
        win.blit(label, rect)
        return rect

    def draw_view_specific_data(self, win, input_text, input_active, status_text):
        win.fill(BLACK)
        title = self.FONT2.render('Look up player data', 1, WHITE)
        subtitle = self.FONT3.render('Type the player name, then press Search.', 1, WHITE)
        win.blit(title, (WIN_WIDTH//2-title.get_width()//2, 120))
        win.blit(subtitle, (WIN_WIDTH//2-subtitle.get_width()//2, 170))
        self.draw_text_input_box(win, self.FONT3, input_text, 220, 260, 360, 40, prompt='Player name', active=input_active)
        search_rect = self.draw_button(win, self.FONT3, 'Search', 250, 340, 150, 42)
        back_rect = self.draw_button(win, self.FONT3, 'Back', 420, 340, 120, 42)
        status = self.FONT3.render(status_text, 1, WHITE)
        win.blit(status, (WIN_WIDTH//2-status.get_width()//2, 420))
        return search_rect, back_rect

    def draw_add_data(self, win, input_text, input_active, status_text):
        win.fill(BLACK)
        title = self.FONT2.render('Add player data', 1, WHITE)
        subtitle = self.FONT3.render('Type the player name, then press Add.', 1, WHITE)
        win.blit(title, (WIN_WIDTH//2-title.get_width()//2, 120))
        win.blit(subtitle, (WIN_WIDTH//2-subtitle.get_width()//2, 170))
        self.draw_text_input_box(win, self.FONT3, input_text, 220, 260, 360, 40, prompt='New player name', active=input_active)
        action_rect = self.draw_button(win, self.FONT3, 'Add', 250, 340, 120, 42)
        back_rect = self.draw_button(win, self.FONT3, 'Back', 390, 340, 120, 42)
        status = self.FONT3.render(status_text, 1, WHITE)
        win.blit(status, (WIN_WIDTH//2-status.get_width()//2, 420))
        return action_rect, back_rect

    def draw_view_all_data(self, win, rows):
        win.fill(BLACK)
        title = self.FONT2.render('All player data', 1, WHITE)
        win.blit(title, (180, 120))
        y = 180
        if rows:
            for row in rows:
                line = self.FONT3.render(f"{row[0]} | Wins: {row[1]} | Losses: {row[2]} | Draws: {row[3]}", 1, WHITE)
                win.blit(line, (180, y))
                y += 30
        else:
            msg = self.FONT3.render('No player data available.', 1, WHITE)
            win.blit(msg, (180, 180))
        back_rect = self.draw_button(win, self.FONT3, 'Back', 300, 520, 120, 42)
        return back_rect
    
    def draw_delete_data(self, win, input_text, input_active, status_text):
        win.fill(BLACK)
        title = self.FONT2.render('Delete player data', 1, WHITE)
        subtitle = self.FONT3.render('Type the player name, then press Delete.', 1, WHITE)
        win.blit(title, (WIN_WIDTH//2-title.get_width()//2, 120))
        win.blit(subtitle, (WIN_WIDTH//2-subtitle.get_width()//2, 170))
        self.draw_text_input_box(win, self.FONT3, input_text, 220, 260, 360, 40, prompt='Player name', active=input_active)
        action_rect = self.draw_button(win, self.FONT3, 'Delete', 250, 340, 120, 42)
        back_rect = self.draw_button(win, self.FONT3, 'Back', 390, 340, 120, 42)
        status = self.FONT3.render(status_text, 1, WHITE)
        win.blit(status, (WIN_WIDTH//2-status.get_width()//2, 420))
        return action_rect, back_rect
    
    def draw_change_data(self, win, input_text, input_active, status_text):
        win.fill(BLACK)
        title = self.FONT2.render('Change player data', 1, WHITE)
        subtitle = self.FONT3.render('Type the player name, then press Search.', 1, WHITE)
        win.blit(title, (WIN_WIDTH//2-title.get_width()//2, 120))
        win.blit(subtitle, (WIN_WIDTH//2-subtitle.get_width()//2, 170))
        self.draw_text_input_box(win, self.FONT3, input_text, 220, 260, 360, 40, prompt='Player name', active=input_active)
        search_rect = self.draw_button(win, self.FONT3, 'Search', 250, 340, 150, 42)
        back_rect = self.draw_button(win, self.FONT3, 'Back', 420, 340, 120, 42)
        status = self.FONT3.render(status_text, 1, WHITE)
        win.blit(status, (WIN_WIDTH//2-status.get_width()//2, 420))
        return search_rect, back_rect
    
    def draw_edit_player_stats(self, win, player_name, wins_text, losses_text, draws_text, wins_active, losses_active, draws_active, status_text):
        win.fill(BLACK)
        title = self.FONT2.render('Edit Player Stats', 1, WHITE)
        subtitle = self.FONT3.render(f'Player: {player_name}', 1, WHITE)
        win.blit(title, (WIN_WIDTH//2-title.get_width()//2, 80))
        win.blit(subtitle, (180, 140))
        wins_label = self.FONT3.render('Wins:', 1, WHITE)
        win.blit(wins_label, (180, 200))
        self.draw_text_input_box(win, self.FONT3, wins_text, 350, 200, 100, 40, active=wins_active)
        losses_label = self.FONT3.render('Losses:', 1, WHITE)
        win.blit(losses_label, (180, 270))
        self.draw_text_input_box(win, self.FONT3, losses_text, 350, 270, 100, 40, active=losses_active)
        draws_label = self.FONT3.render('Draws:', 1, WHITE)
        win.blit(draws_label, (180, 340))
        self.draw_text_input_box(win, self.FONT3, draws_text, 350, 340, 100, 40, active=draws_active)
        save_rect = self.draw_button(win, self.FONT3, 'Save', 250, 470, 100, 42)
        back_rect = self.draw_button(win, self.FONT3, 'Back', 370, 470, 100, 42)
        status = self.FONT3.render(status_text, 1, WHITE)
        win.blit(status, (WIN_WIDTH//2-status.get_width()//2, 420))
        return save_rect, back_rect
    
    def draw_enter_players_name(self, win, player1_text, player2_text, status_text, active_player, info_active = False):
        win.fill(BLACK)
        title = self.FONT2.render('Enter Player Names', 1, WHITE)
        win.blit(title, (180, 120))       
        player1_label = self.FONT3.render('White:', 1, WHITE)
        win.blit(player1_label, (180, 200))
        self.draw_text_input_box(win, self.FONT3, player1_text, 350, 190, 200, 40, prompt='White', active=active_player == 'player1')
        player2_label = self.FONT3.render('Black:', 1, WHITE)
        win.blit(player2_label, (180, 270))
        self.draw_text_input_box(win, self.FONT3, player2_text, 350, 260, 200, 40, prompt='Black', active=active_player == 'player2')
        status = self.FONT3.render(status_text, 1, WHITE)
        win.blit(status, (180, 340))
        start_rect = self.draw_button(win, self.FONT3, 'Start Game', 250, 380, 150, 42)
        back_rect = self.draw_button(win, self.FONT3, 'Back', 420, 380, 120, 42)
        info_rect = self.draw_button(win,self.FONT1, '?', WIN_WIDTH-140, WIN_HEIGHT-140, 150,150)
        if info_active:
            lines = [
                "Enter one of the player names as cpu to play against the AI.",
                "Put a number after cpu to select the difficulty.",
                "For example, cpu1, cpu2, etc.",
                "",
                "",
                "Every difficulty level increases the time taken to make moves.",
                "Max reccomended difficulty is 6"
            ]
            info_texts = [self.FONT3.render(line, 1, WHITE) for line in lines]
            text_width = max(text.get_width() for text in info_texts)
            line_height = self.FONT3.get_height()
            text_height = line_height * 6
            bg_blurr = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            bg_blurr.set_alpha(200)
            bg_blurr.fill(BLACK)
            win.blit(bg_blurr, (0, 0))  
            info_box = pygame.Rect(WIN_WIDTH//2-text_width//2-50, WIN_HEIGHT//2-text_height//2-50, text_width + 100, text_height + 100)
            info_box_outline = pygame.Rect(info_box.left-4, info_box.top-4, info_box.width+8, info_box.height+8)
            pygame.draw.rect(win, WHITE, info_box_outline)
            pygame.draw.rect(win, BLACK, info_box)
            for i, text in enumerate(info_texts):
                text_rect = text.get_rect(centerx = info_box.centerx, top=info_box.top + 50 + i * line_height)
                win.blit(text, text_rect)
            close_rect = self.draw_button(win, self.FONT2, 'X', info_box.right - 50, info_box.top +5, 50, 50, RED)
            return None,None,None,close_rect 
        return start_rect, back_rect, info_rect

    def draw_delete_all_data(self, win,status_text):
        win.fill(BLACK)
        title = self.FONT2.render('Delete All Player Data', 1, WHITE)
        subtitle = self.FONT3.render('This will delete all player data. Are you sure?', 1, WHITE)
        win.blit(title, (WIN_WIDTH//2-title.get_width()//2, 120))
        win.blit(subtitle, (WIN_WIDTH//2-subtitle.get_width()//2, 170))
        action_rect = self.draw_button(win, self.FONT3, 'Delete All', 250, 240, 150, 42)
        back_rect = self.draw_button(win, self.FONT3, 'Back', 420, 240, 120, 42)
        status = self.FONT3.render(status_text, 1, WHITE)
        win.blit(status, (WIN_WIDTH//2-status.get_width()//2, 420))
        return action_rect, back_rect
    
    def draw_saved_games(self, win, rows):
        win.fill(BLACK)
        title = self.FONT2.render("Saved Games",1,WHITE)
        win.blit(title,(180,120))
        buttons = []
        y = 180
        if rows:
            for row in rows:
                text = self.FONT3.render(f"{row[0]}) {row[2]} vs {row[3]} | {row[1]}",1,WHITE)
                game_rect = self.draw_button(win,self.FONT3,f"{row[0]}) {row[2]} vs {row[3]} | {row[1]}",180,y,text.get_width(),text.get_height())
                buttons.append((game_rect,row[0]))
                y += 30
        else:
            msg = self.FONT3.render('No game data available.', 1, WHITE)
            win.blit(msg, (180, 180))
        back_rect = self.draw_button(win, self.FONT3, 'Back', 300, 520, 120, 42)
        return buttons, back_rect
    def draw_delete_game_data(self, win, input_text, input_active, status_text):
        win.fill(BLACK)
        title = self.FONT2.render('Delete game data', 1, WHITE)
        subtitle = self.FONT3.render('Type the game id, then press Delete.', 1, WHITE)
        win.blit(title, (WIN_WIDTH//2-title.get_width()//2, 120))
        win.blit(subtitle, (WIN_WIDTH//2-subtitle.get_width()//2, 170))
        self.draw_text_input_box(win, self.FONT3, input_text, 220, 260, 360, 40, prompt='game id', active=input_active)
        action_rect = self.draw_button(win, self.FONT3, 'Delete', 250, 340, 120, 42)
        back_rect = self.draw_button(win, self.FONT3, 'Back', 390, 340, 120, 42)
        status = self.FONT3.render(status_text, 1, WHITE)
        win.blit(status, (WIN_WIDTH//2-status.get_width()//2, 420))
        return action_rect, back_rect
    def draw_delete_all_game_data(self, win, status_text):
        win.fill(BLACK)
        title = self.FONT2.render('Delete All game Data', 1, WHITE)
        subtitle = self.FONT3.render('This will delete all game data. Are you sure?', 1, WHITE)
        win.blit(title, (WIN_WIDTH//2-title.get_width()//2, 120))
        win.blit(subtitle, (WIN_WIDTH//2-subtitle.get_width()//2, 170))
        action_rect = self.draw_button(win, self.FONT3, 'Delete All', 250, 240, 150, 42)
        back_rect = self.draw_button(win, self.FONT3, 'Back', 420, 240, 120, 42)
        status = self.FONT3.render(status_text, 1, WHITE)
        win.blit(status, (WIN_WIDTH//2-status.get_width()//2, 420))
        return action_rect, back_rect