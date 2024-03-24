from searchMPP import SearcherMPP
from stripsProblem import *
from stripsForwardPlanner import *
import time
from pprint import pprint


def move(x, y, z):
    """string for the 'move' action"""
    return 'move_'+x+'_from_'+y+'_to_'+z


def on(x):
    """string for the 'on' feature"""
    return x+'_is_on'


def clear(x):
    """string for the 'clear' feature"""
    return 'clear_'+x


def create_blocks_world(blocks):
    blocks_and_table = blocks | {'table'}
    # putting blocks on top of one another
    action_map = {
        Strips(
            move(x, y, z),                                # name
            {on(x): y, clear(x): True, clear(z): True},   # preconditions
            {on(x): z, clear(y): True, clear(z): False})  # effects
                                                          # default cost is 1
        for x in blocks
        for y in blocks_and_table
        for z in blocks
        if x != y and y != z and z != x
    }
    # putting blocks onto the table
    action_map.update({
        Strips(move(x, y, 'table'),               # name
               {on(x): y, clear(x): True},        # preconditions
               {on(x): 'table', clear(y): True})  # effects
        for x in blocks
        for y in blocks
        if x != y})

    # all blocks that x can be on
    feature_domain_dict = {
        on(x): blocks_and_table-{x} for x in blocks
    }
    # clear is either False or True
    feature_domain_dict.update({
        clear(x): boolean for x in blocks_and_table
    })
    return STRIPS_domain(feature_domain_dict, action_map)


def blocks_1():
    """
           C
      B -> A
    A C    B
    """
    blocks1dom = create_blocks_world({'a', 'b', 'c'})
    blocks1 = Planning_problem(blocks1dom,
                               {on('a'): 'table', clear('a'): True,
                                on('b'): 'c',  clear('b'): True,
                                on('c'): 'table', clear('c'): False},  # initial state
                               {on('a'): 'b', on('c'): 'a'})  # goal
    return blocks1


def problem_1():
    """
        D    A
        B -> E C
    E A C    B D
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd', 'e'})
    problem = Planning_problem(domain,
                               {on('a'): 'table', clear('a'): True,
                                on('b'): 'c',  clear('b'): False,
                                on('c'): 'table', clear('c'): False,
                                on('d'): 'b', clear('d'): True,
                                on('e'): 'table', clear('e'): True,
                                },  # initial state
                               {on('a'): 'e', on('c'): 'd', on('b'): 'table', on('d'): 'table', on('e'): 'b'})  # goal
    return problem

"""
	     C
	     E
    D -> A -> 	A -> A
    B 	 D    C	B    E C
E A C    B    E D    B D
"""

def problem_1a():
    """
    	     C
	         E
        D -> A
        B 	 D
    E A C    B
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd', 'e'})
    problem = Planning_problem(domain,
                               {on('a'): 'table', clear('a'): True,
                                on('b'): 'c',  clear('b'): False,
                                on('c'): 'table', clear('c'): False,
                                on('d'): 'b', clear('d'): True,
                                on('e'): 'table', clear('e'): True,
                                },  # initial state
                               {on('a'): 'd', on('c'): 'e', on('b'): 'table', on('d'): 'b', on('e'): 'a'})  # goal
    return problem

def problem_1b():
    """
    C
    E
    A ->   A
    D    C B
    B    E D
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd', 'e'})
    problem = Planning_problem(domain,
                               {on('a'): 'd', clear('a'): False,
                                on('b'): 'table',  clear('b'): False,
                                on('c'): 'e', clear('c'): True,
                                on('d'): 'b', clear('d'): False,
                                on('e'): 'a', clear('e'): False,
                                },  # initial state
                               {on('a'): 'b', on('c'): 'e', on('b'): 'd', on('d'): 'table', on('e'): 'table'})  # goal
    return problem

def problem_1c():
    """
    A      A
    C B -> E C
    E D    B D
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd', 'e'})
    problem = Planning_problem(domain,
                               {on('a'): 'c', clear('a'): True,
                                on('b'): 'd',  clear('b'): True,
                                on('c'): 'e', clear('c'): False,
                                on('d'): 'table', clear('d'): False,
                                on('e'): 'b', clear('e'): False,
                                },  # initial state
                               {on('a'): 'e', on('c'): 'd', on('b'): 'table', on('d'): 'table', on('e'): 'b'})  # goal
    return problem


def problem_2():
    """
    A
    B
    C -> A
    D    E D
    E    C B
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd', 'e'})
    problem = Planning_problem(domain,
                               {on('a'): 'b', clear('a'): True,
                                on('b'): 'c',  clear('b'): False,
                                on('c'): 'd', clear('c'): False,
                                on('d'): 'e', clear('d'): False,
                                on('e'): 'table', clear('e'): False,
                                },  # initial state
                               {on('a'): 'e', on('c'): 'table', on('b'): 'table', on('d'): 'b', on('e'): 'c'})  # goal
    return problem

"""
A    E
B    D
C -> C -> A   -> A
D    B    E C    E D
E    A    D B    C B
"""

def problem_2a():
    """
    A    E
    B    D
    C -> C
    D    B
    E    A
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd', 'e'})
    problem = Planning_problem(domain,
                               {on('a'): 'b', clear('a'): True,
                                on('b'): 'c',  clear('b'): False,
                                on('c'): 'd', clear('c'): False,
                                on('d'): 'e', clear('d'): False,
                                on('e'): 'table', clear('e'): False,
                                },  # initial state
                               {on('a'): 'table', on('c'): 'b', on('b'): 'a', on('d'): 'c', on('e'): 'd'})  # goal
    return problem

def problem_2b():
    """
    E
    D
    C -> A
    B    E C
    A    D B
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd', 'e'})
    problem = Planning_problem(domain,
                               {on('a'): 'table', clear('a'): False,
                                on('b'): 'a',  clear('b'): False,
                                on('c'): 'b', clear('c'): False,
                                on('d'): 'c', clear('d'): False,
                                on('e'): 'd', clear('e'): True,
                                },  # initial state
                               {on('a'): 'e', on('c'): 'b', on('b'): 'table', on('d'): 'table', on('e'): 'd'})  # goal
    return problem

def problem_2c():
    """
    A      A
    E C -> E D
    D B    C B
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd', 'e'})
    problem = Planning_problem(domain,
                               {on('a'): 'e', clear('a'): True,
                                on('b'): 'table',  clear('b'): False,
                                on('c'): 'b', clear('c'): True,
                                on('d'): 'table', clear('d'): False,
                                on('e'): 'd', clear('e'): False,
                                },  # initial state
                               {on('a'): 'e', on('c'): 'table', on('b'): 'table', on('d'): 'b', on('e'): 'c'})  # goal
    return problem

def problem_3():
    """
               A
    E   D -> C B
    B A C    D E
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd', 'e'})
    problem = Planning_problem(domain,
                               {on('a'): 'table', clear('a'): True,
                                on('b'): 'table',  clear('b'): False,
                                on('c'): 'table', clear('c'): False,
                                on('d'): 'c', clear('d'): True,
                                on('e'): 'b', clear('e'): True,
                                },  # initial state
                               {on('a'): 'b', on('c'): 'd', on('b'): 'e', on('d'): 'table', on('e'): 'table'})  # goal
    return problem

"""
         D
         C
      -> B -> C   ->   A
E   D    A    D E    C B
B A C    E    B A    D E
""" 

def problem_3a():
    """
             D
             C
          -> B
    E   D    A
    B A C    E
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd', 'e'})
    problem = Planning_problem(domain,
                               {on('a'): 'table', clear('a'): True,
                                on('b'): 'table',  clear('b'): False,
                                on('c'): 'table', clear('c'): False,
                                on('d'): 'c', clear('d'): True,
                                on('e'): 'b', clear('e'): True,
                                },  # initial state
                               {on('a'): 'b', on('c'): 'd', on('b'): 'e', on('d'): 'table', on('e'): 'table'})  # goal
    return problem

def problem_3b():
    """
    D
    C
    B -> C
    A    D E
    E    B A
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd', 'e'})
    problem = Planning_problem(domain,
                               {on('a'): 'e', clear('a'): False,
                                on('b'): 'a',  clear('b'): False,
                                on('c'): 'b', clear('c'): False,
                                on('d'): 'c', clear('d'): True,
                                on('e'): 'table', clear('e'): False,
                                },  # initial state
                               {on('a'): 'table', on('c'): 'd', on('b'): 'table', on('d'): 'b', on('e'): 'a'})  # goal
    return problem

def problem_3c():
    """
    C        A
    D E -> C B
    B A    D E
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd', 'e'})
    problem = Planning_problem(domain,
                               {on('a'): 'table', clear('a'): False,
                                on('b'): 'table',  clear('b'): False,
                                on('c'): 'd', clear('c'): True,
                                on('d'): 'b', clear('d'): False,
                                on('e'): 'a', clear('e'): True,
                                },  # initial state
                               {on('a'): 'b', on('c'): 'd', on('b'): 'e', on('d'): 'table', on('e'): 'table'})  # goal
    return problem


def no_heur(state, goal):
    return 0


def count_mismatches(state, goal):
    fuckup = 0
    for key, val in goal.items():
        assert key in state
        fuckup += val == state[key]

    return -fuckup


def benchmark(problems, heuristic, reps, show_plan=False):
    sum = 0

    for problem in problems:
        for _ in range(reps):
            searcher = SearcherMPP(Forward_STRIPS(problem, heuristic))  # A*
            searcher.max_display_level = 0
            t1 = time.time_ns()
            plan = searcher.search()
            dt = time.time_ns() - t1
            sum += dt

        if show_plan:
            print(f"Plan: {plan}")     

    avg_time = sum / reps
    # print(f"Average time (ns): {sum / reps}")

    return avg_time


def main():
    result = {}
    # result["case_1_naive"] = benchmark(
    #     [problem_1()], no_heur, 100, show_plan=True)
    # result["case_2_naive"] = benchmark(
    #     [problem_2()], no_heur, 100, show_plan=True)
    # result["case_3_naive"] = benchmark(
    #     [problem_3()], no_heur, 100, show_plan=True)

    # result["case_1_heuristic"] = benchmark(
    #     [problem_1()], count_mismatches, 100)
    # result["case_2_heuristic"] = benchmark(
    #     [problem_2()], count_mismatches, 100)
    # result["case_3_heuristic"] = benchmark(
    #     [problem_3()], count_mismatches, 100)
    

    result["case_1_with_sub-goals_naive"] = benchmark(
        [problem_1a(), problem_1b(), problem_1c()], no_heur, 100, show_plan=True)
    result["case_2_with_sub-goals_naive"] = benchmark(
        [problem_2a(), problem_2b(), problem_2c()], no_heur, 100, show_plan=True)
    result["case_3_with_sub-goals_naive"] = benchmark(
        [problem_3a(), problem_3b(), problem_3c()], no_heur, 100, show_plan=True)
    
    result["case_1_with_sub-goals_heuristic"] = benchmark(
        [problem_1a(), problem_1b(), problem_1c()], count_mismatches, 100)
    result["case_2_with_sub-goals_heuristic"] = benchmark(
        [problem_2a(), problem_2b(), problem_2c()], count_mismatches, 100)
    result["case_3_with_sub-goals_heuristic"] = benchmark(
        [problem_3a(), problem_3b(), problem_3c()], count_mismatches, 100)
    
    pprint(result)


# {'case_1_heuristic': 1857514.0,
#  'case_1_naive':     174237136.0,
#  'case_2_heuristic': 946137.0,
#  'case_2_naive':     121888077.0,
#  'case_3_heuristic': 1375991.0,
#  'case_3_naive':     185659843.0}


if __name__ == "__main__":
    main()


# from searchBranchAndBound import DF_branch_and_bound
# import stripsProblem

# SearcherMPP(Forward_STRIPS(stripsProblem.problem1)).search()  #A* with MPP
# DF_branch_and_bound(Forward_STRIPS(stripsProblem.problem1),10).search() #B&B
# To find more than one plan:
