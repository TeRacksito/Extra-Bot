import random

def gen_scramble(moves):
    scramble_length = int(moves)
    moves = ["R", "R'", "R2", "L", "L'", "L2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2"]	
    scramble = ""
    
    for i in range(0, scramble_length):
    	random_move = random.randint(0, len(moves) - 1)
    	
    	if i > 0:
    	    while moves[random_move][0] == prev_move[0]:
    	        random_move = random.randint(0, len(moves) - 1)			
    	    
    	scramble += " " + moves[random_move]
    	prev_move = moves[random_move]
    return scramble