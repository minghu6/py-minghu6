# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""PwdKeeper
a small password keeper, query or add username-password by interactive
list (alias ls l)        #list all label
query          <label>
add            <label> <username> <password>
del-account    <label> <username-todel>
del-label      <old-label> <new-label>
update-account <label> <username> <new-password>
update-label   <old-label> <new-label>
q              # quit
?              # for help

Usage:
  pwd_keeper <path> [--password=<master-pwd>] [--username=<username>]

Options:
  <path>                      account file path to connect
  -u --username=<username>    your account name for pwd_keeper, using fo check account file
  -p --password=<master-pwd>  master password

"""

import os
import getpass

import minghu6
from docopt import docopt
from minghu6.etc.logger import SmallLogger
from minghu6.security.des import des
from color import color
from minghu6.text.seq_enh import split_whitespace, split_blankline


class UsernameMatchError(BaseException): pass


class PwdKeeper:
    def __init__(self, path, master_password, check_username=False, username=None):

        self.path = path
        self.master_password = des.valid_key(master_password)
        self.logger = SmallLogger()
        if not os.path.exists(path):
            self.write_back(username)
        self.logger.read_log(path,
                             format_func=lambda section_name, line, sep: line.split(sep))
        self.log_id = self.logger.get_section(SmallLogger.LOGID)
        if check_username and self.log_id != username:
            raise UsernameMatchError('username:%s file_log_id:%s' % (username,
                                                                     self.log_id))

    def flush_read(self):
        self.logger.read_log(self.path,
                             format_func=lambda section_name, line, sep: line.split(sep))

    def add_account(self, label, username, password):
        content = self.logger.get_section(label, [])
        encrypt_password = des.encryp_str(password, self.master_password)  # encrypy with des
        content.append([username, encrypt_password])
        # print(content)
        self.logger[label] = content
        # print(self.logger.get_section(label, []))

    def del_account(self, label, username_todel):
        content = self.logger.get_section(label, [])
        self.logger[label] = filter(lambda x: x[0] != username_todel, content)

    def del_label(self, label):
        if label in self.logger:
            self.logger[label] = None

    def update_account(self, label, username, new_password):
        if label not in self.logger: raise UsernameMatchError

        # delete and then insert
        content = list(filter(lambda x: x[0] != username,
                              self.logger.get_section(label, [])))

        encrypt_password = des.encryp_str(new_password, self.master_password)  # encrypy with des
        content.append([username, encrypt_password])
        self.logger[label] = content

    def update_label(self, label, new_label):
        content = self.logger[label]
        self.logger[label] = None
        self.logger[new_label] = content

    def write_back(self, log_id=None):
        if log_id is None:
            log_id = self.log_id
        self.logger.write_log(self.path, log_id=log_id,
                              format_func=lambda section_name, elem, sep: elem[0] + sep + elem[1])

    def query_account(self, label):
        if label not in self.logger or self.logger[label] is None:
            return None

        content = list(self.logger[label])
        return [(username, des.decryp_str(encrypt_password, self.master_password))
                for username, encrypt_password in content]

    def get_labels(self):
        """get all labels except _XXX labels and label value is None"""
        return list(filter(lambda label: not label.startswith('_') and \
                                         self.logger[label] is not None,
                           self.logger.get_section_dict().keys()))

    def __del__(self):
        self.write_back()  # WARNING: ERROR LOG WOULD BE WROUTE BACK TOO!!


def desensitization_pwd(pwd):
    length_pwd = len(pwd)

    if length_pwd == 0:
        pwd = ''
    elif length_pwd == 1:
        pwd = '*'
    elif length_pwd == 2:
        pwd = pwd[0] + '*'
    elif length_pwd == 3:
        pwd = pwd[0] + '*' + pwd[-1]
    elif length_pwd == 4:
        pwd = pwd[:2] + '*' + pwd[-1]
    else:
        pwd = pwd[:2] + '*' * (length_pwd-4) + pwd[-2:]
    
    return pwd
    

def main(path, pwd, check_username=False, username=None):
    if pwd is None:
        pwd = getpass.getpass('Input your master password: ')

    pwd_keeper = PwdKeeper(path, pwd, check_username, username)
    color.print_info(pwd_keeper.log_id)
    if username is None:
        username = pwd_keeper.log_id
    base_prompt = '<%s>' % username
    interactive_help = split_blankline(__doc__)[0]
    while True:
        input_result = input(base_prompt).strip()  # STRIP !!
        if 'q' in input_result:
            return

        try:
            if input_result.startswith('query'):
                label = split_whitespace(input_result)[1]
                all_match = pwd_keeper.query_account(label)
                if all_match is None:
                    print('None')
                    possiable_labels = []
                    for each_label in pwd_keeper.get_labels():
                        each_label2 = each_label.lower()
                        label2 = label.lower()
                        if each_label2.startswith(label2) or \
                                each_label2.endswith(label2):
                            possiable_labels.append(each_label)

                    if len(possiable_labels) != 0:
                        print('Maybe: ', end='')
                        for each_label in possiable_labels:
                            color.print_info(each_label, end='')
                        color.print_info()

                else:
                    for item in all_match:
                        try:
                            color.print_info('usrename:{0} passowrd:{1}'.format(*item))
                        except UnicodeEncodeError:
                            username, password = item[0], \
                                                 item[1]
                            color.print_err('usrename:{0} passowrd:{1}'.
                                            format(username, password))

                            color.print_err('Warning: Master Password {0} may be Error'.format(
                                desensitization_pwd(pwd))
                            )

            elif input_result.startswith('add'):
                _, label, username, password = split_whitespace(input_result)
                pwd_keeper.add_account(label, username, password)

            elif input_result.startswith('del-account'):
                _, label, username = split_whitespace(input_result)
                pwd_keeper.del_account(label, username)

            elif input_result.startswith('del-label'):
                _, label = split_whitespace(input_result)
                pwd_keeper.del_label(label)

            elif input_result.startswith('update-account'):
                _, label, username, password = split_whitespace(input_result)
                pwd_keeper.update_account(label, username, password)

            elif input_result.startswith('update-label'):
                _, old_label, new_label = split_whitespace(input_result)
                pwd_keeper.update_label(old_label, new_label)

            elif input_result.startswith('list') or input_result == 'ls' or input_result == 'l':
                [color.print_info(label) for label in pwd_keeper.get_labels() if pwd_keeper]

            elif input_result.startswith('?'):
                color.print_info(interactive_help)
            elif input_result == '':
                pass
            else:  # '?'
                color.print_err('\nInvalid Input')
                print(input_result)
                color.print_info(interactive_help)

        except ValueError:
            color.print_err('\nInvalid Input:')
            print(input_result)
            color.print_info(interactive_help)
            print()


def cli():
    arguments = docopt(__doc__, version=minghu6.__version__)
    path = arguments['<path>']
    master_pwd = arguments['--password']

    if arguments['--username'] is not None:
        main(path, master_pwd, check_username=True, username=arguments['--username'])
    else:
        main(path, master_pwd)


if __name__ == '__main__':
    cli()
