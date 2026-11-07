from globals import *

class Main_menu:
    FONT1 = pygame.font.SysFont('cinzel,georgia,times new roman', 96)
    FONT2 = pygame.font.SysFont('cinzel,georgia,times new roman', 34)
    FONT3 = pygame.font.SysFont('segoeui,helvetica,arial', 22)
    FONT4 = pygame.font.SysFont('segoeui,helvetica,arial', 17)
    BUTTON_FONT = pygame.font.SysFont('segoeui,helvetica,arial', 20, bold=True)

    SINGLE_INPUT_RECT = pygame.Rect(152, 250, 496, 46)
    STATS_INPUT_RECTS = [pygame.Rect(272, 226, 376, 44), pygame.Rect(272, 286, 376, 44), pygame.Rect(272, 346, 376, 44)]
    PLAYER_INPUT_RECTS = [pygame.Rect(232, 230, 300, 46), pygame.Rect(232, 300, 300, 46)]
    ROWS_PER_PAGE = 10
    ROW_HEIGHT = 42

    def __init__(self):
        empty = pygame.Rect(0, 0, 0, 0)
        self.play_text_rect = self.data_text_rect = empty
        self.modify_data_text_rect = empty
        self.exit_text_rect = empty
        self.load_game_text_rect = empty
        self.all_data_text_rect = empty
        self.specific_data_text_rect = empty
        self.back_text_rect = empty
        self.add_data_text_rect = empty
        self.delete_data_text_rect = empty
        self.change_data_text_rect = empty
        self.delete_all_data_text_rect = empty
        self.delete_game_data_text_rect = empty
        self.delete_all_game_data_text_rect = empty
        self.clickable = []
        self.scroll = 0
        self.hand_cursor = False

    def update_cursor(self):
        hovering = any(rect.collidepoint(pygame.mouse.get_pos()) for rect in self.clickable)
        if hovering != self.hand_cursor:
            self.hand_cursor = hovering
            try:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hovering else pygame.SYSTEM_CURSOR_ARROW)
            except pygame.error:
                pass

    def get_status_color(self, status_text):
        if 'success' in status_text:
            return GREEN
        if '|' in status_text or 'Edit' in status_text:
            return OFF_WHITE
        return SOFT_RED

    def draw_button(self, win, text, rect, style='normal'):
        hovered = rect.collidepoint(pygame.mouse.get_pos())
        if style == 'important':
            color, text_color = (LIGHT_GREEN if hovered else GREEN), BACKGROUND
        elif style == 'danger':
            color, text_color = (DARK_RED if hovered else PANEL_LIGHT), SOFT_RED
        elif style == 'muted':
            color, text_color = (PANEL_LIGHT if hovered else None), (OFF_WHITE if hovered else MUTED_GRAY)
        else:
            color, text_color = (BORDER if hovered else PANEL_LIGHT), OFF_WHITE
        if color:
            pygame.draw.rect(win, color, rect, border_radius=6)
        label = self.BUTTON_FONT.render(text, True, text_color)
        win.blit(label, label.get_rect(center=rect.center))
        self.clickable.append(rect)
        return rect

    def draw_text_input_box(self, win, text, rect, placeholder='', active=False):
        pygame.draw.rect(win, BACKGROUND, rect, border_radius=6)
        pygame.draw.rect(win, GREEN if active else BORDER, rect, 2 if active else 1, border_radius=6)
        rendered_text = self.FONT3.render(text if text else placeholder, True, OFF_WHITE if text else MUTED_GRAY)
        text_rect = rendered_text.get_rect(midleft=(rect.x + 14, rect.centery))
        win.blit(rendered_text, text_rect)
        if active and (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor_x = text_rect.right + 2 if text else rect.x + 14
            pygame.draw.line(win, OFF_WHITE, (cursor_x, rect.y + 11), (cursor_x, rect.bottom - 11), 2)

    def main_menu_text(self):
        middle = WIN_WIDTH // 2
        self.play_text_rect = pygame.Rect(middle - 170, 300, 340, 52)
        self.load_game_text_rect = pygame.Rect(middle - 170, 364, 340, 52)
        self.data_text_rect = pygame.Rect(middle - 170, 428, 340, 52)
        self.modify_data_text_rect = pygame.Rect(middle - 170, 492, 340, 52)
        self.exit_text_rect = pygame.Rect(middle - 170, 572, 340, 52)
        return [('Play', self.play_text_rect, 'important'), ('Load saved game', self.load_game_text_rect, 'normal'),
                ('Player stats', self.data_text_rect, 'normal'), ('Manage data', self.modify_data_text_rect, 'normal'),
                ('Exit', self.exit_text_rect, 'muted')]

    def view_data_select(self):
        middle = WIN_WIDTH // 2
        self.all_data_text_rect = pygame.Rect(middle - 170, 260, 340, 52)
        self.specific_data_text_rect = pygame.Rect(middle - 170, 324, 340, 52)
        self.back_text_rect = pygame.Rect(middle - 170, 408, 340, 52)
        return [('View all players', self.all_data_text_rect, 'normal'),
                ('Look up a player', self.specific_data_text_rect, 'normal'),
                ('Back', self.back_text_rect, 'muted')]

    def modify_data_select(self):
        middle = WIN_WIDTH // 2
        self.add_data_text_rect = pygame.Rect(middle - 170, 250, 340, 46)
        self.change_data_text_rect = pygame.Rect(middle - 170, 306, 340, 46)
        self.delete_data_text_rect = pygame.Rect(middle - 170, 362, 340, 46)
        self.delete_game_data_text_rect = pygame.Rect(middle - 170, 434, 340, 46)
        self.delete_all_data_text_rect = pygame.Rect(middle - 170, 506, 340, 46)
        self.delete_all_game_data_text_rect = pygame.Rect(middle - 170, 562, 340, 46)
        self.back_text_rect = pygame.Rect(middle - 170, 634, 340, 46)
        return [('Add player', self.add_data_text_rect, 'normal'), ('Edit player', self.change_data_text_rect, 'normal'),
                ('Delete player', self.delete_data_text_rect, 'normal'),('Delete saved game', self.delete_game_data_text_rect, 'normal'),
                ('Delete all players', self.delete_all_data_text_rect, 'danger'),('Delete all saved games', self.delete_all_game_data_text_rect, 'danger'),
                ('Back', self.back_text_rect, 'muted')]

    def draw_menu(self, win, options, title, big=False):
        win.fill(BACKGROUND)
        self.clickable = []
        if big:
            title_text = self.FONT1.render(title, True, OFF_WHITE)
            win.blit(title_text, title_text.get_rect(center=(WIN_WIDTH // 2, 170)))
            pygame.draw.rect(win, GREEN, (WIN_WIDTH // 2 - 24, 232, 48, 3))
        else:
            title_text = self.FONT2.render(title, True, OFF_WHITE)
            win.blit(title_text, title_text.get_rect(center=(WIN_WIDTH // 2, 190)))
        for label, rect, style in options:
            self.draw_button(win, label, rect, style)

    def clicks(self, event, cur):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return cur
        pos = event.pos
        if cur == 'main menu':
            if self.play_text_rect.collidepoint(pos):
                return 'play'
            elif self.load_game_text_rect.collidepoint(pos):
                return 'load game'
            elif self.data_text_rect.collidepoint(pos):
                return 'data menu'
            elif self.modify_data_text_rect.collidepoint(pos):
                return 'modify data'
            elif self.exit_text_rect.collidepoint(pos):
                return 'exit'
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
            elif self.change_data_text_rect.collidepoint(pos):
                return 'change data'
            elif self.delete_data_text_rect.collidepoint(pos):
                return 'delete data'
            elif self.delete_game_data_text_rect.collidepoint(pos):
                return 'delete game data'
            elif self.delete_all_data_text_rect.collidepoint(pos):
                return 'delete all data'
            elif self.delete_all_game_data_text_rect.collidepoint(pos):
                return 'delete all game data'
            elif self.back_text_rect.collidepoint(pos):
                return 'main menu'
        return cur

    def draw_view_specific_data(self, win, input_text, status_text):
        win.fill(BACKGROUND)
        self.clickable = []
        box = pygame.Rect(120, 110, 560, 330)
        pygame.draw.rect(win, PANEL, box, border_radius=10)
        pygame.draw.rect(win, BORDER, box, 1, border_radius=10)
        win.blit(self.FONT2.render('Look up a player', True, OFF_WHITE), (152, 138))
        win.blit(self.FONT4.render('Find a player by name.', True, MUTED_GRAY), (152, 186))
        self.draw_text_input_box(win, input_text, self.SINGLE_INPUT_RECT, 'Player name', True)
        win.blit(self.FONT3.render(status_text, True, self.get_status_color(status_text)), (152, 312))
        back_rect = self.draw_button(win, 'Back', pygame.Rect(152, 364, 110, 44), 'muted')
        search_rect = self.draw_button(win, 'Search', pygame.Rect(498, 364, 150, 44), 'important')
        return search_rect, back_rect

    def draw_add_data(self, win, input_text, status_text):
        win.fill(BACKGROUND)
        self.clickable = []
        box = pygame.Rect(120, 110, 560, 330)
        pygame.draw.rect(win, PANEL, box, border_radius=10)
        pygame.draw.rect(win, BORDER, box, 1, border_radius=10)
        win.blit(self.FONT2.render('Add player', True, OFF_WHITE), (152, 138))
        win.blit(self.FONT4.render('Create a player with a 0-0-0 record.', True, MUTED_GRAY), (152, 186))
        self.draw_text_input_box(win, input_text, self.SINGLE_INPUT_RECT, 'New player name', True)
        win.blit(self.FONT3.render(status_text, True, self.get_status_color(status_text)), (152, 312))
        back_rect = self.draw_button(win, 'Back', pygame.Rect(152, 364, 110, 44), 'muted')
        action_rect = self.draw_button(win, 'Add', pygame.Rect(498, 364, 150, 44), 'important')
        return action_rect, back_rect

    def draw_delete_data(self, win, input_text, status_text):
        win.fill(BACKGROUND)
        self.clickable = []
        box = pygame.Rect(120, 110, 560, 330)
        pygame.draw.rect(win, PANEL, box, border_radius=10)
        pygame.draw.rect(win, BORDER, box, 1, border_radius=10)
        win.blit(self.FONT2.render('Delete player', True, OFF_WHITE), (152, 138))
        win.blit(self.FONT4.render('Removes the player and their record.', True, MUTED_GRAY), (152, 186))
        self.draw_text_input_box(win, input_text, self.SINGLE_INPUT_RECT, 'Player name', True)
        win.blit(self.FONT3.render(status_text, True, self.get_status_color(status_text)), (152, 312))
        back_rect = self.draw_button(win, 'Back', pygame.Rect(152, 364, 110, 44), 'muted')
        action_rect = self.draw_button(win, 'Delete', pygame.Rect(498, 364, 150, 44), 'danger')
        return action_rect, back_rect

    def draw_change_data(self, win, input_text, status_text):
        win.fill(BACKGROUND)
        self.clickable = []
        box = pygame.Rect(120, 110, 560, 330)
        pygame.draw.rect(win, PANEL, box, border_radius=10)
        pygame.draw.rect(win, BORDER, box, 1, border_radius=10)
        win.blit(self.FONT2.render('Edit player', True, OFF_WHITE), (152, 138))
        win.blit(self.FONT4.render('Find the player whose record you want to change.', True, MUTED_GRAY), (152, 186))
        self.draw_text_input_box(win, input_text, self.SINGLE_INPUT_RECT, 'Player name', True)
        win.blit(self.FONT3.render(status_text, True, self.get_status_color(status_text)), (152, 312))
        back_rect = self.draw_button(win, 'Back', pygame.Rect(152, 364, 110, 44), 'muted')
        search_rect = self.draw_button(win, 'Search', pygame.Rect(498, 364, 150, 44), 'important')
        return search_rect, back_rect

    def draw_delete_game_data(self, win, input_text, status_text):
        win.fill(BACKGROUND)
        self.clickable = []
        box = pygame.Rect(120, 110, 560, 330)
        pygame.draw.rect(win, PANEL, box, border_radius=10)
        pygame.draw.rect(win, BORDER, box, 1, border_radius=10)
        win.blit(self.FONT2.render('Delete saved game', True, OFF_WHITE), (152, 138))
        win.blit(self.FONT4.render('Use the number shown in Load Saved Game.', True, MUTED_GRAY), (152, 186))
        self.draw_text_input_box(win, input_text, self.SINGLE_INPUT_RECT, 'Game number', True)
        win.blit(self.FONT3.render(status_text, True, self.get_status_color(status_text)), (152, 312))
        back_rect = self.draw_button(win, 'Back', pygame.Rect(152, 364, 110, 44), 'muted')
        action_rect = self.draw_button(win, 'Delete', pygame.Rect(498, 364, 150, 44), 'danger')
        return action_rect, back_rect

    def draw_delete_all_data(self, win, status_text):
        win.fill(BACKGROUND)
        self.clickable = []
        box = pygame.Rect(120, 110, 560, 290)
        pygame.draw.rect(win, PANEL, box, border_radius=10)
        pygame.draw.rect(win, BORDER, box, 1, border_radius=10)
        win.blit(self.FONT2.render('Delete all players', True, OFF_WHITE), (152, 138))
        win.blit(self.FONT4.render('This permanently deletes every player record.', True, MUTED_GRAY), (152, 186))
        win.blit(self.FONT3.render(status_text, True, self.get_status_color(status_text)), (152, 250))
        back_rect = self.draw_button(win, 'Back', pygame.Rect(152, 310, 110, 44), 'muted')
        action_rect = self.draw_button(win, 'Delete all', pygame.Rect(498, 310, 150, 44), 'danger')
        return action_rect, back_rect

    def draw_delete_all_game_data(self, win, status_text):
        win.fill(BACKGROUND)
        self.clickable = []
        box = pygame.Rect(120, 110, 560, 290)
        pygame.draw.rect(win, PANEL, box, border_radius=10)
        pygame.draw.rect(win, BORDER, box, 1, border_radius=10)
        win.blit(self.FONT2.render('Delete all saved games', True, OFF_WHITE), (152, 138))
        win.blit(self.FONT4.render('This permanently deletes every saved game.', True, MUTED_GRAY), (152, 186))
        win.blit(self.FONT3.render(status_text, True, self.get_status_color(status_text)), (152, 250))
        back_rect = self.draw_button(win, 'Back', pygame.Rect(152, 310, 110, 44), 'muted')
        action_rect = self.draw_button(win, 'Delete all', pygame.Rect(498, 310, 150, 44), 'danger')
        return action_rect, back_rect

    def draw_edit_player_stats(self, win, player_name, stats_text, focused_field, status_text):
        win.fill(BACKGROUND)
        self.clickable = []
        box = pygame.Rect(120, 110, 560, 420)
        pygame.draw.rect(win, PANEL, box, border_radius=10)
        pygame.draw.rect(win, BORDER, box, 1, border_radius=10)
        win.blit(self.FONT2.render('Edit player', True, OFF_WHITE), (152, 138))
        win.blit(self.FONT4.render(player_name, True, MUTED_GRAY), (152, 186))
        labels = ['Wins', 'Losses', 'Draws']
        for i in range(3):
            label = self.FONT3.render(labels[i], True, MUTED_GRAY)
            win.blit(label, label.get_rect(midleft=(152, self.STATS_INPUT_RECTS[i].centery)))
            self.draw_text_input_box(win, stats_text[i], self.STATS_INPUT_RECTS[i], '0', focused_field == i)
        win.blit(self.FONT3.render(status_text, True, self.get_status_color(status_text)), (152, 410))
        back_rect = self.draw_button(win, 'Back', pygame.Rect(152, 452, 110, 44), 'muted')
        save_rect = self.draw_button(win, 'Save', pygame.Rect(528, 452, 120, 44), 'important')
        return save_rect, back_rect

    def draw_enter_players_name(self, win, player_names, focused_field, status_text):
        win.fill(BACKGROUND)
        self.clickable = []
        box = pygame.Rect(120, 110, 560, 400)
        pygame.draw.rect(win, PANEL, box, border_radius=10)
        pygame.draw.rect(win, BORDER, box, 1, border_radius=10)
        win.blit(self.FONT2.render('New game', True, OFF_WHITE), (152, 138))
        win.blit(self.FONT4.render('Enter a name for each side, or pick a CPU level.', True, MUTED_GRAY), (152, 186))
        labels = ['White', 'Black']
        cpu_rects = []
        for i in range(2):
            input_rect = self.PLAYER_INPUT_RECTS[i]
            label = self.FONT3.render(labels[i], True, MUTED_GRAY)
            win.blit(label, label.get_rect(midleft=(152, input_rect.centery)))
            self.draw_text_input_box(win, player_names[i], input_rect, 'Player name', focused_field == i)
            name = player_names[i].strip().lower()
            if name.startswith('cpu'):
                cpu_button = self.draw_button(win, ('CPU ' + name[3:]).strip(), pygame.Rect(input_rect.right + 16, input_rect.y, 100, input_rect.height), 'important')
            else:
                cpu_button = self.draw_button(win, 'Human', pygame.Rect(input_rect.right + 16, input_rect.y, 100, input_rect.height), 'normal')
            cpu_rects.append(cpu_button)
        win.blit(self.FONT4.render('Click Human / CPU to cycle levels. Higher levels think longer.', True, MUTED_GRAY), (152, 356))
        win.blit(self.FONT3.render(status_text, True, self.get_status_color(status_text)), (152, 388))
        back_rect = self.draw_button(win, 'Back', pygame.Rect(152, 436, 110, 44), 'muted')
        start_rect = self.draw_button(win, 'Start game', pygame.Rect(488, 436, 160, 44), 'important')
        return start_rect, back_rect, cpu_rects[0], cpu_rects[1]

    def draw_view_all_data(self, win, rows):
        win.fill(BACKGROUND)
        self.clickable = []
        box = pygame.Rect(120, 90, 560, 640)
        pygame.draw.rect(win, PANEL, box, border_radius=10)
        pygame.draw.rect(win, BORDER, box, 1, border_radius=10)
        win.blit(self.FONT2.render('All players', True, OFF_WHITE), (152, 118))
        self.scroll = min(self.scroll, max(0, len(rows) - self.ROWS_PER_PAGE))
        first = self.scroll
        last = min(len(rows), first + self.ROWS_PER_PAGE)
        if rows:
            win.blit(self.FONT4.render(f'{len(rows)} registered', True, MUTED_GRAY), (152, 166))
            win.blit(self.FONT4.render('NAME', True, MUTED_GRAY), (152, 208))
            for text, right_edge in (('WINS', 500), ('LOSSES', 574), ('DRAWS', 648)):
                header = self.FONT4.render(text, True, MUTED_GRAY)
                win.blit(header, header.get_rect(topright=(right_edge, 208)))
            y = 236
            for row in rows[first:last]:
                middle_y = y + self.ROW_HEIGHT // 2
                name = self.FONT3.render(str(row[0]), True, OFF_WHITE)
                win.blit(name, name.get_rect(midleft=(152, middle_y)))
                for value, right_edge in ((row[1], 500), (row[2], 574), (row[3], 648)):
                    number = self.FONT3.render(str(value), True, OFF_WHITE)
                    win.blit(number, number.get_rect(midright=(right_edge, middle_y)))
                pygame.draw.line(win, BORDER, (152, y + self.ROW_HEIGHT - 1), (648, y + self.ROW_HEIGHT - 1))
                y += self.ROW_HEIGHT
        else:
            message ='No players yet.'
            text = self.FONT3.render(message, True, MUTED_GRAY)
            win.blit(text, text.get_rect(center=(box.centerx, 340)))
        back_rect = self.draw_button(win, 'Back', pygame.Rect(152, 668, 110, 44), 'muted')
        if len(rows) > self.ROWS_PER_PAGE:
            info = self.FONT4.render(f'{first + 1}-{last} of {len(rows)}  -  scroll for more', True, MUTED_GRAY)
            win.blit(info, info.get_rect(midright=(648, back_rect.centery)))
        return back_rect

    def draw_saved_games(self, win, rows):
        win.fill(BACKGROUND)
        self.clickable = []
        box = pygame.Rect(120, 90, 560, 640)
        pygame.draw.rect(win, PANEL, box, border_radius=10)
        pygame.draw.rect(win, BORDER, box, 1, border_radius=10)
        win.blit(self.FONT2.render('Saved games', True, OFF_WHITE), (152, 118))
        self.scroll = min(self.scroll, max(0, len(rows) - self.ROWS_PER_PAGE))
        first = self.scroll
        last = min(len(rows), first + self.ROWS_PER_PAGE)
        buttons = []
        if rows:
            win.blit(self.FONT4.render('Click a game to resume it.', True, MUTED_GRAY), (152, 166))
            y = 214
            for row in rows[first:last]:
                row_rect = pygame.Rect(136, y, 528, self.ROW_HEIGHT - 4)
                if row_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, PANEL_LIGHT, row_rect, border_radius=6)
                number = self.FONT4.render(f'#{row[0]}', True, MUTED_GRAY)
                win.blit(number, number.get_rect(midleft=(row_rect.x + 16, row_rect.centery)))
                players = self.FONT3.render(f'{row[2]}  vs  {row[3]}', True, OFF_WHITE)
                win.blit(players, players.get_rect(midleft=(row_rect.x + 70, row_rect.centery)))
                when = self.FONT4.render(str(row[1]), True, MUTED_GRAY)
                win.blit(when, when.get_rect(midright=(row_rect.right - 16, row_rect.centery)))
                buttons.append((row_rect, row[0]))
                self.clickable.append(row_rect)
                y += self.ROW_HEIGHT
        else:
            message ='No saved games.'
            text = self.FONT3.render(message, True, MUTED_GRAY)
            win.blit(text, text.get_rect(center=(box.centerx, 340)))
        back_rect = self.draw_button(win, 'Back', pygame.Rect(152, 668, 110, 44), 'muted')
        if len(rows) > self.ROWS_PER_PAGE:
            info = self.FONT4.render(f'{first + 1}-{last} of {len(rows)}  -  scroll for more', True, MUTED_GRAY)
            win.blit(info, info.get_rect(midright=(648, back_rect.centery)))
        return buttons, back_rect