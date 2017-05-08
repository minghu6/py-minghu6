# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""PwdKeeper
a small password keeper, query or add username-password by interactive
list           #list all label
query          <label>
add            <label> <username> <password>
del-account    <label> <username-todel>
del-label      <old-label> <new-label>
update-account <label> <username> <new-password>
update-label   <old-label> <new-label>
q!             #quit

Usage:
  pwd_keeper <path> <master-pwd> [--username=<username>]

Options:
  <path>                    account file path to connect
  -u --username=<username>  your account name for pwd_keeper, using fo check account file

"""

import os

from docopt import docopt

import minghu6
from minghu6.etc.logger import SmallLogger
from minghu6.security.des import des
from minghu6.text.color import color
from minghu6.text.seq_enh import split_whitespace, split_blankline

class UsernameMatchError(BaseException):pass
class PwdKeeper:

    def __init__(self, path, master_password, check_username=False, username=None):


        self.path = path
        self.master_password = des.valid_key(master_password)
        self.logger = SmallLogger()
        if not os.path.exists(path):
            self.write_back(username)
        self.logger.read_log(path,
                             format_func=lambda section_name,line,sep:line.split(sep))
        self.log_id = self.logger.get_section(SmallLogger.LOGID)
        if check_username and self.log_id != username:
            raise UsernameMatchError('username:%s file_log_id:%s'%(username,
                                                                   self.log_id))

    def flush_read(self):
        self.logger.read_log(self.path,
                             format_func=lambda section_name,line,sep:line.split(sep))

    def add_account(self, label, username, password):
        content = list(getattr(self.logger, label, []))
        encrypt_password = des.encryp_str(password, self.master_password) #encrypy with des
        content.append([username, encrypt_password])
        self.logger[label] = content

    def del_account(self, label, username_todel):
        content = list(getattr(self.logger, label, []))
        self.logger[label] = filter(lambda x:x[0] != username_todel, content)

    def del_label(self, label):
        if label in self.logger:
            self.logger[label] = None

    def update_account(self, label, username, new_password):
        if label not in self.logger:raise UsernameMatchError

        # delete and then insert
        content = list(filter(lambda x:x[0] != username, getattr(self.logger, label)))
        encrypt_password = des.encryp_str(new_password, self.master_password) #encrypy with des
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
                              format_func=lambda section_name, elem, sep:elem[0]+sep+elem[1])

    def query_account(self, label):
        if label not in self.logger:
            return None

        content = list(self.logger[label])
        return [(username, des.decryp_str(encrypt_password, self.master_password))
                for username, encrypt_password in content]

    def get_labels(self):
        '''get all labels except _XXX labels'''
        return list(filter(lambda label: not label.startswith('_'),
                           self.logger.get_section_dict().keys()))

    def __del__(self):
        self.write_back() #WARNING: ERROR LOG WOULD BE WROUTE BACK TOO!!


def main(path, pwd, check_username=False, username=None):
    pwd_keeper = PwdKeeper(path, pwd, check_username, username)
    color.print_info(pwd_keeper.log_id)
    if username is None:
        username = pwd_keeper.log_id
    base_prompt = '<%s>'%username
    interactive_help = split_blankline(__doc__)[0]
    while True:
        input_result = input(base_prompt).strip() # STRIP !!
        if 'q!' in input_result:return

        try:
            if input_result.startswith('query'):
                label = split_whitespace(input_result)[1]
                all_match = pwd_keeper.query_account(label)
                if all_match is None:
                    print('None')
                else:
                    for item in all_match:
                        try:
                            color.print_info('usrename:{0} passowrd:{1}'.format(*item))
                        except UnicodeEncodeError:
                            username, password = item[0], \
                                                 item[1]
                            color.print_err('usrename:{0} passowrd:{1}'.
                                            format(username, password))

                            color.print_err('Warning: Master Password {0} may be Error'.format(pwd))

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

            elif input_result.startswith('list'):
                [color.print_info(label) for label in pwd_keeper.get_labels()]

            elif input_result.startswith('?'):
                color.print_info(interactive_help)
            elif input_result == '':
                pass
            else: #'?'
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
    master_pwd = arguments['<master-pwd>']

    if arguments['--username'] is not None:
        main(path, master_pwd, check_username=True, username=arguments['--username'])
    else:
        main(path, master_pwd)


if __name__ == '__main__':
    cli()
