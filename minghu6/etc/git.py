# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""
Git cmd functions
"""
import os

from .cmd import chdir, exec_cmd


def is_valid_git_repo(repo_path):
    repo_path = os.path.abspath(repo_path)
    cmd_list = ['git', 'status']
    with chdir(repo_path):
        info, err = exec_cmd(cmd_list)
        if info[0] != '' and err[0] == '':
            return True
        else:
            return False


def git_init(repo_name, repo_dir=os.curdir, bare=False, force=False):
    """
    
    :param repo_name: 
    :param repo_dir: 
    :param bare: init a bare repo
    :param force: re-init repo if it exists 
    :return: 
    """
    repo_dir = os.path.abspath(repo_dir)
    if not os.path.isdir(repo_dir):
        return False

    repo_path = os.path.join(repo_dir, repo_name)
    if os.path.exists(repo_path) and not os.path.isdir(repo_path):
        return False
    elif not os.path.exists(repo_path):
        os.mkdir(repo_path)  # raise exception, if the repo_path exists and isn't dir.

    if is_valid_git_repo(repo_path) and not force:
        return False

    cmd_list = ['git', 'init']
    if bare:
        cmd_list.append('--bare')

    with chdir(repo_path):

        info, err = exec_cmd(cmd_list)
        # print(info, err) #['Initialized ...'] ['']

    return True


def git_head(repo_path):
    """Get (branch, commit) from HEAD of a git repo."""
    repo_path = os.path.abspath(repo_path)
    try:
        ref = open(os.path.join(repo_path, '.git', 'HEAD'), 'r').read().strip()[5:].split('/')
        branch = ref[-1]
        commit = open(os.path.join(repo_path, '.git', *ref), 'r').read().strip()[:7]
        return branch, commit
    except:
        return None


def git_add(repo_path, pattern_set):
    repo_path = os.path.abspath(repo_path)
    cmd_list = ['git', 'add']
    cmd_list.extend(pattern_set)
    with chdir(repo_path):
        exec_cmd(cmd_list)


def git_commit(repo_path, m, a=True):
    cmd_list = ['git', 'commit']
    if a:
        cmd_list.append('-a')
    if m is None:
        m = ''

    cmd_list.extend(['-m', m])
    with chdir(repo_path):
        exec_cmd(cmd_list)
