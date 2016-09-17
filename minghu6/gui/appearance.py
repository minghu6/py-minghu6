#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
################################################################################
Tk appearance module
################################################################################
"""
import tkinter as tk

def showonCenter(app,resize=(False,False)):

    app.resizable(resize[0],resize[1]) #(width,height)

    app.update() # update window ,must do
    curWidth = app.winfo_width() # get current width
    curHeight = app.winfo_height() # get current height
    scnWidth,scnHeight = app.maxsize() # get screen width and height
    # now generate configuration information
    tmpcnf = '%dx%d+%d+%d'%(curWidth,curHeight,
    (scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
    app.geometry(tmpcnf)
    app.mainloop()

if __name__ == '__main__':

    root=tk.Tk()
    showonCenter(root)