import os
import re
import bag_factory as bf

tgt_colour = 'shiny gold'
accept_tgt = []
tgt_contents = 0

for b in bf.iter_bags():
    if b.can_accept(tgt_colour):
        accept_tgt.append(b.colour)
    if b.colour == tgt_colour:
        tgt_contents += b.total_bags()

print(f'Number of Bags that can contain "{tgt_colour}": {len(accept_tgt)}')
print(f'Number of Bags contained by "{tgt_colour}": {tgt_contents}')

