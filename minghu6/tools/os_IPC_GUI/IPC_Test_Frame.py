# for python3
import os
import sys
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM

import queue
from PyQt4 import QtGui, QtCore

"""
This is a OS Test Frame 
"""


def nop():
    pass


'''
IPC Main Window
'''


class MainWindow_IPC(QtGui.QMainWindow):
    file_p2c = 'p2c'
    file_c2p = 'c2p'
    sock_port = 6666
    host = 'localhost'

    def __init__(self):
        import os_1
        QtGui.QMainWindow.__init__(self)
        self.main = os_1.Ui_MainWindow()
        self.main.setupUi(self)
        self.setLCDNumber()
        self.local_data_queue = queue.Queue()
        self.remote_data_queue = queue.Queue()
        self.setshow_msg()

        self.setForkButton()
        self.setSocketButton()
        if sys.platform[:3] == 'win':
            pass
        else:
            self.setPipButton()
            self.setFIFOPipButton()
        # self.resize(860, 500)
        if len(sys.argv) == 1:
            self.setWindowTitle('Father Process')
        else:
            self.setWindowTitle('Child Process')

        self.statusBar().showMessage('Ready')

    def setshow_msg(self):
        def show_msg():
            while True:
                time.sleep(0.1)
                try:
                    data = self.local_data_queue.get(block=True)
                except queue.Empty:
                    pass
                else:
                    self.main.outputText.append(data)

        thread_recv = threading.Thread(target=show_msg)
        thread_recv.start()

    def setSocketButton(self):
        def SocketSend():
            msg = self.main.textEdit.toPlainText()
            self.main.textEdit.clear()
            self.local_data_queue.put('socket<-you said:' + msg)
            self.remote_data_queue.put(msg)
            self.num += 1
            self.main.P_Number.display(self.num)
            if len(sys.argv) == 1:
                pass
            else:
                def client_send():
                    # self.sock.connect((self.host,self.sock_port))
                    self.sock.send(msg.encode())
                    # self.sock.close()

                thread_send = threading.Thread(target=client_send)
                thread_send.start()

        if len(sys.argv) == 1:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.bind(('', self.sock_port))
            self.sock.listen(5)

            def server_recv():
                conn, addr = self.sock.accept()

                def server_send():
                    while True:
                        time.sleep(0.1)
                        try:
                            data = self.remote_data_queue.get(block=False)
                        except queue.Empty:
                            pass
                        else:
                            conn.send(data.encode())

                thread_send = threading.Thread(target=server_send)
                thread_send.start()
                while True:
                    msg = conn.recv(1024).decode()
                    # conn.close()
                    self.local_data_queue.put('socket->child said:' + msg)

            thread_recv = threading.Thread(target=server_recv)
            thread_recv.start()

        else:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((self.host, self.sock_port))

            def client_recv():
                while True:
                    msg = self.sock.recv(1024).decode()
                    # conn.close()
                    self.local_data_queue.put('socket->father said:' + msg)

            thread_recv = threading.Thread(target=client_recv)
            thread_recv.start()

        QtCore.QObject.connect(self.main.SocketSendButton, QtCore.SIGNAL("clicked()"), SocketSend)

    def setFIFOPipButton(self):
        def FIFOPipSend():
            msg = self.main.textEdit.toPlainText()
            self.main.textEdit.clear()
            self.local_data_queue.put('fifopipe<-you said:' + msg)
            self.pipeout.write(msg + '\n')
            self.pipeout.flush()
            self.num += 1
            self.main.P_Number.display(self.num)

        if len(sys.argv) == 1:
            if not os.path.exists(self.file_p2c):
                os.mkfifo(self.file_p2c)
            if not os.path.exists(self.file_c2p):
                os.mkfifo(self.file_c2p)

            def parent():
                self.pipein = open(self.file_c2p, 'r')
                self.pipeout = open(self.file_p2c, 'w')
                while True:
                    msg = self.pipein.readline()[:-1]
                    self.local_data_queue.put('fifopipe->child said' + msg)

            thread_parent = threading.Thread(target=parent)
            thread_parent.start()

        else:
            def child():
                self.pipeout = open(self.file_c2p, 'w')
                self.pipein = open(self.file_p2c, 'r')
                while True:
                    msg = self.pipein.readline()[:-1]
                    self.local_data_queue.put('fifopipe->father said' + msg)

            thread_child = threading.Thread(target=child)
            thread_child.start()

        QtCore.QObject.connect(self.main.FIFOPipeSendButton, QtCore.SIGNAL("clicked()"), FIFOPipSend)

    def setPipButton(self):
        def PipSend():
            msg = self.main.textEdit.toPlainText()
            self.main.textEdit.clear()
            if len(sys.argv) == 1:  # in parent process
                os.write(self.parent_pipe_write, (msg + '\n').encode())

                self.local_data_queue.put('pipe<-you said' + msg)
            else:  # in child process
                msg = self.child_pipe_read_fd()

            self.num += 1
            self.main.P_Number.display(self.num)

        if len(sys.argv) == 1:  # in parent process
            self.child_pipe_read, self.parent_pipe_write = os.pipe()
            self.parent_pipe_read, self.child_pipe_write = os.pipe()
            # self.parent_pipe_read_fd=os.fdopen(self.parent_pipe_read)
            os.set_inheritable(self.child_pipe_read, True)
            os.set_inheritable(self.child_pipe_write, True)
            os.set_inheritable(self.parent_pipe_read, True)
            os.set_inheritable(self.parent_pipe_write, True)

            os.close(self.child_pipe_read)
            os.close(self.child_pipe_write)
        else:  # in child process
            def child_read():
                self.child_pipe_read = int(sys.argv[2])
                self.child_pipe_write = int(sys.argv[3])
                # self.child_pipe_read_fd=os.fdopen(self.child_pipe_read)
                while True:
                    print('OK?')
                    msg = os.read(self.child_pipe_read, 32)
                    # msg=self.child_pipe_read_fd.readline()[:-1]
                    self.local_data_queue.put('pipe->father said' + msg)

            thread_child = threading.Thread(target=child_read)
            thread_child.start()

        QtCore.QObject.connect(self.main.PipeSendButton, QtCore.SIGNAL("clicked()"), PipSend)

    # depend on setOtherButton
    def setForkButton(self):
        def myFork():
            if len(sys.argv) == 1 and self.onlyone == 0:  # in parent process
                self.onlyone = 1
                if sys.platform[:3] == 'win':
                    pypath = sys.executable
                    os.spawnv(os.P_NOWAIT, pypath, ('python3', 'IPC_Test_Frame.py', str(0)))
                    pass
                else:
                    pid = os.fork()
                    if pid == 0:
                        # os.execlp('python3','python3','child_test.py',str(pid),str(self.child_pipe_read),str(self.child_pipe_write))
                        os.execlp('python3', 'python3', 'IPC_Test_Frame.py', str(pid))
                    else:
                        pass

        self.onlyone = 0
        QtCore.QObject.connect(self.main.forkButton, QtCore.SIGNAL("clicked()"), myFork)

    def setLCDNumber(self):
        self.num = 0


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow_IPC()
    main.show()
    sys.exit(app.exec())
