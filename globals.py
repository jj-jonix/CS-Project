import pygame
import random
import logging
from logging.handlers import RotatingFileHandler
import os
pygame.font.init()
PADDING = 40
BOARD_WIDTH = 800-80
BOARD_HEIGHT = 800-80
DIMENTION = 8
WIN_WIDTH = BOARD_WIDTH + PADDING*2
WIN_HEIGHT = BOARD_HEIGHT +  PADDING*2
SQUARE_SIZE = BOARD_WIDTH//DIMENTION

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (100,100,100)
LIGHT_GRAY = (200,200,200)
CHESSDOTCOM_GREEN = (78,120,55)
BLUE = (53, 204, 240)
IMAGES = {}

PIECES = ['wP','wN','wB','wR','wQ','wK','bP','bN','bB','bR','bQ','bK']
ZOBRIST_TABLE = {}
rng = random.Random(67)
for row in range(8):
    for col in range(8):
        for piece in PIECES:
            ZOBRIST_TABLE[(row,col,piece)] = rng.getrandbits(64)
ZOBRIST_TABLE['turn'] = rng.getrandbits(64)
ZOBRIST_TABLE['wks'] = rng.getrandbits(64)
ZOBRIST_TABLE['wqs'] = rng.getrandbits(64)
ZOBRIST_TABLE['bks'] = rng.getrandbits(64)
ZOBRIST_TABLE['bqs'] = rng.getrandbits(64)
ZOBRIST_TABLE['ep'] = {col: rng.getrandbits(64) for col in range(8)}


def handle_text_input(event, text, active, x, y, width, height):
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = event.pos
        input_rect = pygame.Rect(x, y, width, height)
        active = input_rect.collidepoint(pos)
    
    if event.type == pygame.KEYDOWN and active:
        if event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        elif event.key == pygame.K_RETURN:
            active = False
        else:
            text += event.unicode
    
    return text, active

def draw_text_input_box(win, font, text, x, y, width, height, prompt='', active=False):
    input_rect = pygame.Rect(x, y, width, height)
    border_color = WHITE if active else GRAY

    pygame.draw.rect(win, border_color, input_rect, 2)
    
    display_text = text if text else prompt
    text_color = WHITE if text else LIGHT_GRAY
    rendered_text = font.render(display_text, 1, text_color)
    
    text_rect = rendered_text.get_rect(topleft=(x + 5, y + 5))
    win.blit(rendered_text, text_rect)
    
    if active:
        cursor_x = text_rect.right + 2
        pygame.draw.line(win, WHITE, (cursor_x, y + 5), (cursor_x, y + height - 5), 2)

def zobrist_hash(gs,ZOBRIST_TABLE=ZOBRIST_TABLE):
    h = 0
    for row in range(8):
        for col in range(8):
            piece = gs.board[row][col]
            if piece != '--':
                h ^= ZOBRIST_TABLE[(row,col,piece)]
    if gs.white_to_move:
        h ^= ZOBRIST_TABLE['turn']
    if gs.white_castle_king_side:
        h ^= ZOBRIST_TABLE['wks']
    if gs.white_castle_queen_side:
        h ^= ZOBRIST_TABLE['wqs']
    if gs.black_castle_king_side:
        h ^= ZOBRIST_TABLE['bks']
    if gs.black_castle_queen_side:
        h ^= ZOBRIST_TABLE['bqs']
    if gs.possible_en_passant:
        h ^= ZOBRIST_TABLE['ep'][gs.possible_en_passant[1]]
    return h

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name, filename, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logger.handlers:
        return logger
    handler = RotatingFileHandler(os.path.join(LOG_DIR, filename),maxBytes=5_000_000,backupCount=3,encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger