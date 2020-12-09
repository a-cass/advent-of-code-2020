import os
from functools import reduce


def parse_answers(src,by='group',nline_sep=1):
    """
    Parse expenses into list of values
    """

    with open(src) as f:
        txt = f.read()

    groups = txt.split(os.linesep * (nline_sep + 1))

    return groups


def summarise_group(group_str):
    """
    """
    members = group_str.split(os.linesep)

    summary = {}

    for mnum, m in enumerate(members):
        summary[mnum + 1] = set(m)

    # Any - questions answered by anybody
    ans_any = reduce(lambda x, y: set(x).union(set(y)), members)
    summary['any'] = ans_any

    # All - questions answered by all
    ans_all = reduce(lambda x, y: set(x).intersection(set(y)), members)
    summary['all'] = ans_all

    return summary


if __name__ == '__main__':

    groups = parse_answers('./quiz_answers.txt')

    sum_any = 0
    sum_all = 0

    for grp in groups:
        print('GRP --> ', grp, '\n')
        summary = summarise_group(grp)
        sum_any += len(summary['any'])
        sum_all += len(summary['all'])

    print(f'Sum ANY: {sum_any}\nSum ALL: {sum_all}')