
import copy
import puzzle
import search
import sys
#! ..................................................................................................
class NIM_State(puzzle.PuzzleState):
    PLAYER1 = 1
    PLAYER2 = -1
    def __init__(self, n):
        self.n = n
        self.turn = self.PLAYER1
        self.pieces = [n]
        if sum(self.pieces) != n:
            raise ValueError('Flipping game is not right, left right do not match with n value!')
    def legalMoves(self):
        moves = []
        for index,piece in enumerate(self.pieces):
            for i in range(1, (piece+1)//2):
                if i == piece - i: continue
                moves.append((index,i))
        return moves
    def isGoal(self):
        return self.legalMoves() == []
    def changeTurn(self):
        if self.turn == self.PLAYER1: self.turn = self.PLAYER2
        else: self.turn = self.PLAYER1
    def utility(self):
        return self.PLAYER1 if self.turn == self.PLAYER2 else self.PLAYER2
    def result(self, move):
        index, left_split = move
        new_state = copy.deepcopy(self)
        old_value = new_state.pieces.pop(index)
        new_state.pieces.insert(index,left_split)
        right_split = old_value - left_split
        new_state.pieces.insert(index+1,right_split)
        new_state.changeTurn()
        return new_state
    def __getAsciiString(self):
        """
          Returns a display string for the puzzle
        """
        return f'Turn: {self.turn} --' + str(self.pieces)

    def __str__(self):
        return self.__getAsciiString()

def test_NIM_State():
    nim = NIM_State(12)
    print('init game', nim)
    print(nim.legalMoves())
    print('new game',nim.result(nim.legalMoves()[0]))
# test_NIM_State()

#! ..................................................................................................

def minimax_decision(state, player = True):
    if player: _ , move = max_val(state)
    else: _, move = min_val(state)
    return move
def max_val(state):
    if state.isGoal(): return state.utility(), None
    best_val = - sys.maxsize #maximum, starts at -inf
    best_move = None

    for move in state.legalMoves():
        successor = state.result(move)
        val, _ = min_val(successor)
        if val > best_val:
            best_val = val
            best_move = move
    return (best_val, best_move)

def min_val(state):
    if state.isGoal(): return state.utility(), None
    best_val = sys.maxsize #Minimum, start at inf
    best_move = None

    for move in state.legalMoves():
        successor = state.result(move)
        val, _ = max_val(successor)
        if val < best_val:
            best_val = val
            best_move = move
    return best_val, best_move

def test_minimax():
    n = 7
    init_nim = NIM_State(n)
    
    game = init_nim
    turn = True
    while not game.isGoal():
        player = 'MAX' if turn else 'MIN'
        print(f'---{player}---')
        move = minimax_decision(game,player=turn)
        print(game)
        print('Move: ', move)
        #change game state
        game = game.result(move)
        turn = not turn
    print('Last Stage')
    print(game)
    print('Winner: ', 'MAX' if game.utility() == 1 else 'MIN')
# test_minimax()
#! ..................................................................................................

def alpha_beta_pruning(state, player = True):
    alpha, beta = -sys.maxsize, sys.maxsize
    if player: _ , move = alpha_max_val(state,alpha,beta)
    else: _, move = beta_min_val(state,alpha,beta)
    return move
def alpha_max_val(state, alpha, beta):
    # print(state,' ',alpha,' ', beta)
    if state.isGoal(): return state.utility(), None
    best_val = - sys.maxsize
    best_move = None
    for move in state.legalMoves():
        successor = state.result(move)
        val, _ = beta_min_val(successor, alpha, beta)

        #prune. Parent of this max node is min. Beta of min tell the max value it saw.
        # so if our val bigger than that, we'll never get chosen, max node only get bigger.
        if val >= beta: 
            print(f'Pruning max: {state} after seeing {successor}')
            return val, move 
        
        # update
        if val > best_val:
            best_val = val
            alpha = val
            best_move = move

    return best_val,best_move

def beta_min_val(state, alpha, beta):
    # print(state,' ',alpha,' ', beta)
    if state.isGoal(): return state.utility(), None
    best_val = sys.maxsize
    best_move = None
    for move in state.legalMoves():
        successor = state.result(move)
        val, _ = alpha_max_val(successor,alpha, beta)

        #prune
        if val <= alpha: 
            print(f'Pruning min: {state} after seeing {successor}')
            return val, move 

        #update
        if val < best_val:
            best_val = val
            beta = val
            best_move = move
    return best_val, best_move

def test_alpha_beta():
    n = 5
    init_nim = NIM_State(n)
    
    game = init_nim
    turn = True
    while not game.isGoal():
        player = 'MAX' if turn else 'MIN'
        print(f'---{player}---')
        move = alpha_beta_pruning(game,player=turn)
        print(game)
        print('Move: ', move)
        #change game state
        game = game.result(move)
        turn = not turn
    print('Last Stage')
    print(game)
    print('Winner: ', 'MAX' if game.utility() == 1 else 'MIN')
test_alpha_beta()