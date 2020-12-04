import os
import numpy as np


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
                arr = line_arr.copy()

            else:
                arr = np.concatenate(arr, line_arr)

            line = f.readline().strip()

    if repeat > 0:
        arr = np.tile(arr, repeat)

    return arr


def traverse_biome(biome,step_l=0,step_r=0,step_u=0,step_d=0):
    """
    Traverse the biome using the specified directional steps.
    """
    if step_l == step_r == step_u == step_d == 0:
        print('NO!')

    if tree:
        print('Ouch!')


if __name__ == '__main__':
    r = map_biome('./biome.txt')
    print(r.shape)
    print(r)
