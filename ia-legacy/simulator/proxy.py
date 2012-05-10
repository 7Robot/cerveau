# -*- coding: utf-8 -*-
'''
Created on 3 mai 2012
'''

import socket, threading

class Proxy:
    def __init__(self, port_ia=7773, port_simu=8773):
        self.ia_server = Server("ia", "127.0.0.1", port_ia)
        self.simu_server = Server("simu", "127.0.0.1", port_simu)
        self.ia_server.other = self.simu_server
        self.simu_server.other = self.ia_server
        
    def main(self):
        self.ia_server.start()
        self.simu_server.start()
        


class Server(threading.Thread):
    def __init__(self, name="Server", ip='127.0.0.1', port=7773):
        threading.Thread.__init__(self)
        self.running   = threading.Event( )
        self.s    = socket.socket()
        self.ip   = ip
        self.port = port
        self.conn = None # socket avec le client
        
    def run(self):
        self.s.bind((self.ip, self.port))
        self.s.listen(1)
        self.conn, self.address = self.s.accept()
        print("%s:%d connected" % (self.address[0], self.address[1]))

        keep_on = True
        while keep_on:
            try:
                cmd = self.conn.makefile(buffering=1, errors='replace').readline()
                if cmd == "":
                    keep_on = False
                else:
                    print ("Test server received \t", cmd)
                    self.other.send_cmd(cmd)
            except (socket.timeout,socket.error) as message:
                print ("recv_cmd : socket error", message) #TODO: logger.fatal
                keep_on = False
            

        
    def send_cmd(self, cmd):
        try:
            self.conn.send(bytes(cmd+'\n', "utf-8"))
        except (socket.timeout,socket.error) as message:
            print ("send_cmd : timout", message) #TODO: logger.fatal
        
    def stop(self):
        self.running.set( )
        if self.conn != None:
            self.conn.shutdown(socket.SHUT_WR)
            self.conn.close()
        self.s.shutdown(socket.SHUT_WR)
        self.s.close()
        

        
if __name__ == "__main__":
    proxy = Proxy()
    proxy.main()
        