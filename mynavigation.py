import search
import random
import puzzle
import copy

class NavigationNode:
    def __init__(self, name, paths = []):
        """
        paths = [] of (neighbor name, distance)
        """
        self.name = name
        self.paths = paths
    def __eq__(self, other):
        return self.name == other.name
    def __str__(self):
        return '(Label: {}, Neighbors: {})'.format(self.name,str(['({},{})'.format(n[0],n[1]) for n in self.paths]))

def getState(nav_map, node_name):
    for nav_node in nav_map:
        if nav_node.name == node_name:
            return nav_node

class NavigationState(puzzle.PuzzleState):
    """
    This class is the abstract class of any puzzle state
    """

    def __init__( self,nav_map,current_location, destination):
        """
        Data structure of the puzzle is defined here
        """
        self.nav_map = nav_map
        self.goal = destination
        self.current_location = current_location

        #path here is just for graphing
        self.path_cost = 0
        self.path = [self.current_location.name]
        self.init_node = current_location.name


    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.
          Boolean
        """
        # print(str(self.current_location), str(self.goal), 'done: ', self.current_location == self.goal)
        return self.current_location == self.goal

    def legalMoves(self):
        """
          Returns a list of legal moves from the current state.
          Move: (neighbor nav name, distance)
        """
        return self.current_location.paths



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
        new_state_name, distance = move
        new_state = getState(self.nav_map,new_state_name)
        new_puzzle.current_location = new_state
        new_puzzle.path_cost += distance
        new_puzzle.path.append(new_state_name)
        return new_puzzle


    # Utilities for comparison and display
    def __eq__(self, other):
        if self.current_location != other.current_location: return False
        # for p1, p2 in zip(self.path,other.path):
        #     if p1 != p2: return False
        return True

    def __hash__(self):
        util.raiseNotDefined()
    def __getAsciiString(self):
        """
          Returns a display string for the puzzle
        """
        import networkx as nx
        import matplotlib.pyplot as plt
        G = nx.DiGraph()
        graph = self.nav_map
        for graph_node in graph:
            vertex, edges = graph_node.name, graph_node.paths
            G.add_node("%s" % vertex)
            for edge,weight in edges:
                G.add_node("%s" % edge)
                G.add_edge("%s" % vertex, "%s" % edge, weight = weight)
                # print("'%s' it connects with '%s'" % (vertex,edge))
        # ---- END OF UNCHANGED CODE ----

        # Create positions of all nodes and save them
        pos = nx.spring_layout(G)

        # Draw the graph according to node positions
        nx.draw(G, pos, with_labels=True,node_color = 'gray',)

        # Create edge labels
        labels = {e: str(e) for e in G.edges}
        labels = nx.get_edge_attributes(G,'weight')

        # Draw edge labels according to node positions
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx_edges(G,pos,edgelist = G.edges,edge_color = 'black' , arrows= True,
            arrowsize=20)

        #hightlight start
        highlighted_node_name = self.init_node
        nx.draw_networkx(G.subgraph(highlighted_node_name), pos=pos, node_color='red')

        #hightlight end
        highlighted_node_name = self.goal.name
        nx.draw_networkx(G.subgraph(highlighted_node_name), pos=pos, node_color='green')

        # hightlight path
        path = self.path[1:]
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange')

        plt.show()



    def __str__(self):
        # return 'Node: {}, with path: {}'.format(self.current_location, self.path)
        self.__getAsciiString()
        return 'Printed puzzle in networkX'

class NavigationSearchProblem(search.SearchProblem):
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
            successor.append((ret, move, move[1]))
        return successor

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

def loadMap(n):
    """
        load map with index n (start 0)
    """
    GRAPH_DATA =    [
        {
            "A":[("B",5),("C",6)],
            "B":[("D",10),("E",1)],
            "C":[("E",8),("F",28)],
            "D":[("B",10),("G",3)],
            "E":[("B",1),("C",8)],
            "F":[("C",28),("G",15)],
            "G":[("D",3),("F",15)]
        },

        {
            '1': [('2',87)],
            '2': [('1',87),('3',92)],
            '3': [('2',92),('4',142)],
            '4': [('3',142),('5',98),('7',85)],
            '5': [('4',98),('6',86)],
            '6': [('5',86)],
            '7': [('4',85),('8',90),('9',101),('10',211)],
            '8': [('7',90)],
            '9': [('7',101),('11',97),('20',138)],
            '10': [('7',211),('12',99)],
            '11': [('9',97),('12',80),('20',146)],
            '12': [('10',99),('11',80),('13',151),('15',140)],
            '13': [('12',151),('14',71)],
            '14': [('13',71),('15',75)],
            '15': [('12',140),('14',75), ('16',118)],
            '16': [('15',118),('17',111)],
            '17': [('16',111),('18',70)],
            '18': [('17',70),('19',75)],
            '19': [('18',75),('20',120)],
            '20': [('9',138),('11',146),('19',120)]
        }
    ]
    return [NavigationNode(node_data[0],node_data[1]) for node_data in GRAPH_DATA[n].items()]

FARAGAS_10_DISTANCE = {
    '10': 0,
    '11': 1,
    '12': 2,
    '9': 3,
    '20': 4,
    '7': 5,
    '1': 6,
    '17': 7,
    '18': 8,
    '2': 9,
    '4': 10,
    '3': 11,
    '8': 12,
    '19': 13,
    '13': 14,
    '14': 15,
    '15': 16,
    '16': 17,
    '5': 18,
    '6': 19,
}
def euclid_heuristic(state):
    return FARAGAS_10_DISTANCE[state.current_location.name]*50

def test():
    # graph = loadMap()
    # init_node = graph[0]
    # goal_node = graph[5]
    # nav_puzzle = NavigationState(graph,init_node,goal_node)
    # print('Init: ', str(init_node))
    # print('Goal: ', str(goal_node))
    # problem = NavigationSearchProblem(puzzle= nav_puzzle)
    # start_state = problem.getStartState()
    # print('Start State: ')
    # print(start_state)
    # # print('Successors: ')
    # # print(str(problem.getSuccessors(start_state)))
    # moved_state = start_state
    # while(1):
    #     legal_moves = moved_state.legalMoves()
    #     for x in legal_moves:
    #         if x[0] in moved_state.path:
    #             continue
    #         move = x 
    #     moved_state = moved_state.result(move)
    #     state_name = moved_state.current_location.name
    #     print('Moved to {}!'.format(moved_state.current_location.name))
    #     print(moved_state.path,'with cost: ', moved_state.path_cost)
    #     print(moved_state)
    #     if state_name == 'G':
    #         print('GOT THERE')
    #         break

    return
        
    

if __name__ == '__main__':
    # test()
    # exit()
    graph = loadMap(1)
    print('Graph:')
    for i,x in enumerate(graph):
        print( 'node: ',x.name, 'index: ',i,)
    init_node = graph[input('Choose Starting Index?: ')]
    goal_node = graph[input('Choose Destination Index?: ')]
    nav_puzzle = NavigationState(graph,init_node,goal_node)
    print('Init: ', str(init_node))
    print('Goal: ', str(goal_node))
    problem = NavigationSearchProblem(puzzle= nav_puzzle)
    # search.test_search_problem(problem,search.uniformCostSearch,print_state=False)
    # search.test_search_problem(problem, search.greedySearch, print_state=True, heuristic=euclid_heuristic)
    search.test_search_problem(problem, search.stochasticHillClimb,heuristic = euclid_heuristic, print_state=True)
