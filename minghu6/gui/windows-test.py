#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
################################################################################
test windows.py
################################################################################
"""
from tkinter import Button,mainloop
from windows import MainWindow,PopupWindow,ComponentWindow

def _selftest():

    #mixin usage
    class content:
        "same code used as Tk,Toplevel, andc Frame"
        def __init__(self):
            Button(self,text='Larch',command=self.quit).pack()
            Button(self,text='Sing',command=self.destroy).pack()

    class contentmix(MainWindow,content):
        def __init__(self):
            MainWindow.__init__(self,'mixin','Main')
            content.__init__(self)

    contentmix()

    class contentmix(PopupWindow,content):
        def __init__(self):
            PopupWindow.__init__(self,'mixin','Popup')
            content.__init__(self)
    prev=contentmix()

    class contentmix(ComponentWindow,content):
        def __init__(self):
            ComponentWindow.__init__(self,prev)
            content.__init__(self)
    contentmix()

    #subclass usage
    class contentsub(PopupWindow):
        def __init__(self):
            PopupWindow.__init__(self,'popup','subclass')
            Button(self,text='Pine',command=self.quit).pack()
            Button(self,text='Sing',command=self.destroy).pack()

    contentsub()

    #non-class usage
    win=PopupWindow('popup','attachment')
    Button(win,text='Redwood',command=win.quit).pack()
    Button(win,text='Sing   ',command=win.destroy).pack()
    mainloop()


if __name__=='__main__':
    _selftest()































