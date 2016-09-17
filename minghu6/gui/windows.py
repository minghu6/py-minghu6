#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
################################################################################
Classes that encapsulate top-level interfaces.
Allows same GUI to be main,pop-up,or attached;
content classes may inherit from these directly without a subclass;
designed to be mixed in after app-specific classes:
else,subclass gets methods here,
instead of from app-specific classes -- can't redefine
################################################################################
"""

import os,glob
from tkinter import Tk,Toplevel,Frame,YES,BOTH,RIDGE
from tkinter.messagebox import  showinfo,askyesno

class _window:
    '''
    mixing shared by main and pop-up windows
    '''
    found_icon=None #shared by all instance
    icon_pattern='*.ico' # may be reset
    icon_mine='py.ico'

    def configBorders(self,app,kind,icon_file):
        if not icon_file:
            icon_file=self.findIcon() #try curr,tool dirs

        title=app
        if kind:
            title+=' - '+kind

        self.title(title) #on window border when minimized
        self.iconname(app)
        if icon_file:
            try:
                self.icon_bitmap(icon_file) #window icon image
            except: #because of bad py file or platform
                pass

        self.protocol('WM_DELETE_WINDOW',self.quit) #don't close silent

    def findIcon(self):

        #if already find one
        if _window.found_icon:
            return _window.found_icon
        icon_file=None

        #try cur dir first
        icons_here=glob.glob(self.icon_pattern)

        if icons_here:
            icon_file=icons_here[0]
        else:
            mymod=__import__(__name__)
            path=__name__.split('.')
            for mod in path[1:]:
                mymod=getattr(mymod,mod)
            mydir=os.path.dirname(mymod.__file__)
            myicon=os.path.join(mydir,self.icon_mine)
            if os.path.exists(myicon):
                icon_file=myicon
        _window.found_icon=icon_file
        return icon_file

class MainWindow(Tk,_window):
    '''
    when run in main top-level window
    '''

    def __init__(self,app,kind='',icon_file=None, center=True):
        self.findIcon()
        Tk.__init__(self)
        if center:
            from minghu6.gui.appearance import showonCenter
            pass
        self.__app=app
        self.configBorders(app,kind,icon_file)

    def quit(self):
        if self.okayToQuit():
            try:
                if askyesno(self.__app,'Verify Quit Program?'):

                    self.destroy()
            except RuntimeError:
                import os
                os._exit(0)

        else:
            showinfo(self.__app,'Quit not allowed')

    def destroy(self):
        Tk.quit(self)

    def okayToQuit(self):
        return True

class PopupWindow(Toplevel,_window):
    '''
    when run in secondary pop-up window
    '''

    def __init__(self,app,kind='',icon_file=None, center=True):
        Toplevel.__init__(self)
        self.__app=app
        self.configBorders(app,kind,icon_file)

        if center:
            from minghu6.gui.appearance import showonCenter
            pass


    def quit(self):
        if askyesno(self.__app,'Verify Quit Windows?'):
            self.destroy()

    def destroy(self):
        Toplevel.destroy(self)

class QuietPopupWindow(PopupWindow):
    def quit(self):
        self.destroy()

class ComponentWindow(Frame):
    '''
    when attached to another display
    '''

    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.pack(expand=YES,fill=BOTH)
        self.config(relief=RIDGE,border=2)

    def quit(self):
        showinfo('Quit','Not supported in attachment mode')











if __name__ == '__main__':
    #PopupWindow(Tk())
    MainWindow(Tk())


















