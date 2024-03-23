from searchMPP import SearcherMPP
from stripsProblem import *
from stripsForwardPlanner import *
import time


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


def blocks_4_actions():
    """
      D
      B -> A C
    A C    B D
    """
    domain = create_blocks_world({'a', 'b', 'c', 'd'})
    problem = Planning_problem(domain,
                               {on('a'): 'table', clear('a'): True,
                                on('b'): 'c',  clear('b'): False,
                                on('c'): 'table', clear('c'): False,
                                on('d'): 'b', clear('d'): True,
                                },  # initial state
                               {on('a'): 'b', on('c'): 'd', on('b'): 'table', on('d'): 'table'})  # goal
    return problem


def main():
    reps = 100

    # problem = blocks_1()
    problem = blocks_4_actions()

    sum = 0

    for _ in range(reps):
        searcher = SearcherMPP(Forward_STRIPS(problem))  # A*
        t1 = time.time_ns()
        plan = searcher.search()
        dt = time.time_ns() - t1
        sum += dt

    print(f"Average time (ns): {sum / reps}")

    with open("result.txt", "w") as f:
        f.write(str(plan))


if __name__ == "__main__":
    main()


# from searchBranchAndBound import DF_branch_and_bound
# import stripsProblem

# SearcherMPP(Forward_STRIPS(stripsProblem.problem1)).search()  #A* with MPP
# DF_branch_and_bound(Forward_STRIPS(stripsProblem.problem1),10).search() #B&B
# To find more than one plan:
