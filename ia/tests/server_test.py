# -*- coding: utf-8 -*-
u'''
Created on 28 avr. 2012
'''

import socket, threading



class Server_test(threading.Thread):
    def __init__(self, ip=u'127.0.0.1', port=7773):
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
        print u"%s:%d connected" % (self.address[0], self.address[1])
        self.rcv_thread = threading.Thread(None, self.recv_cmd, None, (), {})
        self.rcv_thread.start()
        self.tests()
        
    def recv_cmd(self):
        keep_on = True
        while keep_on:
            try:
                cmd = self.conn.makefile(buffering=1, errors=u'replace').readline()
                if cmd == u"":
                    keep_on = False
                else:
                    print u"Test server received \t", cmd
            except (socket.timeout,socket.error), message:
                print u"recv_cmd : socket error", message #TODO: logger.fatal
                keep_on = False
            

        
    def send_cmd(self, cmd):
        try:
            self.conn.send(str(cmd+'\n').encode("utf-8"))
        except (socket.timeout,socket.error), message:
            print u"send_cmd : timout", message #TODO: logger.fatal
        
    def stop(self):
        self.running.set( )
        if self.conn != None:
            self.conn.shutdown(socket.SHUT_WR)
            self.conn.close()
        self.s.shutdown(socket.SHUT_WR)
        self.s.close()
        
        
    def tests(self):
        pass
        

      
