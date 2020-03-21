# -*- Coding:utf-8 -*-
"""

"""
import os
from collections import OrderedDict

from color import print_normal, print_error, print_warning, print_italic
from minghu6.algs.func import flatten
from minghu6.io.stdio import askyesno
from shell_op import Op

flat_dir = r'F:\ACGNFM\File\新建'


def list_dirs_of_dir(dst):
    return list(filter(os.path.isdir, map(lambda fn: os.path.join(dst, fn), os.listdir(dst))))


def list_not_dir_fn_of_dir(dst):
    return list(filter(lambda fn: not os.path.isdir(os.path.join(dst, fn)), os.listdir(dst)))


class FlattenDir:
    def __init__(self, dst):
        self.dst = dst
        self.regular_files = None
        self.fn_path_map = None
        self.top_dir_not_dir_fns = list_not_dir_fn_of_dir(self.dst)
    
    def _find_regular_files(self):
        self.fn_path_map = OrderedDict()
        
        for (thisDir, subsHere, filesHere) in os.walk(self.dst):
            if thisDir == self.dst:
                continue
            for fn in filesHere:
                fullname = os.path.join(thisDir, fn)
                
                if fn not in self.fn_path_map:
                    self.fn_path_map[fn] = []
                
                self.fn_path_map[fn].append(fullname)
                
                yield fullname
    
    def print_regular_files(self):
        for filepath in flatten(self._find_regular_files()):
            print_normal(filepath)
        
        given_warning = False
        for fn, fullpath_list in self.fn_path_map.items():
            if len(fullpath_list) > 1 or fn in self.top_dir_not_dir_fns:
                if not given_warning:
                    given_warning = True
                    print_warning('There are same name file conflicts:')
                
                print_italic(fn, ':')
                for filepath in fullpath_list:
                    print_warning(filepath)
                if fn in self.top_dir_not_dir_fns:
                    print_warning(os.path.join(os.path.curdir, fn))
    
    def do_flatten_dir(self):
        for filepath in flatten(self._find_regular_files()):
            dirname, filename = os.path.split(filepath)
            print_normal('extract {0} from {1}'.format(filename, dirname))
        
        given_error = False
        for fn, fullpath_iter in self.fn_path_map.items():
            if len(fullpath_iter) > 1 :
                if not given_error:
                    given_error = True
                    print_error('There are same name file conflicts:')
                
                print_italic(fn, ':')
                for filepath in fullpath_iter:
                    print_error(filepath)
                if fn in self.top_dir_not_dir_fns:
                    print_error(os.path.join(self.dst, fn))

        if given_error:
            return
        
        for empty_dir in list_dirs_of_dir(self.dst):
            print_normal('remove directory %s' % empty_dir)
        
        if not askyesno('continue?'):
            return
        
        with Op('flattendir', self.dst) as op:
            for fn, fullpath_iter in self.fn_path_map.items():
                fullpath = fullpath_iter[0]
                op.mv(fullpath, '.')

    def rm_empty_dirs(self):
        [op.rm(each_dir, recursive=True) for each_dir in list_dirs_of_dir(self.dst)]

    def undo(self):
        with Op('flattendir', self.dst) as op:
            op.undo()


# print(list_dirs_of_dir(flat_dir))
# print(list(find_regular_file(flat_dir)))
# print(FlattenDir(flat_dir).print_regular_files())


# flatten_dir = FlattenDir(flat_dir)
# flatten_dir.do_flatten_dir()
# flatten_dir.rm_empty_dirs()
