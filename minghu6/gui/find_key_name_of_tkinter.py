#! /usr/bin/env python3
# -*- coding:utf-8 -*-

#from tkinter import *
import tkinter as tk

class App_getkeyname:
    def __init__(self, root):
        self.root = root
        self.root.bind('<KeyPress>', self.bind_key)
        self.root.bind('<KeyPress-Shift_R>',self.bind_x_key)

    def bind_key(self,event):

        print(event.keysym)

    def bind_x_key(self,event):

        print('**********')

if __name__=='__main__':
    '''
    main loop
    '''
    root=tk.Tk()
    root.title('Key')
    App_getkeyname(root)
    root.mainloop()