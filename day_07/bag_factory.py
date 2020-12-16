"""
BAG FACTORY
"""
import os
import re

RULES_SRC = './bags.txt'


def parse_rules(bag_list=RULES_SRC):
    rules = {}
    with open(bag_list) as f:
        line = f.readline()
        while line:
            line = line.strip()
            bag_colour = re.match('.*(?=\sbags contain)', line).group()
            bag_accepts = {}
            for m in re.finditer(
                    '((?P<count>\d+)\s(?P<colour>[a-z\s]*))(?=\sbags?[,.])',
                    line):
                bag_accepts.update({m.group('colour'): int(m.group('count'))})

            rules.update({bag_colour:bag_accepts})
            line = f.readline()

    return rules


BAG_RULES = parse_rules()


def get_bag(colour, rules=BAG_RULES):
    try:
        bag_accepts = rules[colour]
        return Bag(colour, bag_accepts)
    except KeyError as e:
        e.args = (f'No rules found for bag colour "{colour}"',)
        raise e


def iter_bags(rules=BAG_RULES):
    """
    """
    for bag_colour, bag_accepts in BAG_RULES.items():
        bag = Bag(bag_colour, bag_accepts)
        yield bag


class Bag(object):
    def __init__(self, colour, accepts=None):
        self.colour = colour
        self.accepts = accepts
        self.contents = {k: 0 for k in accepts.keys()}

    def total_bags(self):
        total = 0
        for accept_colour, accept_count in self.accepts.items():
            total += accept_count
            new_bag = get_bag(accept_colour)
            total += (accept_count * new_bag.total_bags())

        return total

    def can_accept(self, colour, colours_seen=None):
        if colour in self.accepts.keys():
            return True
        else:
            if colours_seen is None:
                colours_seen = []

            accepted = False
            for accept_colour in self.accepts.keys():
                if accept_colour in colours_seen:
                    continue

                new_bag = get_bag(accept_colour)
                accepted = new_bag.can_accept(colour, colours_seen)
                colours_seen.append(accept_colour)

                if accepted:
                    break

            return accepted


if __name__ == '__main__':
    bag = get_bag('shiny gold')
    print(bag.colour)
    print(bag.accepts)
