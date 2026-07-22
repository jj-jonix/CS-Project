from ai import PIECE_VALUE
from globals import zobrist_hash,ZOBRIST_TABLE
class gameState:
    def __init__(self):
        self.board = [['bR','bN','bB','bQ','bK','bB','bN','bR'],
                      ['bP','bP','bP','bP','bP','bP','bP','bP'],
                      ['--','--','--','--','--','--','--','--'],
                      ['--','--','--','--','--','--','--','--'],
                      ['--','--','--','--','--','--','--','--'],
                      ['--','--','--','--','--','--','--','--'],
                      ['wP','wP','wP','wP','wP','wP','wP','wP'],
                      ['wR','wN','wB','wQ','wK','wB','wN','wR']]

        self.move_functions = {'P':self.get_pawn_moves,'R':self.get_rook_moves,'B':self.get_bishop_moves,
                               'K':self.get_king_moves,'Q':self.get_queen_moves,'N':self.get_knight_moves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7,4)
        self.black_king_location = (0,4)
        self.in_check = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.three_fold = False
        self.possible_en_passant=()
        self.white_castle_king_side = True
        self.white_castle_queen_side = True
        self.black_castle_king_side = True
        self.black_castle_queen_side = True
        self.castle_rights_log = [CastleRights(self.white_castle_king_side,self.black_castle_king_side,
                                               self.white_castle_queen_side,self.black_castle_queen_side)]
        self.material_count = 0
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '--':
                    self.material_count +=PIECE_VALUE.get(piece[1],0)

        self.position_counts = {}
        self.zobrist_key = zobrist_hash(self)
        self.zobrist_key_log = []
        self.position_counts[self.zobrist_key] = 1
        self.en_passant_log = [self.possible_en_passant]


    def make_move(self,move):
        key = self.zobrist_key
        self.zobrist_key_log.append(key)
        old_wks = self.white_castle_king_side
        old_wqs = self.white_castle_queen_side
        old_bks = self.black_castle_king_side
        old_bqs = self.black_castle_queen_side
        old_ep = self.possible_en_passant
        
        key ^= ZOBRIST_TABLE[(move.start_row,move.start_col,move.piece_moved)]
        if move.piece_captured != '--' and not move.is_en_passant:
            key ^= ZOBRIST_TABLE[(move.end_row,move.end_col,move.piece_captured)]
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        key ^= ZOBRIST_TABLE['turn']

        if move.piece_moved =='wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved =='bK':
            self.black_king_location = (move.end_row, move.end_col)
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'
            self.material_count += PIECE_VALUE['Q'] - PIECE_VALUE['P']
            key ^= ZOBRIST_TABLE[(move.end_row, move.end_col, self.board[move.end_row][move.end_col])]
        else:
            key ^= ZOBRIST_TABLE[(move.end_row,move.end_col,move.piece_moved)]
        if move.is_en_passant:
            key ^= ZOBRIST_TABLE[(move.start_row,move.end_col, self.board[move.start_row][move.end_col])]
            self.board[move.start_row][move.end_col] = '--' 
            
        if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:
            self.possible_en_passant = ((move.start_row + move.end_row)//2,move.start_col)
        else:
            self.possible_en_passant = ()

        self.update_castle_rights(move)
        self.castle_rights_log.append(CastleRights(self.white_castle_king_side,self.black_castle_king_side,
                                                   self.white_castle_queen_side,self.black_castle_queen_side))
        self.en_passant_log.append(self.possible_en_passant)
        if move.castle:
            if move.end_col - move.start_col == 2:
                rook = self.board[move.end_row][move.end_col+1]
                key ^= ZOBRIST_TABLE[(move.end_row,move.end_col+1,rook)]
                key ^= ZOBRIST_TABLE[(move.end_row,move.end_col-1,rook)]
                self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col +1]
                self.board[move.end_row][move.end_col+1] = '--'
            else:
                rook = self.board[move.end_row][move.end_col-2]
                key ^= ZOBRIST_TABLE[(move.end_row, move.end_col-2, rook)]
                key ^= ZOBRIST_TABLE[(move.end_row, move.end_col+1, rook)]
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col -2]
                self.board[move.end_row][move.end_col-2] = '--'     
        
        if move.is_en_passant:
            self.material_count -= PIECE_VALUE['P']
        elif move.piece_captured != '--' and not move.is_pawn_promotion:
            self.material_count -= PIECE_VALUE.get(move.piece_captured[1], 0)
        
        if old_wks != self.white_castle_king_side:
            key ^= ZOBRIST_TABLE['wks']
        if old_wqs != self.white_castle_queen_side: 
            key ^= ZOBRIST_TABLE['wqs']
        if old_bks != self.black_castle_king_side: 
            key ^= ZOBRIST_TABLE['bks']
        if old_bqs != self.black_castle_queen_side: 
            key ^= ZOBRIST_TABLE['bqs']
        if old_ep:
            key ^= ZOBRIST_TABLE['ep'][old_ep[1]]
        if self.possible_en_passant: 
            key ^= ZOBRIST_TABLE['ep'][self.possible_en_passant[1]]
        self.zobrist_key = key
        self.position_counts[key] = self.position_counts.get(key, 0) + 1
        if self.position_counts[key] >= 3:
            self.three_fold = True

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

            if move.piece_moved =='wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved =='bK':
                self.black_king_location = (move.start_row, move.start_col)
            if move.is_en_passant:
                self.board[move.end_row][move.end_col] ='--'
                self.board[move.start_row][move.end_col] = move.piece_captured
            self.en_passant_log.pop()
            self.possible_en_passant = self.en_passant_log[-1]
            self.castle_rights_log.pop()

            castle_rights = self.castle_rights_log[-1]
            self.white_castle_king_side = castle_rights.wks
            self.black_castle_king_side = castle_rights.bks
            self.white_castle_queen_side = castle_rights.wqs
            self.black_castle_queen_side = castle_rights.bqs
            
            if move.castle:
                if move.end_col - move.start_col == 2:
                    self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col -1]
                    self.board[move.end_row][move.end_col-1] = '--'
                else:
                    self.board[move.end_row][move.end_col -2] = self.board[move.end_row][move.end_col +1]
                    self.board[move.end_row][move.end_col+1] = '--'  
            self.checkmate = False
            self.stalemate = False

            if move.is_en_passant:
                self.material_count += PIECE_VALUE['P']
            elif move.piece_captured != '--' and not move.is_pawn_promotion:
                self.material_count += PIECE_VALUE.get(move.piece_captured[1],0)
            if move.is_pawn_promotion:
                self.material_count -= PIECE_VALUE['Q'] - PIECE_VALUE['P']

            key = self.zobrist_key
            self.position_counts[key] = self.position_counts.get(key, 0) - 1
            if self.position_counts[key] == 0:
                del self.position_counts[key]
            self.zobrist_key = self.zobrist_key_log.pop()
            self.three_fold = self.position_counts.get(self.zobrist_key, 0) >= 3

    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.check_pins_and_checks()
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:
                moves = self.get_all_possible_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []
                if piece_checking[1] == 'N':
                    valid_squares = [(check_row,check_col)]
                else:
                    for i in range(1,8):
                        valid_square = (king_row + check[2]*i, king_col + check[3]*i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].piece_moved[1] != 'K':
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:
                self.get_king_moves(king_row,king_col,moves)        
        else:
            moves = self.get_all_possible_moves()
        if len(moves) == 0:
            if self.in_check:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False    
        return moves
    
    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_to_move) or (turn=='b' and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row,col,moves)
    
        return moves
    def check_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.white_to_move:
            enemy_color = 'b'
            my_color = 'w'
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = 'w'
            my_color = 'b'
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,1),(-1,-1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1,8):
                end_row = start_row + d[0]*i
                end_col = start_col + d[1]*i
                if 0<= end_row <8 and 0<= end_col<8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == my_color and end_piece[1] != 'K':
                        if possible_pin == ():
                            possible_pin = (end_row,end_col, d[0],d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        Type = end_piece[1]
                        if ((0 <= j <=3 and Type == 'R')or
                                (4<=j<=7 and Type == 'B') or
                                (i==1 and Type == 'P' and((enemy_color == 'w' and 6<= j <= 7) or (enemy_color == 'b' and 4<= j <= 5)))or
                                (Type == 'Q') or (i==1 and Type == 'K')):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row,end_col, d[0],d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break    

        knight_moves = ((-2,1),(-2,-1),(-1,-2),(1,-2),(-1,2),(1,2),(2,-1),(2,1))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0<= end_row <8 and 0<= end_col<8:  
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_col,m[0],m[1]))
        return in_check, pins, checks

    def get_pawn_moves(self,row,col,moves):
        board = self.board
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = self.pins[i][2], self.pins[i][3]
                self.pins.remove(self.pins[i])
                break
        if self.white_to_move:
            move_amount = -1
            start_row = 6
            back_row = 0
            enemy_color = 'b'
            king_row,king_col = self.white_king_location
        else:
            move_amount = 1
            start_row = 1
            back_row = 7
            enemy_color = 'w'
            king_row,king_col = self.black_king_location
        pawn_promotion = False
        if self.board[row + move_amount][col] == '--':
            if not piece_pinned or pin_direction == (move_amount,0):
                if row + move_amount == back_row:
                    pawn_promotion = True
                moves.append(Move((row,col),(row+move_amount,col),self.board, pawn_promotion=pawn_promotion))
                if row == start_row and self.board[row + move_amount*2][col] == '--':
                    moves.append(Move((row,col),(row+move_amount*2,col),self.board))

        if col - 1 >= 0:
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[row + move_amount][col - 1][0] == enemy_color:
                    if row + move_amount == back_row:
                        pawn_promotion = True
                    moves.append(Move((row, col),(row + move_amount, col - 1),board,pawn_promotion=pawn_promotion))
                if (row+move_amount, col-1) == self.possible_en_passant:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:
                            inside_range = range(king_col+1,col-1)
                            outside_rage = range(col+1,8)
                        else:
                            inside_range = range(king_col-1,col,-1)
                            outside_rage = range(col-2,-1,-1)
                        for i in inside_range:
                            if self.board[row][i] != '--':
                                blocking_piece = True
                        for i in outside_rage: 
                            square = self.board[row][i]
                            if square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q'):
                                attacking_piece = True
                            elif square[0] != '--':
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col),(row + move_amount, col - 1),board,is_en_passant = True))
                    
        if col + 1 <= 7:
            if not piece_pinned or pin_direction == (move_amount, 1):
                if self.board[row + move_amount][col + 1][0] == enemy_color:
                    if row + move_amount == back_row:
                        pawn_promotion = True
                    moves.append(Move((row, col),(row + move_amount, col + 1),board,pawn_promotion=pawn_promotion))
                if (row+move_amount, col+1) == self.possible_en_passant:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:
                            inside_range = range(king_col+1,col)
                            outside_rage = range(col+2,8)
                        else:
                            inside_range = range(king_col-1,col+1,-1)
                            outside_rage = range(col-1,-1,-1)
                        for i in inside_range:
                            if self.board[row][i] != '--':
                                blocking_piece = True
                        for i in outside_rage: 
                            square = self.board[row][i]
                            if square[0] == enemy_color and (square[1] == 'R' or square[1] == 'Q'):
                                attacking_piece = True
                            elif square[0] != '--':
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col),(row + move_amount, col + 1),board,is_en_passant = True))  
            

    def get_rook_moves(self,row,col,moves):
        board = self.board
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = self.pins[i][2], self.pins[i][3]
                if self.board[row][col][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1,8):
                end_row = row + d[0]*i
                end_col = col + d[1]*i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned  or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = board[end_row][end_col]
                        if end_piece == '--':
                            moves.append(Move((row,col),(end_row,end_col),board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((row,col),(end_row,end_col),board))
                            break
                        else:
                            break
                else:
                    break

    def get_bishop_moves(self,row,col,moves):
        board = self.board
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = self.pins[i][2], self.pins[i][3]
                self.pins.remove(self.pins[i])
                break
        directions = ((-1,-1),(1,-1),(-1,1),(1,1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1,8):
                end_row = row + d[0]*i
                end_col = col + d[1]*i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned  or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = board[end_row][end_col]
                        if end_piece == '--':
                            moves.append(Move((row,col),(end_row,end_col),board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((row,col),(end_row,end_col),board))
                            break
                        else:
                            break
                else:
                    break

    def get_knight_moves(self,row,col,moves):
        board = self.board
        piece_pinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        knight_moves = ((-2,1),(-2,-1),(-1,-2),(1,-2),(-1,2),(1,2),(2,-1),(2,1))
        enemy_color = 'b' if self.white_to_move else 'w'
        if not piece_pinned:
            for nr,nc in knight_moves:
                end_row = row + nr
                end_col = col + nc
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = board[end_row][end_col]
                    if end_piece == '--' or end_piece[0] == enemy_color :
                        moves.append(Move((row,col),(end_row,end_col),board))

    def get_queen_moves(self,row,col,moves):
        self.get_rook_moves(row,col,moves)
        self.get_bishop_moves(row,col,moves)
        

    def get_king_moves(self,row,col,moves):
        board = self.board
        king_moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = row + king_moves[i][0]
            end_col = col + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = board[end_row][end_col]
                if end_piece[0] != ally_color:
                    if ally_color == 'w':
                        self.white_king_location = (end_row,end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, _, _ = self.check_pins_and_checks()
                    if not in_check:
                        moves.append(Move((row,col),(end_row,end_col),board))
                    if ally_color == 'w':
                        self.white_king_location = (row,col)
                    else:
                        self.black_king_location = (row,col)
        if not self.in_check:
            if self.white_castle_king_side and board[row][col] =='wK' and board[row][col+1] == '--' and board[row][col+2] == '--':
                self.white_king_location = (row,col+1)
                in_check1,_,_ = self.check_pins_and_checks()
                self.white_king_location = (row,col+2)
                in_check2,_,_ = self.check_pins_and_checks()
                if not in_check1 and not in_check2:
                    moves.append(Move((row,col),(row,col+2),board,castle=True))
                self.white_king_location=(row,col)
            if self.white_castle_queen_side and board[row][col] =='wK' and board[row][col-1] == '--' and board[row][col-2] == '--' and board[row][col-3]=='--':
                self.white_king_location = (row,col-1)
                in_check1,_,_ = self.check_pins_and_checks()
                self.white_king_location = (row,col-2)
                in_check2,_,_ = self.check_pins_and_checks()
                if not in_check1 and not in_check2:
                    moves.append(Move((row,col),(row,col-2),board,castle=True))
                self.white_king_location=(row,col)
            if self.black_castle_king_side and board[row][col] =='bK' and board[row][col+1] == '--' and board[row][col+2] == '--':
                self.black_king_location = (row,col+1)
                in_check1,_,_ = self.check_pins_and_checks()
                self.black_king_location = (row,col+2)
                in_check2,_,_ = self.check_pins_and_checks()
                if not in_check1 and not in_check2:
                    moves.append(Move((row,col),(row,col+2),board,castle=True))
                self.black_king_location=(row,col)
            if  self.black_castle_queen_side and board[row][col] =='bK' and board[row][col-1] == '--' and board[row][col-2] == '--' and board[row][col-3]=='--':
                self.black_king_location = (row,col-1)
                in_check1,_,_ = self.check_pins_and_checks()
                self.black_king_location = (row,col-2)
                in_check2,_,_ = self.check_pins_and_checks()
                if not in_check1 and not in_check2:
                    moves.append(Move((row,col),(row,col-2),board,castle=True))
                self.black_king_location=(row,col)
    
    
    def update_castle_rights(self,move):
        if move.piece_moved == 'wK':
            self.white_castle_king_side = False
            self.white_castle_queen_side = False
        elif move.piece_moved == 'bK':
            self.black_castle_king_side = False
            self.black_castle_queen_side = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 7:
                    self.white_castle_king_side = False
                elif move.start_col ==0:
                    self.white_castle_queen_side = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 7:
                    self.black_castle_king_side = False
                elif move.start_col ==0:
                    self.black_castle_queen_side = False
        if move.piece_captured == 'wR':
            if move.end_row == 7:
                if move.end_col == 0:
                    self.white_castle_queen_side = False
                elif move.end_col == 7:
                    self.white_castle_king_side = False
        elif move.piece_captured == 'bR':
            if move.end_row == 0:
                if move.end_col == 0:
                    self.black_castle_queen_side = False
                elif move.end_col == 7:
                    self.black_castle_king_side = False
            

class CastleRights:
    def __init__(self,wks,bks,wqs,bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs

class Move:
    rank_to_rows = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    files_to_cols = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    rows_to_ranks = {v: k for k, v in rank_to_rows.items()}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    
    def __init__(self, start_square, end_square, board,pawn_promotion=False, is_en_passant = False, castle = False):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_pawn_promotion = pawn_promotion
        self.is_en_passant = is_en_passant
        self.castle = castle
        if is_en_passant:
            self.piece_captured = 'bP' if self.piece_moved == 'wP' else 'wP'
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row*10 + self.end_col
    def __eq__(self,other):
        if isinstance(other,Move):
            if self.move_id == other.move_id:
                return True
            return False




    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self,row,col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
    

    