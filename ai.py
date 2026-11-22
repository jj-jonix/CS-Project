from globals import setup_logger
search_logger = setup_logger('search', 'search.log')

PIECE_VALUE = {'K': 999, 'Q':9, 'R': 5, 'B': 3 , 'N': 3, 'P':1 }
PHASE_TABLE = {'N':1,'B':1,'R':2,'Q':4,'-':0,'K':0,'P':0}
HANGING_PIECE_PENALTY = {'P': 0.6,'N': 1.5,'B': 1.5,'R': 2.5,'Q': 5.0}
CHECKMATE_SCORE = 1000
STALEMATE_SCORE = 0
DEPTH = 1
MAX_PHASE = 24
MAX_QUIESCENCE_DEPTH = 5
ISOLATED_PAWN_PENALTY = 0.25
DOUBLED_PAWN_PENALTY = 0.20  
PASSED_PAWN_BONUS = [0, 0.3, 0.5, 0.9, 1.5, 2.2, 3.5, 0]
KING_SHIELD_BONUS = 0.3
OPEN_FILE_NEAR_KING_PENALTY = 0.4
BISHOP_PAIR_BONUS = 0.3
ROOK_OPEN_FILE_BONUS = 0.3
MOBILITY_WEIGHT = 0.09

KILLER_MOVES = {}
HISTORY_HEURISTIC = {} 
TRANSPOSITION_TABLE = {}
TT_EXACT = 0
TT_LOWER = 1
TT_UPPER = 2
MATE_THRESHOLD = CHECKMATE_SCORE - 100
CONTEMPT = 0.05

KNIGHT_TABLE = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
    [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
    [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
    [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
    [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
    [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
]

BISHOP_TABLE = [
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
    [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
    [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
    [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
    [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
]

ROOK_TABLE = [
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ 0.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0,  0.0],
]

QUEEN_TABLE = [
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ 0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
]

PAWN_TABLE = [
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
    [ 1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
    [ 0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
    [ 0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
    [ 0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
    [ 0.5,  1.0,  1.0,  2.0,  2.0,  1.0,  1.0,  0.5],
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
]
KING_TABLE_MIDGAME = [
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [ 2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
    [ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0],
    [ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0],
]

KING_TABLE_ENDGAME = [
    [-5.0, -4.0, -3.0, -2.0, -2.0, -3.0, -4.0, -5.0],
    [-3.0, -2.0, -1.0,  0.0,  0.0, -1.0, -2.0, -3.0],
    [-3.0, -1.0,  2.0,  3.0,  3.0,  2.0, -1.0, -3.0],
    [-3.0, -1.0,  3.0,  4.0,  4.0,  3.0, -1.0, -3.0],
    [-3.0, -1.0,  3.0,  4.0,  4.0,  3.0, -1.0, -3.0],
    [-3.0, -1.0,  2.0,  3.0,  3.0,  2.0, -1.0, -3.0],
    [-3.0, -3.0,  0.0,  0.0,  0.0,  0.0, -3.0, -3.0],
    [-5.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -5.0],
]

PIECE_SQUARE_TABLES = {
    'N': KNIGHT_TABLE,
    'B': BISHOP_TABLE,
    'R': ROOK_TABLE,
    'Q': QUEEN_TABLE,
    'P': PAWN_TABLE,
}
def choose_move(gamestate, valid_moves, depth):
    global DEPTH
    DEPTH = depth if depth else 1
    search_logger.debug(f"choose_move called with {len(valid_moves)} valid moves. checkmate={gamestate.checkmate} stalemate={gamestate.stalemate}")
    if not valid_moves:
        search_logger.error("choose_move called with EMPTY valid_moves list — no legal move exists, but checkmate/stalemate not set?")
        return None
    return call_negamax(gamestate,valid_moves)


def evaluate(gamestate, full = True):
    if gamestate.checkmate:
        return - CHECKMATE_SCORE if gamestate.white_to_move else CHECKMATE_SCORE
    if gamestate.stalemate or gamestate.three_fold:
        return CONTEMPT if gamestate.white_to_move else -CONTEMPT
    score = 0
    phase = 0
    board = gamestate.board
    for row in range(8):
        for col in range(8):
            square = board[row][col]
            if square == '--':
                continue
            color = square[0]
            piece_type = square[1] 
            piece = board[row][col]
            phase += PHASE_TABLE[piece[1]]
            value = 0
            if piece_type in PIECE_VALUE:
                value += PIECE_VALUE[piece_type]
            table = PIECE_SQUARE_TABLES.get(piece_type)
            if table is not None:
                if color == 'w':
                    value += table[row][col] * 0.1
                else:
                    value += table[7 - row][col] * 0.1
            score += value if color == 'w' else -value


    phase = min(phase,MAX_PHASE)/MAX_PHASE
    value = 0
    mid_game_value = KING_TABLE_MIDGAME[gamestate.white_king_location[0]][gamestate.white_king_location[1]]
    end_game_value = KING_TABLE_ENDGAME[gamestate.white_king_location[0]][gamestate.white_king_location[1]]
    value += (mid_game_value * phase + end_game_value * (1 - phase)) * 0.1
    score += value
    value = 0
    mid_game_value = KING_TABLE_MIDGAME[7 - gamestate.black_king_location[0]][gamestate.black_king_location[1]]
    end_game_value = KING_TABLE_ENDGAME[7 - gamestate.black_king_location[0]][gamestate.black_king_location[1]]
    value += (mid_game_value * phase + end_game_value * (1 - phase)) * 0.1
    score -= value

    score += king_proximity_bonus(gamestate.white_king_location,gamestate.black_king_location,phase)
    score += pawn_structure_penalty(board)
    score += passed_pawn_bonus(board, phase)
    score += king_safety(board, gamestate.white_king_location, gamestate.black_king_location) * phase
    score += bishop_pair_bonus(board) 
    score += rook_open_file_bonus(board)

    if not full:
        return score
    original_turn = gamestate.white_to_move
    gamestate.white_to_move = True
    white_moves = gamestate.get_all_possible_moves()
    gamestate.white_to_move = False
    black_moves = gamestate.get_all_possible_moves()
    gamestate.white_to_move = original_turn
    score += mobility_score(white_moves, black_moves)
    score += hanging_piece_penalty(gamestate, white_moves, black_moves)
    opponent_moves = black_moves if gamestate.white_to_move else white_moves
    if len(opponent_moves) == 0:
        return CONTEMPT if gamestate.white_to_move else -CONTEMPT
    return score

def call_negamax(gs, valid_moves):
    KILLER_MOVES.clear()
    HISTORY_HEURISTIC.clear()
    global next_move
    next_move = None
    best_move = None
    search_logger.debug(f"--- New search. white_to_move={gs.white_to_move}, material_count={gs.material_count} ---")
    score = 0
    turn_multiplier = 1 if gs.white_to_move else -1
    for current_depth in range(1, DEPTH + 1):
        global DEPTH_RUNTIME
        DEPTH_RUNTIME = current_depth
        if current_depth == 1 or abs(score) >= MATE_THRESHOLD:
            score = negamax_alpha_beta(gs, valid_moves, current_depth, -CHECKMATE_SCORE, CHECKMATE_SCORE, turn_multiplier)
        else:
            window = 0.5
            alpha, beta = score - window, score + window
            while True:
                new_score = negamax_alpha_beta(gs, valid_moves, current_depth, alpha, beta, turn_multiplier)
                if new_score <= alpha:
                    alpha = max(alpha - window, -CHECKMATE_SCORE)
                    window *= 2
                elif new_score >= beta:
                    beta = min(beta + window, CHECKMATE_SCORE)
                    window *= 2
                else:
                    score = new_score
                    break
                if alpha <= -CHECKMATE_SCORE and beta >= CHECKMATE_SCORE:
                    score = negamax_alpha_beta(gs, valid_moves, current_depth, -CHECKMATE_SCORE, CHECKMATE_SCORE, turn_multiplier)
                    break
        search_logger.debug(f"Depth {current_depth} complete. score={score:.2f} best_move={next_move.get_chess_notation() if next_move else None}")
        if next_move is not None:
            best_move = next_move
        else:
            #safeguard so that best move is not none in any case 
            key = gs.zobrist_key
            entry = TRANSPOSITION_TABLE.get(key)
            if entry and entry[3] is not None:
                best_move = entry[3]
    search_logger.debug(f"Search finished. Final best_move={best_move.get_chess_notation() if best_move else 'NONE'}")
    return best_move
 

def negamax_alpha_beta(gs,valid_moves,depth,alpha,beta, turn_multiplier):

    global next_move
    if gs.checkmate:
        return -(CHECKMATE_SCORE - (DEPTH_RUNTIME - depth))
    if gs.stalemate or gs.three_fold:
        return CONTEMPT
    if depth == 0:
        return quiescence_search(gs,valid_moves,alpha,beta,turn_multiplier)
    
    key = gs.zobrist_key
    ply = DEPTH_RUNTIME - depth
    tt_score, tt_move = tt_find(key,depth,alpha,beta,ply)
    if tt_score is not None:
        if ply == 0 and tt_move is not None:
            next_move = tt_move
        return tt_score
    killers = KILLER_MOVES.get(depth,[])
    valid_moves = order_moves(valid_moves,tt_move,killers,HISTORY_HEURISTIC) 
    max_score = -(CHECKMATE_SCORE - (DEPTH_RUNTIME-depth))
    best_move_here = None
    original_alpha = alpha
    for i,move in enumerate(valid_moves):
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        is_quiet = True if move.piece_captured == '--' and not move.is_pawn_promotion else False
        if i >= 4 and depth >= 3 and is_quiet and not gs.in_check:
            score = -negamax_alpha_beta(gs,next_moves,depth-2,-alpha-1,-alpha,-turn_multiplier)
            if score > alpha:
                score = -negamax_alpha_beta(gs,next_moves,depth-1,-beta,-alpha,-turn_multiplier)    
        else:
            score = -negamax_alpha_beta(gs,next_moves,depth-1,-beta,-alpha,-turn_multiplier)
        
        gs.undo_move()
        if score > max_score:
            max_score = score
            best_move_here = move
            if depth == DEPTH_RUNTIME:
                next_move = move
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            store_killer_move(move, depth)
            update_history(move, depth)
            break
    flag = TT_EXACT
    if max_score <= original_alpha:
        flag = TT_UPPER
    elif max_score >= beta:
        flag = TT_LOWER
    tt_store(key,depth,max_score,flag,best_move_here,ply)
    return max_score

def order_moves(valid_moves, tt_move = None, killers = None, history = None):
    moves = []
    for move in valid_moves:
        score = 0
        if tt_move is not None and move == tt_move:
            score = 100000
        elif move.piece_captured != '--' or move.is_pawn_promotion:
            score = 10000 + mvv_lva_score(move)
        elif killers and move in killers:
            score = 5000
        elif history:
            score = history.get((move.start_row, move.start_col,move.end_row, move.end_col),0)
        moves.append((score,move))
    moves.sort(key=lambda pair: pair[0], reverse=True)
    return [move for _,move in moves]

def quiescence_search(gs,valid_moves,alpha,beta,turn_multiplier,quiescence_depth = 0):
    #extra layer on top of negamax when max deapth is reached to go further and search tactical moves like captures promotions and checks
    global next_move
    if gs.checkmate:
        return -(CHECKMATE_SCORE - (DEPTH_RUNTIME + quiescence_depth))
    if gs.stalemate or gs.three_fold:
        return STALEMATE_SCORE
    
    static_eval = turn_multiplier * evaluate(gs, full= True if quiescence_depth == 0 else False)
    if quiescence_depth >= MAX_QUIESCENCE_DEPTH:
        return static_eval
    if static_eval > alpha:
        alpha = static_eval
    if static_eval >= beta:
        return beta
    tactical_moves = []
    for move in valid_moves:
        if move.piece_captured != '--':
            tactical_moves.append(move)
            continue
        if move.is_pawn_promotion:
            tactical_moves.append(move)
            continue
        gs.make_move(move)
        in_check, _, _ = gs.check_pins_and_checks()
        if in_check:
            tactical_moves.append(move)
        gs.undo_move()
    capture_moves = order_moves(tactical_moves)
    for move in capture_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -quiescence_search(gs,next_moves, -beta, -alpha, -turn_multiplier, quiescence_depth + 1)
        gs.undo_move()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha

def pawn_structure_penalty(board):
    white_pawn_files = [0] * 8
    black_pawn_files = [0] * 8

    for row in range(8):
        for col in range(8):
            square = board[row][col]
            if square == 'wP':
                white_pawn_files[col] += 1
            elif square == 'bP':
                black_pawn_files[col] += 1

    score = 0

    for col in range(8):
        if white_pawn_files[col] > 0:
            left = white_pawn_files[col-1] if col > 0 else 0 
            right = white_pawn_files[col+1] if col < 7 else 0
            if left == 0 and right == 0:
                score -= ISOLATED_PAWN_PENALTY * white_pawn_files[col]
            if white_pawn_files[col] > 1:
                score -= DOUBLED_PAWN_PENALTY * (white_pawn_files[col] - 1)

        if black_pawn_files[col] > 0:
            left = black_pawn_files[col - 1] if col > 0 else 0
            right = black_pawn_files[col + 1] if col < 7 else 0
            if left == 0 and right == 0:
                score += ISOLATED_PAWN_PENALTY * black_pawn_files[col]
            if black_pawn_files[col] > 1:
                score += DOUBLED_PAWN_PENALTY * (black_pawn_files[col] - 1)
    return score

def passed_pawn_bonus(board,phase):
    score = 0
    end_game_weight = 1 + (1-phase)

    for row in range(8):
        for col in range(8):
            square = board[row][col]
            color = square[0]
            piece_type = square[1]

            if piece_type != 'P':
                continue
            cols_to_check = []
            for col2 in (col-1,col,col+1):
                if 0<= col2 <= 7:
                    cols_to_check.append(col2)
            if color == 'w':
                rows_ahead = range(row-1,-1,-1)
                enemy = 'b'
            else:
                rows_ahead = range(row+1,8)
                enemy = 'w'

            is_passed = True
            for row2 in rows_ahead:
                for col2 in cols_to_check:
                    if board[row2][col2] == enemy + 'P':
                        is_passed = False
                        break
                if not is_passed:
                    break
            
            if is_passed:
                rank_from_promotion = 7-row if color == 'w' else row
                bonus = PASSED_PAWN_BONUS[rank_from_promotion] * end_game_weight
                score += bonus if color == 'w' else -bonus
    return score

def king_safety(board, white_king_location, black_king_location):
    score = 0
    w_row,w_col = white_king_location
    b_row,b_col = black_king_location

    shield_cols = []
    for col in (w_col-1,w_col,w_col+1):
        if 0<= col <= 7:
            shield_cols.append(col)
    for col in shield_cols:
        shield_row = w_row - 1
        if shield_row >= 0 and board[shield_row][col] == 'wP':
            score += KING_SHIELD_BONUS
        file_has_pawn = any(board[row][col] == 'wP' for row in range(8))
        if not file_has_pawn:
            score -= OPEN_FILE_NEAR_KING_PENALTY

    shield_cols = []
    for col in (b_col-1,b_col,b_col+1):
        if 0<= col <= 7:
            shield_cols.append(col)
    for col in shield_cols:
        shield_row = b_row + 1
        if shield_row <= 7 and board[shield_row][col] == 'bP':
            score -= KING_SHIELD_BONUS
        file_has_pawn = any(board[row][col] == 'bP' for row in range(8))
        if not file_has_pawn:
            score += OPEN_FILE_NEAR_KING_PENALTY

    return score

def bishop_pair_bonus(board):
    score = 0
    white_bishops = 0
    black_bishops = 0
    for row in range(8):
        for col in range(8):
            square = board[row][col]
            if square == 'wB':
                white_bishops += 1
            elif square == 'bB':
                black_bishops += 1

    if white_bishops >= 2:
        score += BISHOP_PAIR_BONUS
    if black_bishops >= 2:
        score -= BISHOP_PAIR_BONUS
    
    return score

def rook_open_file_bonus(board):
    score = 0
    for col in range(8):
        white_pawn = any(board[r][col] == 'wP' for r in range(8))
        black_pawn = any(board[r][col] == 'bP' for r in range(8))
        is_open = not white_pawn and not black_pawn
        if not is_open:
            continue
        for row in range(8):
            if board[row][col] == 'wR':
                score += ROOK_OPEN_FILE_BONUS
            elif board[row][col] == 'bR':
                score -= ROOK_OPEN_FILE_BONUS
    return score

def mobility_score(white_moves, black_moves):
    return (len(white_moves) - len(black_moves)) * MOBILITY_WEIGHT

def store_killer_move(move,depth):
    if move.piece_captured != '--':
        return
    move_at_depth = KILLER_MOVES.setdefault(depth,[])
    if move not in move_at_depth:
        move_at_depth.insert(0,move)
        if len(move_at_depth) >2:
            move_at_depth.pop()

def update_history(move,depth):
    key = (move.start_row, move.start_col, move.end_row, move.end_col)
    HISTORY_HEURISTIC[key] = HISTORY_HEURISTIC.get(key, 0) + depth * depth


def tt_store(key,depth,score,flag,best_move,ply):
    old = TRANSPOSITION_TABLE.get(key)
    if score >= MATE_THRESHOLD:
        score += ply
    elif score<= -MATE_THRESHOLD:
        score -= ply
    if old is None or depth > old[0] or (depth == old[0] and flag == TT_EXACT):
        TRANSPOSITION_TABLE[key] = (depth,score,flag,best_move)


def tt_find(key,depth,alpha,beta,ply):
    entry = TRANSPOSITION_TABLE.get(key)
    if entry == None:
        return None,None
    tt_depth,tt_score,tt_flag,tt_move = entry
    score = tt_score
    if score >= MATE_THRESHOLD:
        score -= ply
    elif score <= -MATE_THRESHOLD:
        score += ply
    if tt_depth  < depth:
        return None, tt_move
    if tt_flag == TT_EXACT:
        return score,tt_move
    if tt_flag == TT_LOWER and score >= beta:
        return score,tt_move
    if tt_flag == TT_UPPER and score <= alpha:
        return score,tt_move
    
    return None, tt_move


def mvv_lva_score(move):
    #most valuable victem least valuable attacker for move ordering
    if move.piece_captured != '--':
        victem = PIECE_VALUE[move.piece_captured[1]]
        attacker = PIECE_VALUE[move.piece_moved[1]]
        return victem * 10 -attacker
    if move.is_pawn_promotion:
        return PIECE_VALUE['Q']
    return -1


def hanging_piece_penalty(gs, white_moves, black_moves):
    score = 0
    white_attacks = {(m.end_row, m.end_col) for m in white_moves}
    black_attacks = {(m.end_row, m.end_col) for m in black_moves}
    board = gs.board
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == '--':
                continue
            color = piece[0]
            p = piece[1]
            if p == 'K':
                continue
            if color == 'w':
                attacked = (row, col) in black_attacks
                defended = (row, col) in white_attacks
                if attacked and not defended:
                    score -= HANGING_PIECE_PENALTY[p]
            else:
                attacked = (row, col) in white_attacks
                defended = (row, col) in black_attacks
                if attacked and not defended:
                    score += HANGING_PIECE_PENALTY[p]
    return score


def non_pawn_material(gs):
    ally_color = 'w' if gs.white_to_move else 'b'
    for row in gs.board:
        for piece in row:
            if piece != '--' and piece[0] == ally_color and piece[1] not in ('P','K'):
                return True
    else:
        return False
    

def king_proximity_bonus(white_king_location, black_king_location, phase):
    w_row, w_col = white_king_location
    b_row, b_col = black_king_location
    dist = abs(w_row - b_row) + abs(w_col - b_col)
    endgame_weight = 1 - phase
    return (7 - dist) * 0.08 * endgame_weight