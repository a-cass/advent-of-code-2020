import os
import re

# Validation specifications
passport_spec = {'byr': range(1920, 2003),
                 'iyr': range(2010, 2021),
                 'eyr': range(2020, 2031),
                 'hgt': list(range(59, 77)) + list(range(150, 193)),
                 'hcl': '#[\da-f]{6}',
                 'ecl': ['amb,', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
                 'pid': '\d{9}'}


class Passport(object):
    req_fields = ['byr', 'ecl', 'eyr', 'hcl', 'hgt', 'iyr', 'pid']

    def __init__(self, byr=None, ecl=None, eyr=None, hcl=None, hgt=None,
                 iyr=None, pid=None, cid=None):
        self.byr = byr
        self.ecl = ecl
        self.eyr = eyr
        self.hcl = hcl
        self.hgt = hgt
        self.iyr = iyr
        self.pid = pid
        self.cid = cid

    def req_present(self):
        return all([field is not None for field in self.req_fields])

    def req_valid(self, valid_dict):
        """
        Validate fields using spec in class
        """
        # Set all fields to True i.e. valid
        valid_results = dict({field:True for field in self.req_fields })

        for field, spec in valid_dict.items():
            valid_results[field] = self.validator(field, spec)

        return all(valid_results.values())

    def validator(self, field, valid_spec):
        """
        """
        if valid_spec is str:
            return re.match(valid_spec, str(getattr(self,field))) is not None
        else:
            return val in valid_spec



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
            is_valid = passport_obj.req_valid()

        if passport_obj.is_valid():
            count_valid += 1
        else:
            count_invalid += 1

    return dict(count_valid=count_valid, count_invalid=count_invalid)


print(process_passwords('./passports.txt'))
