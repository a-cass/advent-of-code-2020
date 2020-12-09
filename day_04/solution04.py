import os
import re
import argparse

# Validation specifications
height_pttn = '^((?:1[5-8][0-9]cm)|(?:19[0-3]cm)|(?:59in)|(?:6[0-9]in)|' \
              '(?:7[0-6]in))$'
passport_criteria = {'byr': range(1920, 2003),
                     'iyr': range(2010, 2021),
                     'eyr': range(2020, 2031),
                     'hgt': height_pttn,
                     'hcl': '^#[\da-f]{6}$',
                     'ecl': ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
                     'pid': '\d{9}$'}


class Passport(object):
    req_fields = ['byr', 'ecl', 'eyr', 'hcl', 'hgt', 'iyr', 'pid']

    def __init__(self, byr=None, ecl=None, eyr=None, hcl=None, hgt=None,
                 iyr=None, pid=None, cid=None):
        self.byr = int(byr) if byr is not None else byr
        self.ecl = ecl
        self.eyr = int(eyr) if eyr is not None else eyr
        self.hcl = hcl
        self.hgt = hgt
        self.iyr = int(iyr) if iyr is not None else iyr
        self.pid = pid
        self.cid = cid

    def req_present(self):
        return all([getattr(self, field) is not None
                    for field in self.req_fields])

    def req_valid(self, valid_dict):
        """
        Validate req fields using spec in class
        """
        # Set all fields to False i.e. invalid
        valid_results = dict({field: False for field in self.req_fields})

        for field, criteria in valid_dict.items():
            valid_results[field] = self.validator(field, criteria)

        return all(valid_results.values())

    def validator(self, field, criteria):
        """
        """
        val = getattr(self, field)

        if val is None:
            return False
        elif isinstance(criteria, str):
            return re.match(criteria, str(val)) is not None
        else:
            return val in criteria


def process_passports(passport_batch, nline_sep=1, valid_method=None):
    """
    Validate passports in batch file.

    valoid method: None, present, 'value'

    """
    count_valid = 0
    count_invalid = 0

    passport_str = ''
    with open(passport_batch) as f:
        txt = f.read()

    passports = txt.split(os.linesep * (nline_sep + 1))

    while passports:
        passport = passports.pop()

        if passport.isspace():
            continue

        kv_str = passport.split()
        passport_dict = dict([s.split(':') for s in kv_str])
        passport_obj = Passport(**passport_dict)

        is_valid = True
        if valid_method == 'present':
            is_valid = passport_obj.req_present()
        elif valid_method == 'value':
            is_valid = passport_obj.req_valid(valid_dict=passport_criteria)

        if is_valid:
            count_valid += 1
        else:
            count_invalid += 1

    return dict(count_valid=count_valid, count_invalid=count_invalid)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Passport Validator',
                                     description='Advent of Code 2020 '
                                                 'Solution 4'
                                     )
    parser.add_argument('passport_batch', help='Path to password batch file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-rp', '--req-present', action='store_true',
                       help='Validate that all required values are present'
                       )
    group.add_argument('-rv', '--req-value', action='store_true',
                       help='Validate that all required values are present '
                            'and valid'
                       )

    args = parser.parse_args()
    valid_method = None
    if args.req_present:
        valid_method = 'present'
    elif args.req_value:
        valid_method = 'value'

    print(process_passports(args.passport_batch, valid_method=valid_method))
