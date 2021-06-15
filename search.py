# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class SearchNode():
    def __init__(self,state,path_cost,heuristic, parent = None, action = None, depth = 0):
        self.state = state
        self.path_cost = path_cost
        self.heuristic = heuristic
        self.parent = parent
        self.action = action
        self.depth = depth
    def get_node_path(self):
        if not self.parent: return []
        solution = self.parent.get_node_path() 
        solution.append(self.action)
        return solution
    def __eq__(self,other):
        return self.state == other.state
    def better(self,other):
        return self.state == other.state and self.path_cost + self.heuristic < other.path_cost + other.heuristic
    def __str__(self):
        return 'SearchNode --- [State: {}, PathCost: {}, Heuris: {}, Total: {}]'.format(str(self.state),self.path_cost, self.heuristic,self.path_cost + self.heuristic)        
        return 'SearchNode --- [State: {}, Parent: {}, PathCost: {}, Action: {}]'.format(str(self.state),str(self.parent),self.path_cost,str(self.action))


from time import time
def performance_calc_wrapper(func):
    def time_capture(*arg,**kwarg):
        start = time()
        ret_val = func(*arg,**kwarg)
        end = time()
        print('The function took: {:.5f}s to finish'.format(end-start))
        return ret_val
    return time_capture

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem, print_state = False):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    return genericSearch(problem,util.Stack(), print_state)



    util.raiseNotDefined()

def breadthFirstSearch(problem, print_state=False):
    """Search the shallowest nodes in the search tree first."""
    return genericSearch(problem,util.Queue(), print_state)

def uniformCostSearch(problem, print_state=False):
    """Search the node of least total cost first."""
    return genericSearch(problem, util.PriorityQueueWithFunction(lambda node: node.path_cost), print_state)

def depthLimitedSearch(problem,depth, print_state=False):
    return genericSearch(problem, util.Stack(), print_state, depth)
def ilterativeDeepeningSearch(problem,print_state=False):
    depth = 0
    while (1):
        print('At max depth: ', depth)
        result = depthLimitedSearch(problem,depth,print_state)
        if not result is None: return result
        depth += 1
def greedySearch(problem,heuristic_function, print_state=False):
    return genericSearch(problem, util.PriorityQueueWithFunction(lambda node: heuristic_function(node.state)), print_state)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic_function = nullHeuristic, print_state=False):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    return genericSearch(problem, util.PriorityQueueWithFunction(lambda node: node.path_cost + heuristic_function(node.state,problem)), print_state,heuristics=heuristic_function)

def normalized_list(lst):
    print(
        'list: ', lst
    )
    s = float(sum(lst))
    return [x/s for x in lst]

from scipy.stats import rv_discrete
import numpy
def stochasticHillClimb(problem,heuristic, print_state = False):
    #init node
    current_node = SearchNode(problem.getStartState(),0 ,heuristic(current_node.state,problem))
    print('Current Node: ', str(current_node))
    input('Next?')
    while(True):
        if problem.isGoalState(current_node.state):
            return current_node.get_node_path()
        #get childs
        successors = problem.getSuccessors(current_node.state)
        print('successors: ', successors)
        #stochastic hill climb, only choose 1 child
        current_heuristic = heuristic(current_node.state)
        child_steepness = [abs(heuristic(suc_state) - current_heuristic )for suc_state, action, step_cost in successors]
        print('current-steep: ', current_heuristic, 'childsteep: ', str(child_steepness))
        probability = normalized_list(child_steepness)
        print('prob list: ', probability)
        choosen_index = rv_discrete(values = (numpy.array(range(len(successors))),probability)).rvs(size = 1)[0]
        chose_state, chose_action, chose_step = successors[choosen_index]
        current_node = SearchNode(
            chose_state,
            current_node.path_cost + chose_step,
            current_node,
            chose_action
        )


        

@performance_calc_wrapper
def genericSearch(problem,frontier = None, print_steps = False, limit = None, heuristics = nullHeuristic):
    # print_steps = True

    start_state = problem.getStartState()
    start_node = SearchNode(start_state,0,heuristics(start_state,problem))
    # print('startnode!',str(start_node))
    #NOTE: redundant 
    # if problem.isGoalState(start_node.state):
    #     print('init state is goal!') 
    #     return start_node.get_node_path()

    frontier.push(start_node)
    explored = []
    count = 0 #use for counting iterations
    while True:
        
        if frontier.isEmpty():
            print("Fail!")
            return None
            
        current_node = frontier.pop()

        #still print test
        if print_steps:
            print('\n')
            print('iteration: ', count)

            print(f'Frontier: {[str(x) for x in frontier]}')
            print(f'Explored: {[str(x) for x in explored]}')
            print(str(current_node))
            print('Path By Recur Search Node: ', current_node.get_node_path())
            print('isgoal: ', problem.isGoalState(current_node.state))

        #NOTE: only check for goal if node is being explored, 
        # do not check when successor is made 
        # cause it mess up the priority 
        if problem.isGoalState(current_node.state):
            print('done searching') 
            return current_node.get_node_path()
        explored.append(current_node)
        
        #for depth limited
        if limit is not None:
            if limit == current_node.depth: continue
         
        successors = problem.getSuccessors(current_node.state)
        # print(successors)
        #flip successor if generating in DFS (not flip is not wrong but just reversed)
        if isinstance(frontier,util.Stack): 
            successors = successors[::-1]
        
        #use for debugging and checking
        if print_steps:
            if successors == []:
                print('No possible move, abort current path!')
                input("Next? !")

        #get successor and expand search tree
        for successor in successors:
            suc_state, action, step_cost = successor
            child_node = SearchNode(
                suc_state,
                current_node.path_cost + step_cost,
                heuristics(suc_state,problem),
                parent = current_node,
                action = action,
                depth=current_node.depth + 1)
            
            in_explored = child_node in explored
            in_frontier = child_node in frontier
            if (not in_explored) and (isinstance(frontier,util.Stack) or (not in_frontier)):
                # print(f'child: {child_node}, in_explored: {in_explored} and in_frontier {in_frontier}')
                frontier.push(child_node)
            else:
                #update if uniform cost search 
                if isinstance(frontier,util.PriorityQueue):
                    for i, node in enumerate(explored):
                        if node == child_node:
                            # print('Oldnode: {}, newnode: {}'.format(node, child_node))
                            if node.better(child_node):
                                break
                            else:
                                print(f'Replaced in explored old: {node} with {child_node}')
                                explored[i] = child_node
                                break
                    frontier.update(child_node,child_node.heuristic + child_node.path_cost)
                if print_steps:
                    x= input('Has DupMove')
                    print(suc_state)
            

        #still print checking
        if print_steps:
            count+=1
            print('Remaining nodes: ', frontier.size())
            print('Checked: ', count)
            input("Press return for the next state...")
            print('\n')

def test_search_problem(problem,search_class, print_state = False, depth = None,heuristic = None):
    puzzle = problem.getStartState()
    
    print('Starting puzzle state:')
    print(puzzle)

    if heuristic is None:
        if depth is None:
             path = search_class(problem,print_state)
        else:
            path = search_class(problem,depth,print_state)
    else:
        path = search_class(problem,heuristic,print_state)

    if not path:
        print('Either cant solve or already start at goal!')
        return
    print('%s found a path of %d moves: %s' % (str(search_class.__name__),len(path), str(path)))
    # path = breadthFirstSearch(problem, print_state)
    # print('BFS found a path of %d moves: %s' % (len(path), str(path)))

    # path = depthFirstSearch(problem,print_state)
    # print('DFS found a path of %d moves: %s' % (len(path), str(path)))

    # path = uniformCostSearch(problem, print_state)
    # print('UCS found a path of %d moves: %s' % (len(path), str(path)))

    #NOTE: use for showing result states
    input("Press return to see solution states...")
    current_state = puzzle
    i = 1
    for a in path:
        current_state = current_state.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
        print(current_state)

        input("Press return for the next state...")   # wait for key stroke
        i += 1


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
