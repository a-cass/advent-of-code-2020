import os
import re
import argparse


def parse_bording_pass(src):
    """
    Parse expenses into list of values
    """
    vals = []
    with open(src) as f:
        line = f.readline()
        while line:
            if not line.isspace():
                val = line.strip()
                vals.append(val)
            line = f.readline()

    return vals


def seat_finder(bpass, row_range=range(0, 127), col_range=range(0, 9)):
    """
    Determine the seat location indicated by bpass
    """

    row_num = None
    col_num = None

    if len(row_range) == 1:
        row_num = row_range[0]
    if len(col_range) == 1:
        col_num = col_range[0]

    if row_num is not None and col_num is not None:
        return (row_num, col_num)

    c = bpass[0]
    middle_row = int(len(row_range) / 2)
    middle_col = int(len(col_range) / 2)
    if c.upper() == 'F':
        row_range = row_range[:middle_row]
    elif c.upper() == 'B':
        row_range = row_range[middle_row:]
    elif c.upper() == 'L':
        col_range = col_range[:middle_col]
    elif c.upper() == 'R':
        col_range = col_range[middle_col:]

    return seat_finder(bpass[1:], row_range, col_range)


def calculate_seatid(row,col):
    """
    Calculate SeatID from row and column numbers
    """
    return (row * 8) + col


if __name__ == '__main__':
    passes = parse_bording_pass('./boarding_passes.txt')
    seat_ids = []
    for p in passes:
        try:
            seat = seat_finder(p)
        except IndexError:
            raise Exception(f'Boarding "{p}" pass does not resolve to a seat')

        seat_id = calculate_seatid(*seat)
        print(seat_id, p)

        seat_ids.append(seat_id)

    seat_id_max = max(seat_ids)
    seat_id_min = min(seat_ids)
    remaining = set(range(seat_id_min, seat_id_max + 1)).difference(seat_ids)
    potential_seats = list(remaining)
    if len(potential_seats) == 1:
        potential_seats = potential_seats[0]

    print(f'Max SeatID = {seat_id_max}')
    print(f'Min SeatID = {seat_id_min}')
    print(f'My SeatID = {potential_seats}')
