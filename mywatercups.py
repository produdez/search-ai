import random
import modules.search as search
import modules.puzzle as puzzle
import copy

# ! Problem Def  ----------------------------------------------------

class Cup:
    def __init__(self, name, cup_size):
        self.name = name
        self.cup_size = cup_size
        self.water_level = 0
    def isFull(self):
        return self.water_level == self.cup_size
    def isEmpty(self):
        return self.water_level == 0
    def fill(self):
        self.water_level = self.cup_size
    def pourOut(self, other = None):
        if other is None: #pour out
            self.water_level = 0
            return
        if isinstance(other, Cup):
            pour_amount = min(self.water_level, other.space())
            self.water_level -= pour_amount
            other.water_level += pour_amount
            return
        #error case   
        print('pouring to wtf?')
        return None
    def space(self):
        return self.cup_size - self.water_level
    def __eq__(self, other):
        return self.name == other.name and self.cup_size == other.cup_size and self.water_level == other.water_level
    def __str__(self):
        return 'Cup: {}, water: {}, size: {}.'.format(self.name, self.water_level,self.cup_size)

class CupPuzzleState(puzzle.PuzzleState):
    """
    This class is the abstract class of any puzzle state
    """

    POUR_1_2 = 1
    POUR_2_1 = 2
    POUR_1_OUT = 3
    POUR_2_OUT = 4
    FILL_1 = 5
    FILL_2 = 6

    def __init__( self,cup1_size, cup2_size, water_level):
        """
        Data structure of the puzzle is defined here
        """
        self.cup1 = Cup('First Cup', cup1_size)
        self.cup2 = Cup('Second Cup', cup2_size)
        self.goal_level = water_level


    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.
          Boolean
        """
        # print(str(self.current_location), str(self.goal), 'done: ', self.current_location == self.goal)
        return self.cup1.water_level == self.goal_level or self.cup2.water_level == self.goal_level

    def legalMoves(self):
        """
          Returns a list of legal moves from the current state.
          Move: (neighbor nav name, distance)
        """

        moves = []
        if not self.cup1.isFull(): 
            moves.append(self.FILL_1)
            if not self.cup2.isEmpty():
                moves.append(self.POUR_2_1)
        if not self.cup2.isFull():
            moves.append(self.FILL_2)
            if not self.cup1.isEmpty():
                moves.append(self.POUR_1_2)
        if not self.cup1.isEmpty():
            moves.append(self.POUR_1_OUT)
        if not self.cup2.isEmpty():
            moves.append(self.POUR_2_OUT)

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
        new_puzzle = copy.deepcopy(self)

        cup1 = new_puzzle.cup1
        cup2 = new_puzzle.cup2
        if move == self.POUR_1_2:
            cup1.pourOut(cup2)
        if move == self.POUR_2_1:
            cup2.pourOut(cup1)
        if move == self.FILL_1:
            cup1.fill()
        if move == self.FILL_2:
            cup2.fill()
        if move == self.POUR_1_OUT:
            cup1.pourOut()
        if move == self.POUR_2_OUT:
            cup2.pourOut()

        return new_puzzle


    # Utilities for comparison and display
    def __eq__(self, other):
        return self.cup1 == other.cup1 and self.cup2 == other.cup2

    def __hash__(self):
        util.raiseNotDefined()
    def __getAsciiString(self):
        """
          Returns a display string for the puzzle
        """
        string = []
        string.append('----- Cups ------\n')
        string.append(self.cup1.name)
        cup1_side = ('-' * (4* self.cup1.cup_size+1))
        row_line = '|'
        for i in range(self.cup1.cup_size):
            if i < self.cup1.water_level:
                cell = 'o'
            else: 
                cell = ' '
            row_line = row_line + ' ' + str(cell) + ' |'
        string.append(cup1_side + '\n' + row_line +  '\n'+cup1_side)
        # string.append('\n')
        string.append(self.cup2.name)
        cup2_side = ('-' * (4* self.cup2.cup_size+1))
        row_line = '|'
        for i in range(self.cup2.cup_size):
            if i < self.cup2.water_level:
                cell = 'o'
            else: 
                cell = ' '
            row_line = row_line + ' ' + str(cell) + ' |'
        string.append(cup2_side + '\n'+ row_line + '\n'+cup2_side)

        return '\n'.join(string)
            




    def __str__(self):
        return self.__getAsciiString()

class CupSearchProblem(search.SearchProblem):
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

# ! DATA  ----------------------------------------------------


def loadCupPuzzle(n):
    """
        load map with index n (start 0)
    """
    CUP_DATA =    [
        (4,3,2),
        (9,4,6)
    ]
    data = CUP_DATA[n]
    cup1_size = data[0]
    cup2_size = data[1]
    water_level_goal = data[2]
    return CupPuzzleState(cup1_size,cup2_size,water_level_goal)
    

def test():
    puzzle = loadCupPuzzle(0)
    problem = CupSearchProblem(puzzle)
    print(problem.getStartState())
    
    successor = problem.getSuccessors(puzzle)[0]
    next_state = problem.getStartState().result(successor[1])
    print(next_state)
    return
        
# ! TESTS  ----------------------------------------------------


if __name__ == '__main__':

    puzzle = loadCupPuzzle(int(input('Problem Index:? ')))
    problem = CupSearchProblem(puzzle)
    search.test_search_problem(problem,search.ilterativeDeepeningSearch,print_state=False)
    # search.test_search_problem(problem,search.depthLimitedSearch,print_state=False, depth=6)

