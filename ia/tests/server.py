# -*- coding: utf-8 -*-
'''
Created on 28 avr. 2012
'''

import socket, threading



class Server_test(threading.Thread):
    def __init__(self, ip='127.0.0.1', port=7773):
        threading.Thread.__init__(self)
        self.running   = threading.Event( )
        self.ip = ip
        self.port = port
        self.s = socket.socket()
        self.conn = None # socket avec le client
        
    def run(self):
        self.s.bind((self.ip, self.port))
        self.s.listen(1)
        self.conn, self.address = self.s.accept()
        print("%s:%d connected" % (self.address[0], self.address[1]))
        rcv_thread = threading.Thread(None, self.recv_cmd, None, (), {})
        rcv_thread.start()
        self.tests()
        
    def recv_cmd(self):
        while self.running.isSet():
            cmd = self.conn.makefile().readline()
            print ("recv ", cmd)
        
    def send_cmd(self, cmd):
        self.conn.send(bytes(cmd+'\n', "utf-8"))
        
    def stop(self):
        self.running.set( )
        if self.conn != None:
            self.conn.close()
        self.s.close()
        
        
    def tests(self):
        pass
        

        