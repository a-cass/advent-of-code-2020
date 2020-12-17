"""
BAG FACTORY

Module for parsing of bag rules and creation of Bag objects.

"""
import os
import re

# Default location for rules file
RULES_SRC = './bags.txt'


def parse_rules(bag_list=RULES_SRC):
    """
    Parse file of bag rules to dictionary.

    Parameters
    ----------
    bag_list: str, optional
        Path to source file. The default path is determined from the
        module constant `RULES_SRC`.

    Returns
    -------
    rules: dict(str:dict(str:int))
        Dictionary of bag colours and corresponding rules for each bag
        identified in `bag_list`. Keys are bag colours; values are
        acceptance rules for each bag. Acceptance rules are dictionaries
        of the form colour:max allowed.

    """
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


# On initialisation set bag rules to result of parsing the file RULES_SRC
BAG_RULES = parse_rules()


def get_bag(colour, rules=BAG_RULES):
    """
    Creates a Bag object using the colour and rules specified.

    Parameters
    ----------
    colour: str
        Colour of bag to construct
    rules: dict(str:dict(str:int)), optional
        Dictionary of bag colours and corresponding rules. Keys are bag
        colours; values are acceptance rules for each bag. Acceptance
        rules are dictionaries of the form colour:max allowed.The default
        value uses rules from module constant `BAG_RULES`, determined on
        module initialisation.

    Returns
    -------
    Bag
        `Bag` object with associated colour rules.

    Raises
    ------
    KeyError
        If specified colour is not found in `rules` keys.

    """
    try:
        bag_accepts = rules[colour]
        return Bag(colour, bag_accepts)
    except KeyError as e:
        e.args = (f'No rules found for bag colour "{colour}"',)
        raise e


def iter_bags(rules=BAG_RULES):
    """
    Iterate through all available bags in the rules dictionary.

    At each iteration a Bag object is constructed based on the
    corresponding rules.

    Parameters
    ----------
    rules: dict(str:dict(str:int)), optional
        Dictionary of bag colours and corresponding rules. Keys are bag
        colours; values are acceptance rules for each bag. Acceptance
        rules are dictionaries of the form colour:max allowed.The default
        value uses rules from module constant `BAG_RULES`, determined on
        module initialisation.

    Yields
    ------
    Bag
        `Bag` object with associated colour rules.

    """
    for bag_colour, bag_accepts in BAG_RULES.items():
        yield Bag(bag_colour, bag_accepts)


class Bag(object):
    """
    A bag object of a particular colour.

    Bags may have other bags inside them and have rules determining
    the colours and amount of these inner bags.

    Parameters
    __________
    colour: str
        Bag colour.
    accepts: dict(str:int))
        Acceptance rules for inner bags. Keys are accepted colours, values are
        the maximum allowed amount of each bag.

    """
    def __init__(self, colour, accepts=None):
        self.colour = colour
        self.accepts = accepts
        self.contents = {k: 0 for k in accepts.keys()}

    def total_bags(self):
        """
        Total number of inner bags allowed inside this bag.

        As inner bags may themselves have inner bags this function is
        recursive. The total for this bag is made up of the contents of
        accepted inner bags multiplied by the maximum allowed amount of
        each bag.

        Returns
        -------
        total: int
            Total amount of inner bags.

        """
        total = 0
        for accept_colour, accept_count in self.accepts.items():
            total += accept_count
            new_bag = get_bag(accept_colour)
            total += (accept_count * new_bag.total_bags())

        return total

    def can_accept(self, colour, colours_seen=None):
        """
        Determines if this bag can contain a bag of the specified colour.

        A check is performed to see if this bag can directly contain the
        specified bag i.e. it is an accepted inner bag. If it cannot the
        list of accepted bags are then searched recursively.

        The `colours_seen` argument is used to keep track of the inner
        bags already checked and avoid infinite checks.

        Parameters
        ------
        colour: str
            Colour of bag to check.
        colours_seen: list of str, optional
            List of inner bag colours already checked; default is None.
            This parameter is used when traversing inner bags. Bags
            already checked are not checked again.

        Returns
        -------
        accepted: bool
            True if this bag can contain the specified bag either directly
            or through inner bags.

        """
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
    print(globals())