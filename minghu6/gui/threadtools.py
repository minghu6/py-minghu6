#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
################################################################################
System-wide thread interface utilities for GUIs.

Implements a single thread callback queue and checker timer loop
shared by all the windows in a program ;worker threads queue
they exit and progress actions to be run in the main thread;
this doesn't block the the GUI - it just spawns operations
and manages and dispatches exits and progress;
worker threads can overlap freely with the main thread,
and with other workers,

Using a queue of callback functions and
arguments is more useful than a simple data queue
if there can be many kinds of threads
running at the same time - each kind may have different implied exit actions.

Because GUI API is not completely thread-safe,instead of calling GUI update
callback directly after thread main action,place them on a shared queue,
to be run from a timer loop in the main actions,and unpredictable;
requires threads to be split into main action,exit actions,and progress action.

Assumes threaded action raises an exception on failure,and has a 'progress'
callback argument if it it supports progress updates;
also assumes callbacks are either short-lived or update as they run,
and that queue will contain callback functions (or other callables)
for use in a GUI app - requires a widget
in order to schedule and catch 'after' event loop callbacks;
 to use this model in non-GUI contexts,could use simple thread timer instead.

"""

#run if no threads

try:
    import _thread as thread
except:
    import _dummy_thread as thread

#shared cross-process queue
#name in shared global scope,lives in shared object memory
import queue
import sys

threadQueue=queue.Queue(maxsize=0) #infinite size

################################################################################
#
################################################################################

def threadChecker(widget,delayMsecs=100,perEvent=1): #10x/sec,1/timer
    for i in range(perEvent):
        try:
            (callback,args)=threadQueue.get(block=False)
        except queue.Empty:
            break
        else:
            callback(*args)

    widget.after(delayMsecs,
                 lambda: threadChecker(widget,delayMsecs,perEvent))


def threaded(action,args,context,onExit,onFail,onProgress):
    try:
        if not onProgress: #wait for action in this thread
            action(*args)
        else:
            def progress(*any):
                threadQueue.put((onProgress,any+context))
            action(progress=progress,*args)

    except:
        threadQueue.put((onFail,(sys.exc_info(),)+context))
    else:
        threadQueue.put((onExit,context))

def startThread(action,args,context,onExit,onFail,onProgress=None):
    thread.start_new_thread(threaded,
                            (action,args,context,onExit,onFail,onProgress))


class ThreadCounter:
    def __init__(self):
        self.count=0
        self.mutex=thread.allocate_lock() # use Threading.semaphore

    def inc(self):
        with self.mutex:
            self.count +=1

    def dec(self):
        with self.mutex:
            self.count-=1

    def __len__(self):
        return self.count

if __name__=='__main__':
    import time
    from tkinter.scrolledtext import ScrolledText


    def onEvent(i):
        myname='thread-%s'%i
        startThread(
            action=threadaction,
            args=(i,3),
            context=(myname,),
            onExit=threadexit,
            onFail=threadfail,
            onProgress=threadprogress
        )

    #thread's main action
    def threadaction(id,reps,progress):
        for i in range(reps):
            time.sleep(1)
            if progress:
                progress(i)

        if id%2==1:
            raise Exception

    def threadexit(myname):
        text.insert('end','%s\texit\n'%myname)
        text.see('end')

    def threadfail(exc_info,myname):
        text.insert('end','%s\tfail\t%s\n'%(myname,exc_info[0]))

    def threadprogress(count,myname):
        text.insert('end','%s\tprog\t%s\n'%(myname,count))
        text.see('end')
        text.update()

    text=ScrolledText()
    text.pack()
    threadChecker(text)
    text.bind('<Button-1>',
              lambda event:list((map(onEvent,range(6)))))

    text.mainloop()



























