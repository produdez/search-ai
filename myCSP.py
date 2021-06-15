from typing import Any, Callable, Tuple, Type
from typing import List
from typing import Dict
from typing import Generic
from typing import TypeVar
from inspect import signature
from collections.abc import Sequence
import copy
# import util
#! ..................................................................................................

class Variable():
    def __init__(self,name: str, value ,domain: List) -> None:
        self.name = name
        self.value = value
        self.domain = domain
        self.new = True
        if not value in domain:
            raise ValueError(f'Value {str(value)} not in domain {str(domain)}')
    def check_valid_value(self):
        if not self.value in self.domain:
            raise ValueError(f'Value {str(self.value)} not in domain {str(self.domain)}')
    def __str__(self) -> str:
        if len(self.domain) == 0: return f'Var {self.name}, val: {self.value}, domain: []'
        else: return f'Var {self.name}, val: {self.value}, domain: {self.domain[0]} to {self.domain[-1]}'
    def isAssigned(self):
        return not self.new
    def assign(self, value):
        self.value = value
        self.new = False
        # self.check_valid_value()
    def __eq__(self, o: object) -> bool:
        if isinstance(o,Variable):
            return self.value == o.value  and self.isAssigned() and o.isAssigned()
        else: 
            return self.value == o 

class Constraint():
    def __init__(self,name,func: Callable[[List[Variable]],bool],*variables: Variable) -> None:
        self.name = name
        self.variables = variables
        self.count = len(variables)
        self.func = func
        self.func_param_len =len(signature(func).parameters)
        if self.func_param_len != len(variables):
            raise TypeError('Function parameter does not match variable count!')
    def non_assigned_count(self):
        return len([1 for x in self.variables if not x.isAssigned()])
    def isGood(self):
        # print([(x.name, x.isAssigned()) for x in self.variables])
        # Only check if all of the concerned values are assigned.
        if  self.non_assigned_count()  == 0:
            return self.func(*self.variables)
        return True
    def __str__(self) -> str:
        return f'Constraint: {self.name} for variables: {str([x.name for x in self.variables])}, {self.isGood()}, nonass:{self.non_assigned_count()}'

#! ..................................................................................................

class CSP_State:
    def __init__(self) -> None:
        self.variables: Dict[str,Variable] = dict()
        self.constraints: List[Constraint] = list()
    def var(self,var_name):
        return self.variables[var_name]
    def val(self,var_name):
        return self.variables[var_name].value
    def add_var(self,*var: Variable):
        for v in var:
            self.variables[v.name] = v
    def add_constraint(self, *constraint: Constraint):
        for con in constraint:
            self.constraints.append(con)
    def non_assigned_count(self):
        return len([1 for x in self.variables.values() if not x.isAssigned()])

    def isValid(self, assignment: Variable = None):
        '''Validate current state or newly assigned state'''
        if assignment is None:
            return all([con.isGood() for con in self.constraints])
        else:
            var_name,new_value = assignment.name,assignment.value
            old_var = self.var(var_name)
            old_value, old_new = old_var.value, old_var.new
            old_var.assign(new_value)
            result = self.isValid()
            old_var.value = old_value
            old_var.new = old_new
            return result
    def assign(self, move):
        self.variables[move.name].assign(move.value)

    def isComplete(self):
        return self.non_assigned_count() == 0
    
    def __getitem__(self, name):
        return self.variables[name]
    
    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.
          Boolean
        """
        return self.isValid() and self.non_assigned_count() == 0

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.
        """
        moves : List[str,Any] = []
        for var in self.variables.values():
            if not var.isAssigned(): #only assign one variable per move
                for value in var.domain:
                    move = Variable(var.name,value,var.domain)
                    if self.isValid(assignment=move):
                        moves.append(move)
                break
        return moves

    def result(self, move):
        ''' Copy to new puzzle and move there'''
        new_game=copy.deepcopy(self)
        new_game.assign(move)
        return new_game

    # Utilities for comparison and display
    def __eq__(self, other):
        return all([v1 == v2 for v1,v2 in zip(self.variables.values(), other.variables.values())])

    def __hash__(self):
        util.raiseNotDefined()
    def __getAsciiString(self):
        """
          Returns a display string for the puzzle
        """
        util.raiseNotDefined()

    def __str__(self):
        return self.__getAsciiString()


def test_var_class():
    x = Variable('x',5,range(1,10))
    y = Variable('y',5,range(1,10))
    print(x)
    s = lambda a,b: a.value + b.value
    print(s(x,y))
def test_constraint_class():
    x = Variable('x',5,range(1,10))
    y = Variable('y',5,range(1,10))
    non_equal = Constraint('not_equal', lambda a,b: a != b,x,y)
    print(non_equal, f'result: {non_equal.isGood()}')
def test_csp_state():
    x = Variable('x',5,range(1,10))
    y = Variable('y',6,range(1,10))
    non_equal = Constraint('not_equal', lambda a,b: a != b,x,y)
    game = CSP_State()
    game.add_var(x,y)
    game.add_constraint(non_equal)
    print(game.isValid())

#! ..................................................................................................

def diff2(a,b):
    return a.value != b.value
class Cryptharithmetic_State (CSP_State):

    def __init__(self) -> None:
        super(Cryptharithmetic_State,self).__init__()
        number_domain = list(range(0,10))
        t = Variable('t', 0, number_domain)
        w = Variable('w', 1, number_domain)
        o = Variable('o', 2, number_domain)
        f = Variable('f', 3, number_domain)
        u = Variable('u', 5, number_domain)
        r = Variable('r', 6, number_domain)
        x1 = Variable('x1', 7, number_domain)
        x2 = Variable('x2', 8, number_domain)
        x3 = Variable('x3', 9, number_domain)
        con1 = Constraint('c1',lambda o,r,x1: 2*o.value == r.value + x1.value * 10,o,r,x1)
        con2 = Constraint('c2',lambda w,u,x1,x2: 2*w.value + x1.value == u.value + x2.value * 10,w,u,x1,x2)
        con3 = Constraint('c3',lambda t,o,x2,x3: 2*t.value + x2.value == o.value + x3.value * 10,t,o,x2,x3)
        con4 = Constraint('c4',lambda x3,f: x3 == f,x3,f)
        self.add_constraint(con1,con2,con3,con4)
        self.add_var(f,x3,x1,x2,t,w,o,u,r)
        
        #all diff constraints
        diff_vars = [t,w,o,f,u,r]
        n= len(diff_vars)
        for i in range(n):
            for j in range(i+1,n):
                self.add_constraint(Constraint(f'diff{i*n+j}',diff2,diff_vars[i],diff_vars[j]))

        #NOTE: extra non zero constraints
        nonz1 = Constraint('non0_1',lambda x: not (x==0),f)
        nonz2 = Constraint('non0_2',lambda x: not (x==0),t)
        # #NOTE: hints
        # fone = Constraint('f==1',lambda x: x == 1, f)
        # x1less = Constraint('x1<=1', lambda x: x.value <= 1,x1)
        # x2less = Constraint('x2<=1', lambda x: x.value <= 1,x2)
        self.add_constraint(nonz1,nonz2)
    
      
    def __getAsciiString(self):
        """
          Returns a display string for the puzzle
        """
        result = []
        assigned_vars = []
        non_assigned_vars = []
        for v in self.variables.values():
            if v.isAssigned():
                assigned_vars.append(f'{v.name} : {v.value}')
            else: 
                non_assigned_vars.append(f'{v.name}')
        result.append('Assigned: '+', '.join(assigned_vars))
        result.append('Not_Assigned: '+', '.join(non_assigned_vars))
        return '\n'.join(result) + '\n'
    def __str__(self):
        return self.__getAsciiString()



def queen_free(q1: Variable, q2: Variable):
    i1,j1 = int(q1.name[-1]),q1.value
    i2,j2 = int(q2.name[-1]),q2.value
    if i1 == i2 or j1 == j2: return False
    if abs(i1-i2) == abs(j1-j2): return False
    return True
class NQueenState (CSP_State):

    def __init__(self, n = 4) -> None:
        super(NQueenState,self).__init__()
        queen_domain = list(range(0,n))
        self.board_size = n
        #vars
        for i in range(n):
            queen_var = Variable(f'Q{i}',i,queen_domain)
            self.add_var(queen_var)
        #constraints
        for i in range(n):
            for j in range(i+1,n):
                constraint = Constraint(f'QCheck{i},{j}',queen_free,self.var(f'Q{i}'),self.var(f'Q{j}'))
                self.add_constraint(constraint)
    
      
    def __getAsciiString(self):
        """
          Returns a display string for the puzzle
        """
        queen_postions = [queen.value if queen.isAssigned() else None for queen in self.variables.values()]
        lines = []
        horizontalLine = ('-' * (4* self.board_size+1))
        lines.append(horizontalLine)
        for row in range(self.board_size):
            rowLine = '|'

            for i in range(self.board_size):
                col = ''
                if queen_postions[row] == i:
                    col = 'Q'
                else:
                    col = ' '

                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

def test_nqueen_state():
    init = NQueenState()
    print(init)
    for move in init.legalMoves():
        print(init.result(move))
# test_nqueen_state()
#! ..................................................................................................
class MapColoringState(CSP_State):
    def __init__(self) -> None:
        super().__init__()
        color_range = ['red','blue','green']
        var_names = ['WA','NT','Q','NSW','V','SA','T']
        var_count = len(var_names)
        for var_name in var_names:
            self.add_var(Variable(var_name,'red',color_range))
        diff_color = lambda a,b: not(a==b)
        adj_pairs = [('WA','NT'),('WA','SA'),('NT','SA'),('NT','Q'),('SA','Q'),('SA','NSW'),('SA','V'),('Q','NSW'),('NSW','V')]
        for name1,name2 in adj_pairs:
            v1,v2 = self.var(name1), self.var(name2)
            self.add_constraint(Constraint(f'Diff {name1},{name2}',diff_color,v1,v2))
        # for i in range(var_count):
        #     for j in range(i+1,var_count):
        #         v1, v2 = self.var(var_names[i]), self.var(var_names[j])
        #         self.add_constraint(Constraint(f'DiffCol{i*var_count + j}',diff_color,v1,v2))

    def __getAsciiString(self):
        """
          Returns a display string for the puzzle
        """
        result = []
        assigned_vars = []
        non_assigned_vars = []
        for v in self.variables.values():
            if v.isAssigned():
                assigned_vars.append(f'{v.name} : {v.value}')
            else: 
                non_assigned_vars.append(f'{v.name}')
        result.append('Assigned: '+', '.join(assigned_vars))
        result.append('Not_Assigned: '+', '.join(non_assigned_vars))
        return '\n'.join(result) + '\n'
    def __str__(self):
        return self.__getAsciiString()
def test_mapcolorstate():
    mapc = MapColoringState()
    print(mapc)
    for move in mapc.legalMoves():
        print(mapc.result(move))
# test_mapcolorstate()

#! ..................................................................................................

def recursive_backtrack(csp_state: CSP_State,prt = False, pause = False):
    if csp_state.isGoal():
        print('Found')
        return csp_state
    valid_moves = csp_state.legalMoves() #valid moves of one var
    if prt:
        print('Current State')
        print(csp_state)
    if pause:
        input('Next?')
    for move in valid_moves:
        result = recursive_backtrack(csp_state.result(move))
        if not result is None:
            return result
    return None #failure
    


#! ..................................................................................................

def search_problem(problem = Cryptharithmetic_State()):
    print('Init problem:')
    print(problem)
    init_state = problem
    search_stack = [init_state]
    explored = []
    ilteration = 0
    prt = False
    pause = False
    slowdown = False
    slow_print = False
    if prt:
        for c in init_state.constraints:
                print(c)

    if init_state.isGoal():
        return init_state
    while(1):
        state = search_stack.pop()
        if state.isGoal():
            return state
        explored.append(state)
        #print test
        if prt:
            print('Ilteration: ',ilteration,'.........')
            ilteration += 1
            print(state)
            if state.non_assigned_count() <= 1:
                for c in state.constraints:
                    print(c)
                if slow_print: slowdown = input('Important Pause, wanna slowdown?')
            for c in state.constraints:
                print(c)
        
        successor_state = [state.result(move) for move in state.legalMoves()][::-1]
        if prt: print('Succ Statets: ')
        for succ in successor_state:

            appended = False
            if slowdown:
                print('Exploring Sucss')
                print(succ)
                for c in succ.constraints:
                    print(c)
            if succ in explored or succ in search_stack: 
                if slowdown: 
                    print('skipped')
                        
                continue
            search_stack.append(succ)
            appended = True
            if prt: print(succ)
        if pause or slowdown: input('Next?')
        if not appended: slowdown = False


#! ..................................................................................................


def test_cryptarithmetic():
    
    result = search_problem()
    print('Result:')
    print(result)

def test_nqueen():
    n = input('Nqueen?, n=?')
    result = search_problem(NQueenState(n=int(n)))
    print('Result:')
    print(result)
def test_map_color():
    result = search_problem(MapColoringState())
    print('Result:')
    print(result)
#! ..................................................................................................

def backtrack_nqueen():
    n = input('Nqueen?, n = ?')
    result = recursive_backtrack(NQueenState(n=int(n)))
    print('Result:')
    print(result)
def backtrack_cryptoarithmetic():
    result = recursive_backtrack(Cryptharithmetic_State())
    print('Result:')
    print(result)
def backtrack_mapcoloring():
    result = recursive_backtrack(MapColoringState())
    print('Result:')
    print(result)


#! ..................................................................................................
def isBinaryConstrant(con: Constraint):
    return con.count == 2
def arc_3(csp: CSP_State):
    arcs = set([con for con in csp.constraints if isBinaryConstrant(con)])
    while len(arcs) != 0:
        arc = arcs.pop()
        if check_arc_consistency(arc):
            x1, x2 = arc.variables
            if x1.domain.empty(): return False
            arcs.update(get_neighbors(x1,csp, exclude=x2))
        
def check_arc_consistency(arc: Constraint):
    x1,x2 = arc.variables
    func = arc.func
    non_consistent_x1_values = []
    for vx1 in x1.domain:
        temp_x1 = copy.copy(x1)
        temp_x1.assign(vx1)
        consistant = False
        for vx2 in x2.domain:
            temp_x2 = copy.copy(x2)
            temp_x2.assign(vx2)
            # print('Vals: ', temp_x1, temp_x2,'Result: ', func(temp_x1,temp_x2))
            if func(temp_x1,temp_x2):
                consistant = True
                break
        if not consistant:
            # print('not-con at', temp_x1)
            non_consistent_x1_values.append(vx1)
    # print(f'Var1: {x1}, Var2: {x2}')
    # print('Inconsistence: ', non_consistent_x1_values)
    [x1.domain.remove(val) for val in non_consistent_x1_values]

    #NOTE: check the reverse direction
    check_arc_consistency(Constraint('Reversed', func,x2,x1))

def improved_backtrack(csp_state: CSP_State,prt = False, pause = False):
    if csp_state.isGoal():
        print('Found')
        return csp_state
    #NOTE: Here use 3-arc to prune domain before finding new moves.
    arc_3(csp_state)
    valid_moves = csp_state.legalMoves() #valid moves of one var
    if prt:
        print('Current State')
        print(csp_state)
    if pause:
        input('Next?')
    for move in valid_moves:
        result = recursive_backtrack(csp_state.result(move))
        if not result is None:
            return result
    return None #failure

def test_check_arc_con():
    v1 = Variable('V1',5,list(range(0,10)))
    v2 = Variable('V2',5,list(range(0,10)))
    con = Constraint('Square',lambda x,y: x.value ** 2 == y.value,v1,v2)
    check_arc_consistency(con)
    print(v1,v2)
# test_check_arc_con()

def get_neighbors(variable: Variable, csp: CSP_State,exclude = None):
    neighbor = set()
    for arc in csp :
        if isBinaryConstrant(arc) and  variable in arc.variables:
            neighbor.update([val for val in arc.variables if val not in [variable, exclude]])
    return neighbor
def test_arc_3():
    modded_queen_csp = NQueenState()
    modded_queen_csp.var('Q1').domain = [1]
    modded_queen_csp.var('Q1').assign(1)

    print('Before:')
    for v in modded_queen_csp.variables.values(): print(v,'assign: ',v.isAssigned())
    arc_3(modded_queen_csp)
    print('After:')
    for v in modded_queen_csp.variables.values(): print(v,'assign: ',v.isAssigned())


from time import time
#TODO: This is wrong due to implementation maybe, fix later
def test_improved_backtrack():
    n = 12
    t1 = time()
    result = recursive_backtrack(NQueenState(n=n))
    print('Traditional Recursive Backtrack time: ', time() - t1)

    t2 = time()
    result = improved_backtrack(NQueenState(n = n))
    print('Improved Recursive Backtrack time: ', time() - t2)
# test_improved_backtrack()

#! ..................................................................................................
import random
def random_conflict_var(state: CSP_State):
    shuffled_conflict_list = random.sample(state.constraints,len(state.constraints))
    for cons in shuffled_conflict_list:
        if not cons.isGood(): 
            return cons.variables[random.randint(0, len(cons.variables) -1)]
def min_conflict_value(var: Variable, state: CSP_State):
    old_val = var.value
    best_val = None
    min_conflict_count = len(state.constraints)
    for val in var.domain:
        if val == old_val: continue
        var.assign(val)
        conflict_count =sum([not c.isGood() for c in state.constraints])
        if conflict_count < min_conflict_count:
            min_conflict_count = conflict_count
            best_val = val
    var.assign(old_val)
    return best_val

    

def local_search_min_conflict(state: CSP_State, max_steps = 10000, print_step = True):
    #NOTE: random select conflicted and resolve that until finish
    if not state.isComplete():
        raise TypeError('Puzzle State is not complete!')
    for _ in range(max_steps):
        if print_step: print(state)
        if state.isGoal(): return state
        chosen_var = random_conflict_var(state)
        min_conflict_val = min_conflict_value(chosen_var, state)
        chosen_var.assign(min_conflict_val)

def random_complete_assign(csp: CSP_State):
    for var in csp.variables.values():
        random_val = random.choice(var.domain)
        var.assign(random_val)
def test_local_search_csp():
    state = NQueenState(4)
    random_complete_assign(state)
    print('Random State For Local Search: ')
    print(state)
    local_search_min_conflict(state)
    print('Successful? ', state.isGoal())
    print('Final State: ', state)
# test_local_search_csp()
    

if __name__ == '__main__':
    # test_var_class()
    # test_constraint_class()
    # test_csp_state()
    # test_cryptarithmetic()
    # test_nqueen()
    # test_map_color()



    # backtrack_nqueen()
    # backtrack_cryptoarithmetic()
    # backtrack_mapcoloring()

    pass