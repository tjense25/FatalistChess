import sys
import time
import random
from statistics import mean
from termcolor import colored
from collections import defaultdict

symbol = {'RQ':'Rook', 'NQ':'Night', 'BQ':'Bishop', 'Q':'Queen', 'K':'King', 'BK':'Bishop', 'NK':'Night','RK':'Rook',
		  'A':'Pawn','B':'Pawn','C':'Pawn','D':'Pawn','E':'Pawn','F':'Pawn','G':'Pawn','H':'Pawn'}

def insufficient(board):
	balive = []
	walive = []
	for pos,piece in board.items():
		if piece[1]: balive.append(symbol[piece[0]])
		else: walive.append(symbol[piece[0]])

	binsuff = False
	winsuff = False
	if len(balive) == 2 and 'Bishop' in balive: binsuff=True
	elif len(balive) == 2 and 'Night' in balive: binsuff=True
	elif len(balive) == 1: binsuff=True

	if len(walive) == 2 and 'Bishop' in walive: winsuff=True
	elif len(walive) == 2 and 'Night' in walive: winsuff=True
	elif len(walive) == 1: winsuff=True

	return binsuff and winsuff



def update_board(board, turn, move):
	new_board = dict(board)
	piece,old_pos,new_pos = move
	if new_pos == "CastleK":
		del new_board[old_pos]
		del new_board[(old_pos[0],8)]
		new_board[(old_pos[0],7)] = (piece, turn)
		new_board[(old_pos[0],6)] = ('RK', turn)
	elif new_pos == "CastleQ":
		del new_board[old_pos]
		del new_board[(old_pos[0],1)]
		new_board[(old_pos[0],3)] = (piece, turn)
		new_board[(old_pos[0],4)] = ('RK', turn)
	else:
		del new_board[old_pos]
		new_board[new_pos] = (piece, turn)
	return new_board


def filter_moves(moves, board, turn, color, opponent_color, firstmove):
	#removes moves that leave king in check
	valid_moves = []
	for move in moves:
		new_board = update_board(board, turn, move)
		if not check_for_check(new_board, not turn, opponent_color, firstmove):
			valid_moves.append(move)
	return valid_moves

def check_for_check(board, turn, color, firstmove):
	# return true if opponent king in check
	moves = enumerate_moves(board, turn, color, firstmove)
	for _,_,pos in moves:
		if pos in board and board[pos] == ('K', not turn): return True
	return False


def draw_board(board, player_color):
	if player_color == "White":
		print("--------------------------------------------------------")
		for i in range(8,0,-1):
			blank_row=(colored("       ",'white',"on_dark_grey" if i%2 else "on_black")+colored("       ",'white',"on_black" if i % 2 else "on_dark_grey"))*4
			row = ""
			print(blank_row)
			for j in range(1,9):
				on = "on_black"
				if (i+j) % 2 == 0: 
					on = "on_dark_grey"
				if (i,j) in board and board[(i,j)][1]: piece = colored(symbol[board[(i,j)][0]][0], 'magenta', on, attrs=['bold'])
				elif (i,j) in board: piece = colored(symbol[board[(i,j)][0]][0], 'white', on, attrs=['bold'])
				else: piece = colored(" ", 'white',on)
				row += colored("   ",'white',on) + piece + colored("   ",'white',on)
			print(row)
			print(blank_row)
		print("--------------------------------------------------------")
	else:
		print("--------------------------------------------------------")
		for i in range(1,9):
			blank_row=(colored("       ",'white',"on_dark_grey" if i%2==0 else "on_black")+colored("       ",'white',"on_black" if i%2==0 else "on_dark_grey"))*4
			row = ""
			print(blank_row)
			for j in range(8,0,-1):
				on = "on_black"
				if (i+j) % 2 == 0: 
					on = "on_dark_grey"
				if (i,j) in board and board[(i,j)][1]: piece = colored(symbol[board[(i,j)][0]][0], 'magenta', on, attrs=['bold'])
				elif (i,j) in board: piece = colored(symbol[board[(i,j)][0]][0], 'white', on, attrs=['bold'])
				else: piece = colored(" ", 'white',on)
				row += colored("   ",'white',on) + piece + colored("   ",'white',on)
			print(row)
			print(blank_row)
		print("--------------------------------------------------------")

			
def enumerate_moves(board, turn, color, firstmove):
	moves = []
	for piece,pos in color.items():
		if pos == 0 or pos not in board or board[(pos)] != (piece,turn): continue
		if symbol[piece] == "Pawn":
			D = -1 if turn else 1
			if (piece, turn) not in firstmove and (pos[0]+2*D,pos[1]) not in board and (pos[0]+1*D,pos[1]) not in board: moves.append( (piece, pos, (pos[0]+2*D,pos[1])) )
			if (pos[0]+1*D,pos[1]) not in board: moves.append( (piece, pos, (pos[0]+1*D,pos[1])) )
			if (pos[0]+1*D,pos[1]+1) in board and board[(pos[0]+1*D,pos[1]+1)][1]!=turn: moves.append( (piece,pos, (pos[0]+1*D,pos[1]+1)) )
			if (pos[0]+1*D,pos[1]-1) in board and board[(pos[0]+1*D,pos[1]-1)][1]!=turn: moves.append( (piece,pos, (pos[0]+1*D,pos[1]-1)) )
		if symbol[piece] == "Night":
			if pos[0]+2 <= 8 and pos[1]+1 <= 8 and ((pos[0]+2,pos[1]+1) not in board or board[(pos[0]+2,pos[1]+1)][1]!=turn): moves.append( (piece, pos, (pos[0]+2,pos[1]+1)) )
			if pos[0]+2 <= 8 and pos[1]-1 >= 1 and ((pos[0]+2,pos[1]-1) not in board or board[(pos[0]+2,pos[1]-1)][1]!=turn): moves.append( (piece, pos, (pos[0]+2,pos[1]-1)) )
			if pos[0]+1 <= 8 and pos[1]+2 <= 8 and ((pos[0]+1,pos[1]+2) not in board or board[(pos[0]+1,pos[1]+2)][1]!=turn): moves.append( (piece, pos, (pos[0]+1,pos[1]+2)) )
			if pos[0]+1 <= 8 and pos[1]-2 >= 1 and ((pos[0]+1,pos[1]-2) not in board or board[(pos[0]+1,pos[1]-2)][1]!=turn): moves.append( (piece, pos, (pos[0]+1,pos[1]-2)) )
			if pos[0]-1 >= 1 and pos[1]+2 <= 8 and ((pos[0]-1,pos[1]+2) not in board or board[(pos[0]-1,pos[1]+2)][1]!=turn): moves.append( (piece, pos, (pos[0]-1,pos[1]+2)) )
			if pos[0]-1 >= 1 and pos[1]-2 >= 1 and ((pos[0]-1,pos[1]-2) not in board or board[(pos[0]-1,pos[1]-2)][1]!=turn): moves.append( (piece, pos, (pos[0]-1,pos[1]-2)) )
			if pos[0]-2 >= 1 and pos[1]+1 <= 8 and ((pos[0]-2,pos[1]+1) not in board or board[(pos[0]-2,pos[1]+1)][1]!=turn): moves.append( (piece, pos, (pos[0]-2,pos[1]+1)) )
			if pos[0]-2 >= 1 and pos[1]-1 >= 1 and ((pos[0]-2,pos[1]-1) not in board or board[(pos[0]-2,pos[1]-1)][1]!=turn): moves.append( (piece, pos, (pos[0]-2,pos[1]-1)) )
		if symbol[piece] == "Bishop":
			for i in range(1,8):
				if pos[0]+i > 8 or pos[1]+i > 8: break
				elif (pos[0]+i,pos[1]+i) in board and board[(pos[0]+i,pos[1]+i)][1]!=turn: 
					moves.append( (piece, pos, (pos[0]+i,pos[1]+i)) )
					break
				elif (pos[0]+i,pos[1]+i) in board: break
				else: moves.append( (piece, pos, (pos[0]+i,pos[1]+i)) )
			for i in range(1,8):
				if pos[0]+i > 8 or pos[1]-i < 1: break
				elif (pos[0]+i,pos[1]-i) in board and board[(pos[0]+i,pos[1]-i)][1]!=turn: 
					moves.append( (piece, pos, (pos[0]+i,pos[1]-i)) )
					break
				elif (pos[0]+i,pos[1]-i) in board: break
				else: moves.append( (piece, pos, (pos[0]+i,pos[1]-i)) )
			for i in range(1,8):
				if pos[0]-i < 1 or pos[1]+i > 8: break
				elif (pos[0]-i,pos[1]+i) in board and board[(pos[0]-i,pos[1]+i)][1]!=turn: 
					moves.append( (piece, pos, (pos[0]-i,pos[1]+i)) )
					break
				elif (pos[0]-i,pos[1]+i) in board: break
				else: moves.append( (piece, pos, (pos[0]-i,pos[1]+i)) )
			for i in range(1,8):
				if pos[0]-i < 1 or pos[1]-i < 1: break
				elif (pos[0]-i,pos[1]-i) in board and board[(pos[0]-i,pos[1]-i)][1]!=turn: 
					moves.append( (piece, pos, (pos[0]-i,pos[1]-i)) )
					break
				elif (pos[0]-i,pos[1]-i) in board: break
				else: moves.append( (piece, pos, (pos[0]-i,pos[1]-i)) )
		if symbol[piece] == "Rook":
			for i in range(1,8):
				if pos[0]+i > 8: break
				elif (pos[0]+i,pos[1]) in board and board[(pos[0]+i,pos[1])][1]!=turn: 
					moves.append( (piece, pos, (pos[0]+i,pos[1])) )
					break
				elif (pos[0]+i,pos[1]) in board: break
				else: moves.append( (piece, pos, (pos[0]+i,pos[1])) )
			for i in range(1,8):
				if pos[0]-i < 1: break
				elif (pos[0]-i,pos[1]) in board and board[(pos[0]-i,pos[1])][1]!=turn: 
					moves.append( (piece, pos, (pos[0]-i,pos[1])) )
					break
				elif (pos[0]-i,pos[1]) in board: break
				else: moves.append( (piece, pos, (pos[0]-i,pos[1])) )
			for i in range(1,8):
				if pos[1]+i > 8: break
				elif (pos[0],pos[1]+i) in board and board[(pos[0],pos[1]+i)][1]!=turn: 
					moves.append( (piece, pos, (pos[0],pos[1]+i)) )
					break
				elif (pos[0],pos[1]+i) in board: break
				else: moves.append( (piece, pos, (pos[0],pos[1]+i)) )
			for i in range(1,8):
				if pos[1]-i < 1: break
				elif (pos[0],pos[1]-i) in board and board[(pos[0],pos[1]-i)][1]!=turn: 
					moves.append( (piece, pos, (pos[0],pos[1]-i)) )
					break
				elif (pos[0],pos[1]-i) in board: break
				else: moves.append( (piece, pos, (pos[0],pos[1]-i)) )
		if symbol[piece] == "Queen":
			for i in range(1,8):
				if pos[0]+i > 8: break
				elif (pos[0]+i,pos[1]) in board and board[(pos[0]+i,pos[1])][1]!=turn: 
					moves.append( (piece, pos, (pos[0]+i,pos[1])) )
					break
				elif (pos[0]+i,pos[1]) in board: break
				else: moves.append( (piece, pos, (pos[0]+i,pos[1])) )
			for i in range(1,8):
				if pos[0]-i < 1: break
				elif (pos[0]-i,pos[1]) in board and board[(pos[0]-i,pos[1])][1]!=turn: 
					moves.append( (piece, pos, (pos[0]-i,pos[1])) )
					break
				elif (pos[0]-i,pos[1]) in board: break
				else: moves.append( (piece, pos, (pos[0]-i,pos[1])) )
			for i in range(1,8):
				if pos[1]+i > 8: break
				elif (pos[0],pos[1]+i) in board and board[(pos[0],pos[1]+i)][1]!=turn: 
					moves.append( (piece, pos, (pos[0],pos[1]+i)) )
					break
				elif (pos[0],pos[1]+i) in board: break
				else: moves.append( (piece, pos, (pos[0],pos[1]+i)) )
			for i in range(1,8):
				if pos[1]-i < 1: break
				elif (pos[0],pos[1]-i) in board and board[(pos[0],pos[1]-i)][1]!=turn: 
					moves.append( (piece, pos, (pos[0],pos[1]-i)) )
					break
				elif (pos[0],pos[1]-i) in board: break
				else: moves.append( (piece, pos, (pos[0],pos[1]-i)) )
			for i in range(1,8):
				if pos[0]+i > 8 or pos[1]+i > 8: break
				elif (pos[0]+i,pos[1]+i) in board and board[(pos[0]+i,pos[1]+i)][1]!=turn: 
					moves.append( (piece, pos, (pos[0]+i,pos[1]+i)) )
					break
				elif (pos[0]+i,pos[1]+i) in board: break
				else: moves.append( (piece, pos, (pos[0]+i,pos[1]+i)) )
			for i in range(1,8):
				if pos[0]+i > 8 or pos[1]-i < 1: break
				elif (pos[0]+i,pos[1]-i) in board and board[(pos[0]+i,pos[1]-i)][1]!=turn: 
					moves.append( (piece, pos, (pos[0]+i,pos[1]-i)) )
					break
				elif (pos[0]+i,pos[1]-i) in board: break
				else: moves.append( (piece, pos, (pos[0]+i,pos[1]-i)) )
			for i in range(1,8):
				if pos[0]-i < 1 or pos[1]+i > 8: break
				elif (pos[0]-i,pos[1]+i) in board and board[(pos[0]-i,pos[1]+i)][1]!=turn: 
					moves.append( (piece, pos, (pos[0]-i,pos[1]+i)) )
					break
				elif (pos[0]-i,pos[1]+i) in board: break
				else: moves.append( (piece, pos, (pos[0]-i,pos[1]+i)) )
			for i in range(1,8):
				if pos[0]-i < 1 or pos[1]-i < 1: break
				elif (pos[0]-i,pos[1]-i) in board and board[(pos[0]-i,pos[1]-i)][1]!=turn: 
					moves.append( (piece, pos, (pos[0]-i,pos[1]-i)) )
					break
				elif (pos[0]-i,pos[1]-i) in board: break
				else: moves.append( (piece, pos, (pos[0]-i,pos[1]-i)) )
		if symbol[piece] == "King":
			if (piece, turn) not in firstmove and (pos[0],8) in board and board[(pos[0],8)] == ('RK', turn) and ('RK', turn) not in firstmove and (pos[0], 6) not in board and (pos[0],7) not in board: moves.append((piece, pos, "CastleK"))
			if (piece, turn) not in firstmove and (pos[0],1) in board and board[(pos[0],1)] == ('RQ', turn) and ('RQ', turn) not in firstmove and (pos[0], 2) not in board and (pos[0],3) not in board and (pos[0],4) not in board: moves.append((piece, pos, "CastleQ"))
			if pos[0]+1 <= 8 and pos[1]+1 <= 8 and ((pos[0]+1,pos[1]+1) not in board or board[(pos[0]+1,pos[1]+1)][1]!=turn): moves.append( (piece,pos, (pos[0]+1,pos[1]+1)) )
			if pos[0]+1 <= 8 and pos[1]-1 >= 1 and ((pos[0]+1,pos[1]-1) not in board or board[(pos[0]+1,pos[1]-1)][1]!=turn): moves.append( (piece,pos, (pos[0]+1,pos[1]-1)) )
			if pos[0]+1 <= 8 and ((pos[0]+1,pos[1]) not in board or board[(pos[0]+1,pos[1])][1]!=turn): moves.append( (piece,pos, (pos[0]+1,pos[1])) )
			if pos[1]+1 <= 8 and ((pos[0],pos[1]+1) not in board or board[(pos[0],pos[1]+1)][1]!=turn): moves.append( (piece,pos, (pos[0],pos[1]+1)) )
			if pos[1]-1 >= 1 and ((pos[0],pos[1]-1) not in board or board[(pos[0],pos[1]-1)][1]!=turn): moves.append( (piece,pos, (pos[0],pos[1]-1)) )
			if pos[0]-1 >= 1 and ((pos[0]-1,pos[1]) not in board or board[(pos[0]-1,pos[1])][1]!=turn): moves.append( (piece,pos, (pos[0]-1,pos[1])) )
			if pos[0]-1 >= 1 and pos[1]+1 <= 8 and ((pos[0]-1,pos[1]+1) not in board or board[(pos[0]-1,pos[1]+1)][1]!=turn): moves.append( (piece,pos, (pos[0]-1,pos[1]+1)) )
			if pos[0]-1 >= 1 and pos[1]-1 >= 1 and ((pos[0]-1,pos[1]-1) not in board or board[(pos[0]-1,pos[1]-1)][1]!=turn): moves.append( (piece,pos, (pos[0]-1,pos[1]-1)) )

	return moves
			
def play_chess(print_all=False, print_last=False, interactive=False):
	player_color = random.choice(['Black', 'White'])
	print( "God says you will play as %s" % colored(player_color, "magenta" if player_color=='Black' else "white"))
	firstmove = defaultdict(lambda x: True)
	white = {'RQ':(1,1),'NQ':(1,2), 'BQ':(1,3), 'Q':(1,4), 'K':(1,5), 'BK':(1,6), 'NK':(1,7), 'RK':(1,8),
			 'A':(2,1), 'B':(2,2), 'C':(2,3), 'D':(2,4), 'E':(2,5), 'F':(2,6), 'G':(2,7), 'H':(2,8)}
	black = {'RQ':(8,1),'NQ':(8,2), 'BQ':(8,3), 'Q':(8,4), 'K':(8,5), 'BK':(8,6), 'NK':(8,7), 'RK':(8,8),
			 'A':(7,1), 'B':(7,2), 'C':(7,3), 'D':(7,4), 'E':(7,5), 'F':(7,6), 'G':(7,7), 'H':(7,8)}

	board = {}
	for piece,pos in white.items():
		board[pos] = (piece, False)
	for piece,pos in black.items():
		board[pos] = (piece, True)

	n=0
	check = False
	result=""
	while True: 
		time.sleep(.5)
		if print_all: 
			print('{:^56d}'.format(n))
			if check: print('{:^66s}'.format(colored("Check!", "red")))
			draw_board(board, player_color)

		if insufficient(board): 
			result="Insufficient Material. Draw."
			break

		turn = n%2 #WHITE=FALSE
		moves = enumerate_moves(board, turn, black if turn else white, firstmove)
		moves = filter_moves(moves, board, turn, black if turn else white, white if turn else black, firstmove)

		if check and len(moves) == 0: 
			if print_all or print_last: 
				print(colored("Checkmate!",'red'))
				if turn: print ("White Wins!")
				else: print(colored("Black wins!", "magenta"))
			if turn: result = "Checkmate! White wins."
			else: result = "Checkmate! Black wins."
			break
		elif len(moves) == 0:
			if print_all or print_last: 
				print("Stalemate!")
				print("Game is a draw.")
			result = "Stalemate. Draw."
			break
		piece,old_pos,new_pos = random.choice(moves)
		if interactive and (turn and player_color=="Black") or (not turn and player_color=="White"):
			random.shuffle(moves)
			index = 0
			while not (index - 1) in range(len(moves)):
				try: 
					index = int(input("Choose a number between 1 and %d: " % len(moves)))
				except: index = 0
			piece,old_pos,new_pos = moves[index-1]

		firstmove[(piece,turn)] = False

		if new_pos == "CastleK":
			del board[old_pos]
			del board[(old_pos[0],8)]
			board[(old_pos[0],7)] = (piece, turn)
			board[(old_pos[0],6)] = ('RK', turn)
			if turn: 
				black[piece] = (old_pos[0],7)
				black['RK'] = (old_pos[0],6)
			else:
				white[piece] = (old_pos[0],7)
				white['RK'] = (old_pos[0],6)
			continue
		if new_pos == "CastleQ":
			del board[old_pos]
			del board[(old_pos[0],1)]
			board[(old_pos[0],3)] = (piece, turn)
			board[(old_pos[0],4)] = ('RK', turn)
			if turn: 
				black[piece] = (old_pos[0],3)
				black['RQ'] = (old_pos[0],4)
			else:
				white[piece] = (old_pos[0],3)
				white['RQ'] = (old_pos[0],4)
			continue
					
		if new_pos in board:
			if turn: white[board[new_pos][0]]=0
			else: black[board[new_pos][0]]=0
		if turn: black[piece] = new_pos
		else: white[piece] = new_pos
		del board[old_pos]

		if symbol[piece]=="Pawn" and new_pos[0] == 1+7*(1-(turn%2==1)):
			promotion = random.choice(['Queen','Rook','Night','Bishop'])
			new_piece = promotion[0] + piece
			if turn: 
				del black[piece]
				black[new_piece]=new_pos
			else: 
				del white[piece]
				white[new_piece]=new_pos
			symbol[new_piece] = promotion
			piece = new_piece
		board[new_pos] = (piece, turn)
		check = check_for_check(board, turn, black if turn else white, firstmove)
		n+=1
	if print_all or print_last:
		print(result, n)
		if player_color in result: print(colored('God has declared that you are a winner', 'yellow'))
		else: print(colored('God has declared that you are a loser', 'dark_grey'))
	return (result,n)

play_chess(print_all=True, interactive=True)
	
