import sys
import argparse
from itertools import combinations
from functools import reduce
from operator import mul


def parse_expenses(src):
    '''
    Parse expenses into list of values
    '''
    vals = []
    with open(src) as f:
        line = f.readline()
        while line:
            val = int(line.strip())
            vals.append(val)
            line = f.readline()

    return vals


def number_cruncher(values, nvars=2, target_sum=2020):
    '''
    Crunch numbers for the elves
    '''

    for combo in combinations(values, nvars):
        if sum(combo) == target_sum:
            return combo


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Expenses Fixer',
                                     description='Advent of Code 2020 Solution 1')
    parser.add_argument('report', help='Path to expenses report')
    parser.add_argument('-n', '--num-vars', type=int, help='Number of expenses to sum', default=2)
    parser.add_argument('-t', '--target', type=int, help='Value the expenses must sum to', default=2020)

    args = parser.parse_args()

    vals = parse_expenses(args.report)
    combo = number_cruncher(vals, args.num_vars, args.target)

    print(f'Expenses combo : {combo}')
    print(f'Combo product : {reduce(mul, combo)}')