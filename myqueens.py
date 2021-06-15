import search
import random
import puzzle
import copy

class NQueenState(puzzle.PuzzleState):
    """
    This class is the abstract class of any puzzle state
    """
    EMPTY = 0
    CHECKED = 1
    QUEEN = 3

    def __init__( self,n):
        """
        Data structure of the puzzle is defined here
        """
        self.board = []
        for i in range(n):
            self.board.append([self.EMPTY]*n)
        self.board_size = n
        self.queen_count = 0
        self.empty = n*n

    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.
          Boolean
        """
        return self.board_size == self.queen_count

    def legalMoves(self):
        """
          Returns a list of legal moves from the current state.
        """
        moves = []
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == self.EMPTY: 
                    moves.append( (i,j) )
        return moves


    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """

        def find_queen_checks(queen_index, n):
            def sameRow(i,j,m,n): return i == m
            def sameCol(i,j,m,n): return j == n
            def onDiagonal(i,j,m,n):
                return abs(i-m) == abs (j-n)
            checked_list = []
            q_row, q_col = queen_index
            for i in range (n):
                for j in range(n):
                    if i == q_row and j == q_col: continue

                    if (sameRow(i,j,q_row,q_col)
                    or sameCol(i,j,q_row,q_col)
                    or onDiagonal(i,j,q_row,q_col)): 
                        checked_list.append((i,j))
            return checked_list

        #get new board, queen position
        new_puzzle = copy.deepcopy(self)
        board_size = new_puzzle.board_size
        queen_row, queen_col = move

        #set queen cell and cells checked by queen
        board = new_puzzle.board
        board[queen_row][queen_col] = self.QUEEN
        checks = find_queen_checks(move,board_size)
        for i,j in checks:
            board[i][j] = self.CHECKED

        #increase queen count and decrease empty count
        new_puzzle.queen_count +=1
        new_puzzle.empty -= len(checks) + 1
        return new_puzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        for row in range(self.board_size):
            if self.board[row] != other.board[row]: return False
        return True

    def __hash__(self):
        util.raiseNotDefined()
    def __getAsciiString(self):
        """
          Returns a display string for the puzzle
        """
        lines = []
        horizontalLine = ('-' * (4* self.board_size+1))
        lines.append(horizontalLine)
        for row in self.board:
            rowLine = '|'
            for col in row:
                if col == self.EMPTY:
                    col = ' '
                if col == self.QUEEN:
                    col = 'Q'
                if col == self.CHECKED:
                    col = 'x'
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

class NQueenSearchProblem(search.SearchProblem):
    def __init__(self,puzzle):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self,state):
        return state.isGoal()

    def getSuccessors(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        successor = []
        for move in state.legalMoves():
            ret = state.result(move)
            successor.append((ret, move, 1))
        return successor

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

def loadEmptyChessBoard(n):
    pass

def test():
    puzzle = NQueenState(4)
    problem = NQueenSearchProblem(puzzle)
    print(problem.puzzle)
    suc = problem.getSuccessors(puzzle)[0]
    print(suc[0])

def empty_Heuristics(state):
    return -state.empty

if __name__ == '__main__':
    # test()
    # exit()
    puzzle = NQueenState(int(input('BoardSize:? ')))
    problem = NQueenSearchProblem(puzzle)
    search.test_search_problem(problem,search.depthFirstSearch,print_state=False)
    # search.test_search_problem(problem, search.astar, heuristic= empty_Heuristics, print_state=True)