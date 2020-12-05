import os
import numpy as np
from functools import reduce
from operator import mul


def map_biome(map_src, clear='.', blocked='#', repeat=0):
    """
    """

    translate_chars = {clear: '1',
                       blocked: '0'}

    arr = None
    with open(map_src) as f:
        line = f.readline().strip()
        while line:
            translation = str.translate(line, str.maketrans(translate_chars))
            line_arr = np.array(list(translation), dtype=np.int8)

            if arr is None:
                arr = line_arr

            else:
                arr = np.vstack((arr, line_arr))

            line = f.readline().strip()

    if repeat > 0:
        arr = np.tile(arr, repeat)

    return arr


def traverse_biome(biome, start_coords=(0, 0), step_l=0, step_r=1, step_u=0,
                   step_d=1, max_steps=5000, biome_end_row=None,
                   biome_end_col=None, verbose=False):
    """
    Traverse the biome using the specified directional steps.
    """

    pos_x, pos_y = start_coords
    biome_l, biome_w = biome.shape
    biome_end_row = biome_end_row or np.inf
    biome_end_col = biome_end_col or np.inf

    step_count = 0
    block_count = 0
    valid_count = 0

    if step_l == step_r == step_u == step_d == 0:
        if verbose:
            print('You cannot traverse by taking 0 steps!')
    else:
        while True:
            if step_count == max_steps:
                break

            # Determine new pos using steps.
            new_x = pos_x - step_l + step_r
            new_y = pos_y - step_u + step_d

            if new_x >= biome_end_col or new_y >= biome_end_row:
                break

            # Modulo is used to account for positions outside of biome.shape
            # and allow essentially an infinite scroll through repeating tiles
            # of the biome.
            new_x = new_x % biome_w
            new_y = new_y % biome_l

            if biome[new_y, new_x]:
                valid_count += 1
                msg = 'Weeee...'

            else:
                block_count += 1
                msg = 'Ouch!...'

            if verbose:
                print(msg)

            step_count += 1
            pos_x, pos_y = new_x, new_y

    return dict(step_count=step_count, valid_count=valid_count,
                block_count=block_count)


if __name__ == '__main__':
    b = map_biome('./biome.txt')

    routes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    tree_count = {}
    for i, (step_r, step_d) in enumerate(routes):
        res = traverse_biome(b, step_r=step_r, step_d=step_d,
                             biome_end_row=b.shape[0])
        tree_count[i + 1] = res['block_count']

    print(tree_count)
    print(reduce(mul, tree_count.values()))
