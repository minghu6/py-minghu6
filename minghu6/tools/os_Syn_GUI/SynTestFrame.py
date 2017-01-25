
#for python3.4
import sys, os, time
from PyQt4 import QtGui, QtCore
import threading, _thread, queue
from multiprocessing import Process, Queue, \
SimpleQueue, Value, sharedctypes, Lock, Event
import ctypes

import random
import os_2

'''
Synchronization Main Window
'''
class MainWindow_Syn(QtGui.QMainWindow):
    
    default_process_number = 15
    #if sub thread find that flag==1,then it exit
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.main = os_2.Ui_MainWindow()
        self.main.setupUi(self)
        self.setWindowTitle('Syncronization')

        
        #set data segment
        self.sell_ticket_data_queue = Queue()
        self.bus_data_queue = Queue()
            #set shared memory
        self.ticket_number_casual = sharedctypes.RawValue(ctypes.c_int, 50)
        self.ticket_number_restrict = sharedctypes.RawValue(ctypes.c_int, 50)

        #set process list
        self.processes1 = []
        self.processes2 = []

        #set syncronization
        self.sell_ticket_lock = Lock()
        #self.sell_ticket_event=Event()
        self.closedoor_e = Event()
        self.park_e = Event()
        self.open_once_e = Event()
        self.setshow_msg()
        #set Button etc
        self.setsell_ticket_casualButton()
        self.setsell_ticket_restrictButton()
        self.setend_sell_ticketButton()
        self.setspinBox()

        self.setgo_busButton()
        self.setend_busButton()
        
    def setshow_msg(self):
        '''
        open a thread for each GUI module
        aim to receive the data from syncronization queue,and append it to the GUI
        '''
        def sell_ticket_show_msg():
            while True:
                time.sleep(0.1)
                try:
                    sell_ticket_data = self.sell_ticket_data_queue.get(block=True)
                    pass
                except queue.Empty:
                    pass
                else:
                    self.main.sell_ticketTextBrowser.append(sell_ticket_data)
                    pass
        def bus_show_msg():
            while True:
                try:
                    bus_data = self.bus_data_queue.get(block=True)

                except queue.Empty:
                    pass
                else:
                    self.main.busTextBrowser.append(bus_data)


        threading.Thread(target=sell_ticket_show_msg).start()
        threading.Thread(target=bus_show_msg).start()
    
    def setspinBox(self):
        self.main.spinBox.setRange(0, 102)


    def setsell_ticket_casualButton(self):
        '''
        WITHOUT syncronized protect to tickets
        '''
        def sell_ticket_casual():
            
            def sell_ticket_casual_process(id, sell_ticket_data_queue, ticket_number_casual):
                while True:
                    time.sleep(0.5)
                    if(ticket_number_casual.value <= 0):
                        #sell_ticket_data_queue
                        break
                    else:
                        ticket_number_casual.value -= 1;
                        msg = 'process {0:d}: there (are/is) {1:d} tickets available-casual\
                           '.format(id, ticket_number_casual.value)
                        #print(msg)
                        sell_ticket_data_queue.put(msg)
                       
            #initial work for restart the button again
            self.main.sell_ticketTextBrowser.clear()
                #get the suitable number of processes to sell tickets
            pnumber = self.main.spinBox.value()
            if pnumber < 2:
                pnumber = self.default_process_number
                msg = 'least process number is 2,start with default number'
                self.sell_ticket_data_queue.put(msg)
            
            #[queue.get() for queue in self.sell_ticket_data_queue]
            self.ticket_number_casual.value = 50
            msg = 'initial tickets number is {0:d}\nseller number is {1:d}\nNow,selling start...\n'.format(self.ticket_number_casual.value, pnumber)
            self.sell_ticket_data_queue.put(msg)
            self.processes1 = []
            for i in range(pnumber):
                self.processes1.append(Process(target=sell_ticket_casual_process, args=(i, self.sell_ticket_data_queue, self.ticket_number_casual), daemon=True))
                self.processes1[-1].start()

        QtCore.QObject.connect(self.main.sell_ticket_casualButton, QtCore.SIGNAL("clicked()"), sell_ticket_casual)


    def setsell_ticket_restrictButton(self):
        '''
        WITH syncronized protect to tickets
        '''
        def sell_ticket_restrict():

            def sell_ticket_restrict_process(id, sell_ticket_data_queue,
                                                 ticket_number_restrict, sell_ticket_lock):
                while True:
                        time.sleep(0.5)
                        with sell_ticket_lock:
                            if(ticket_number_restrict.value <= 0):
                                break
                            else:
                                ticket_number_restrict.value -= 1
                                msg = 'process {0:d}: there (are/is) {1:d} tickets available-restrict'.format(id, ticket_number_restrict.value)
                                sell_ticket_data_queue.put(msg)

            #initial work for restart the button again
            self.main.sell_ticketTextBrowser.clear()
            #get the suitable number of processes to sell tickets
            pnumber = self.main.spinBox.value()
            if pnumber < 2:
                pnumber = self.default_process_number
                msg = 'least process number is 2,start with default number'
                self.sell_ticket_data_queue.put(msg)

            self.ticket_number_restrict.value = 50
            msg = 'initial tickets number is {0:d}\nseller number is {1:d}\nNow,selling start...\n'.format(self.ticket_number_restrict.value, pnumber)

            self.sell_ticket_data_queue.put(msg)
            self.processes2 = []
            for i in range(pnumber):

                self.processes2.append(Process(target=sell_ticket_restrict_process, args=(i, self.sell_ticket_data_queue, self.ticket_number_restrict, self.sell_ticket_lock), daemon=True))
                self.processes2[-1].start()

        QtCore.QObject.connect(self.main.sell_ticket_restrictButton, QtCore.SIGNAL("clicked()"), sell_ticket_restrict)

    def setend_sell_ticketButton(self):
        '''
		terminate processes in a dangerous(but convenient)way
		'''
        def exit_sell_ticket():
            [process.terminate() for process in self.processes1]
            [process.terminate() for process in self.processes2]
        QtCore.QObject.connect(self.main.end_sell_ticketButton, QtCore.SIGNAL("clicked()"), exit_sell_ticket)

    def setgo_busButton(self):
        '''
		start driver and conductor work
		'''
        def go_bus():
            '''drive with the door closed.
            open the door when parking.
            open no more than once each parking.
            '''
            class driver(Process):
                def __init__(self, bus_data_queue, closedoorevent, parkevent, open_once_e):
                    Process.__init__(self)
                    self.closedoor_e = closedoorevent
                    self.park_e = parkevent
                    self.open_once_e = open_once_e
                    self.bus_data_queue = bus_data_queue
                def run(self):
                    while True:
                        self.closedoor_e.wait()
                        self.park_e.clear()
                        self.drive()
                        self.park_e.set()
                        self.park()
                        self.closedoor_e.clear()
                        self.open_once_e.set()

                    def drive(sef):
                        msg = 'Drive...'
                        self.bus_data_queue.put(msg)
                        timeit = random.random() * 3
                        time.sleep(timeit)
                    def park(self):
                        msg = 'park...'
                        self.bus_data_queue.put(msg)
                        timeit = random.random() * 2 + 1
                        time.sleep(timeit)
            class conductor(Process):
                def __init__(self, bus_data_queue, cld_e, park_e, open_once_e):
                    Process.__init__(self)
                    self.park_e = park_e
                    self.closedoor_e = cld_e
                    self.open_once_e = open_once_e

                    self.bus_data_queue = bus_data_queue
                def run(self):
                    once = 0
                    while True:
                        self.park_e.wait()
                        self.open_once_e.wait()
                        self.open_once_e.clear()
                        self.opendoor()
                        self.closedoor_e.set()
                        self.closedoor()
                        self.selltickets()

                def opendoor(self):
                    msg = 'open the door'
                    self.bus_data_queue.put(msg)
                    timeit = random.random()
                    time.sleep(timeit)
                def closedoor(self):
                    msg = 'close the door'
                    self.bus_data_queue.put(msg)
                    timeit = random.random()
                    time.sleep(timeit)
                def selltickets(self):
                    msg = 'selling tickets...'
                    self.bus_data_queue.put(msg)
                    timeit = random.random()
                    time.sleep(timeit)

                    self.closedoor_e = Event()
                    self.park_e = Event()
                    self.open_once_e = Event()

                    self.closedoor_e.set()
                    self.park_e.clear()
                    self.open_once_e.set()
                    self.driver1 = driver(self.bus_data_queue, self.closedoor_e, self.park_e, self.open_once_e)
                    self.driver1.start()
                    self.conductor1 = conductor(self.bus_data_queue, self.closedoor_e, self.park_e, self.open_once_e)
                    self.conductor1.start()

        QtCore.QObject.connect(self.main.go_busButton, QtCore.SIGNAL("clicked()"), go_bus)

    def setend_busButton(self):
        def end_bus():
            self.driver1.terminate()
            self.conductor1.terminate()
        QtCore.QObject.connect(self.main.end_busButton, QtCore.SIGNAL("clicked()"), end_bus)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow_Syn()
    main.show()
    sys.exit(app.exec())
        
