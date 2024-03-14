from searchMPP import SearcherMPP
from stripsProblem import *
from stripsForwardPlanner import *


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


blocks1dom = create_blocks_world({'a', 'b', 'c'})
blocks1 = Planning_problem(blocks1dom,
                           {on('a'): 'table', clear('a'): True,
                            on('b'): 'c',  clear('b'): True,
                               on('c'): 'table', clear('c'): False},  # initial state
                           {on('a'): 'b', on('c'): 'a'})  # goal

blocks2dom = create_blocks_world({'a', 'b', 'c', 'd'})
tower4 = {clear('a'): True, on('a'): 'b',
          clear('b'): False, on('b'): 'c',
          clear('c'): False, on('c'): 'd',
          clear('d'): False, on('d'): 'table'}
blocks2 = Planning_problem(blocks2dom,
                           tower4,  # initial state
                           {on('d'): 'c', on('c'): 'b', on('b'): 'a'})  # goal

blocks3 = Planning_problem(blocks2dom,
                           tower4,  # initial state
                           {on('d'): 'a', on('a'): 'b', on('b'): 'c'})  # goal

# from searchBranchAndBound import DF_branch_and_bound
# import stripsProblem

# SearcherMPP(Forward_STRIPS(stripsProblem.problem1)).search()  #A* with MPP
# DF_branch_and_bound(Forward_STRIPS(stripsProblem.problem1),10).search() #B&B
# To find more than one plan:
s1 = SearcherMPP(Forward_STRIPS(blocks2))  # A*
s1.search()  # find another plan
# s1.search()  # find another plan
