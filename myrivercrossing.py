import search
import random
import puzzle
import copy
from itertools import combinations 

class Boat:
    def __init__(self, capacity):
        self.name = 'Boat'
        self.capacity = capacity
        self.passenger = set()
    def __eq__(self, o):
        return self.passenger == o.passenger and self.capacity == o.capacity
    # def __str__(self):
    #     return 'Boat -- Cap: {}, Ride: {}'.format(self.capacity,self.passenger)
    def load(self,move):
        self.passenger.clear()
        self.passenger.update(move)
    def unload(self,land):
        land.population.update(self.passenger)
        self.passenger.clear()
    def isFull(self):
        return len(self.passenger) == self.capacity
    def isEmpty(self):
        return len(self.passenger) == 0
    def __str__(self):
        string = []
        passenger_list = list(self.passenger)
        string.append(self.name)
        cell_count = self.capacity
        river_width = ('-' * (4* cell_count+1))
        row_line = '|'
        for i in range(cell_count):
            if i < len(self.passenger):
                cell = passenger_list[i]
            else: 
                cell = ' '
            row_line = row_line + ' ' + str(cell) + ' |'
        string.append(river_width + '\n' + row_line +  '\n'+river_width)
        return '\n'.join(string)
class Land:
    def __init__(self, name, population = set()):
        self.name = name
        self.population = population
    def __eq__(self,o):
        return self.population == o.population
    # def __str__(self):
    #     return '{} -- Population: {}'.format(self.name,str(self.population))
    def unload(self,move):
        self.population -= move
    def isEmpty(self):
        return len(self.population) == 0
    def __str__(self):
        string = []
        population_list = list(self.population)
        cell_count = 10
        river_width = ('-' * (4* cell_count+1))
        row_line = '|'
        for i in range(cell_count):
            if i < len(self.population):
                cell = population_list[i]
            else: 
                cell = ' '
            row_line = row_line + ' ' + str(cell) + ' |'
        string.append(river_width + '\n' + row_line +  '\n'+river_width)

        return '\n'.join(string)


        

class RiverCrossingPuzzleState(puzzle.PuzzleState):
    """
    This class is the abstract class of any puzzle state
    """


    def __init__( self,boat, leftside, rightside,boat_location, prohibited_sets, goal, must_have_passenger = set()):
        """
        Data structure of the puzzle is defined here
        """
        self.boat = boat #remember location
        self.leftside = leftside
        self.rightside = rightside
        self.boat_location = boat_location
        self.prohibited_sets = prohibited_sets # list of characters (set) that cant be together
        self.goal = goal # the solution Land
        self.must_have_passenger = must_have_passenger
    def getRealPopulationSets(self):
        left_pop = self.leftside.population.union(self.boat.passenger) if self.boat_location == self.leftside else self.leftside.population
        right_pop = self.rightside.population.union(self.boat.passenger) if self.boat_location == self.rightside else self.rightside.population
        return (left_pop,right_pop)
    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.
          Boolean
        """
        right_pop = self.getRealPopulationSets()[1]
        return right_pop == self.goal.population
    def legalMoves(self):
        """
          Returns a list of legal moves from the current state.
          Move: {} -> set of what to load on the boat
        """
        boat = self.boat    
        boat_location = self.boat_location
        boat_cap = boat.capacity
        current_population = boat_location.population.union(boat.passenger)
        other_population = self.leftside.population if boat_location == self.rightside else self.rightside.population
        prohibit_sets = self.prohibited_sets
        
        #fail case
        for prohibited in prohibit_sets:
            if current_population == prohibited or other_population == prohibited:
                return []
        
        #get all possible combinations of move and remove prohibited ones
        all_case = []

        for passenger_count in range(1,boat_cap+1 - len(self.must_have_passenger)): #combination 1 to n
            all_case += list(combinations(current_population,passenger_count))
        
        all_case = [self.must_have_passenger.union(set(x)) for x in all_case] #convert tuple (from combination function) to set
        
        for prohibited in prohibit_sets: # remove prohibited
            if prohibited in all_case: all_case.remove(prohibited)
        return all_case # set of all possible moves




    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.

        move: set of all passengers {p1,p2,...}
        """
        new_puzzle = copy.deepcopy(self)
        boat = new_puzzle.boat
        boat_location = new_puzzle.boat_location
        passenger = move
        #load boat, remove from land
        boat.unload(boat_location)
        boat.load(passenger)
        boat_location.unload(passenger)
        #move boat

        if boat_location == new_puzzle.rightside:
            new_puzzle.boat_location = new_puzzle.leftside
        else:
            new_puzzle.boat_location = new_puzzle.rightside

        return new_puzzle


    # Utilities for comparison and display
    def __eq__(self, other):

        left1,right1 = self.getRealPopulationSets()
        left2,right2 = other.getRealPopulationSets()
        loc1 = 'L' if self.boat_location == self.leftside else 'R'
        loc2 = 'L' if other.boat_location == other.leftside else 'R'
        return left1 == left2 and right1 == right2 and loc1 == loc2


    def __hash__(self):
        util.raiseNotDefined()
    def __getAsciiString(self):
        """
          Returns a display string for the puzzle
        """
        string = []
        string.append('----- River ------\n')
        #left
        string.append(str(self.leftside))
        #boat if left
        if self.boat_location == self.leftside:
            string.append(str(self.boat) + '-Top')
        #river
        string.append('\n\n')
        #boat if right
        if self.boat_location == self.rightside:
            string.append(str(self.boat) + '-Bot')
        #right
        string.append(str(self.rightside))

        return '\n'.join(string)
            




    def __str__(self):
        return self.__getAsciiString()

class RiverCrossingSearchProblem(search.SearchProblem):
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

def loadRiverPuzzle():
    """
        load map with index n (start 0)
    """
    WOLF = "W"
    SHEEP = "S"
    FARMER = "F"
    VEGETABLE = "V"
    boat = Boat(2)
    leftside = Land('TopSide',set([WOLF,FARMER,SHEEP,VEGETABLE]))
    rightside = Land('BottomSide',set())
    init_location = leftside
    goal = Land('Goal',set([WOLF,FARMER,SHEEP,VEGETABLE]))
    prohibited_sets = [set([WOLF,SHEEP]),set([SHEEP,VEGETABLE]), set([SHEEP,VEGETABLE,WOLF])]
    must_have_boat_people = set(FARMER)

    return RiverCrossingPuzzleState(boat,leftside,rightside,init_location,prohibited_sets,goal,must_have_passenger=must_have_boat_people)
    

def test():
    puzzle = loadRiverPuzzle()
    problem = RiverCrossingSearchProblem(puzzle)
    # print(problem.getStartState())
    
    # successor = problem.getSuccessors(puzzle)[0]
    # # print('successors:', str(successor))
    # next_state = problem.getStartState().result(successor[1])
    # print(next_state)
    search.test_search_problem(problem,search.depthFirstSearch,print_state=False)
    return
        
    

if __name__ == '__main__':
    # test()
    # exit()

    puzzle = loadRiverPuzzle()
    problem = RiverCrossingSearchProblem(puzzle)
    search.test_search_problem(problem,search.depthFirstSearch,print_state=False)