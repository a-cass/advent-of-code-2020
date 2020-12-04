import os
import re
import argparse
from warnings import warn


PW_PTTN = '(?P<nmin>\d{1,2})-(?P<nmax>\d{1,2})\s(?P<char>[a-z]{1}):\s(?P<password>.*)'


def char_count_validate(password,char,nmin,nmax):
    '''
    Validate character count in password.
    '''
    if int(nmin) <= password.count(char) <= int(nmax):
        return True
    else:
        return False


def char_pos_validate(password,char,nmin,nmax):
    '''
    Validate character position in password.
    '''
    pos1, pos2 = int(nmin) - 1, int(nmax) - 1
    return (password[pos1] == char) ^ (password[pos2] == char)


def validate_passwords(pw_src,line_pttn=PW_PTTN,valid_func=char_count_validate):
    '''
    Validate North Pole Toboggan Rental Shop passwords.
    '''
    line_pttn = re.compile(line_pttn)
    count_pass = 0
    
    with open(pw_src) as f:
        line = f.readline()
        while line:
            m = line_pttn.match(line.strip())
            if m is None:
                warn(f'Failed to parse "{line}"')
            else:
                # Perform validation
                if valid_func(**m.groupdict()):
                    count_pass += 1

            line = f.readline()

    return count_pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Password Validator',
                                     description='Advent of Code 2020 Solution 2')
    parser.add_argument('password_list', help='Path to password list')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--char-count', action='store_true',
                       help='Validate using character count',default=True)
    group.add_argument('-p', '--char-pos', action='store_true',
                       help='Validate using character position')

    args = parser.parse_args()

    if args.char_pos:
        func = char_pos_validate
    else:
        func = char_count_validate

    count_valid = validate_passwords(args.password_list,valid_func=func)
    print(f'Count valid: {count_valid}')
