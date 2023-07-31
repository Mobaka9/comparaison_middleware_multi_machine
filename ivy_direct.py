import getopt
import os
import string
from ivy.std_api import *
from time import sleep, time
import sys
import time
from abstract_protocol import AbstractProtocol



class IvyDirectProtocol(AbstractProtocol):
    
    def __init__(self,args,logger,com):
        self.is_initialized = False
        self.args = args
        self.send_end = ""
        self.id = 0
        self.plt_data = []
        self.wait = True
        self.logger = logger
        self.pop_hello = True
        self.com = com
        self.client=""
        
    
    
   
        
    def initialize(self):
        
            if self.com == "PUB":
                IVYAPPNAME = 'Sender'

            else:
                IVYAPPNAME = 'Receiver'

            sivybus = ''
            sisreadymsg = '[%s is ready]' % IVYAPPNAME                               
            def lprint(fmt, *arg):

                print(IVYAPPNAME + ': ' + fmt % arg)

                
            def usage(scmd):
                lpathitem = string.split(scmd, '/')
                fmt = '''Usage: %s [-h] [-b IVYBUS | --ivybus=IVYBUS]
                where
                \t-h provides the usage message;
                \t-b IVYBUS | --ivybus=IVYBUS allow to provide the IVYBUS string in the form
                \t adresse:port eg. 127.255.255.255:2010
                '''
                print(fmt % lpathitem[-1])
            
            def oncxproc(agent, connected):
                if connected == IvyApplicationDisconnected:
                    lprint('Ivy application %r was disconnected', agent)
                else:
                    lprint('Ivy application %r was connected', agent)
                lprint('currents Ivy application are [%s]', IvyGetApplicationList())


            def ondieproc(agent, _id):
                lprint('received the order to die from %r with id = %d', agent, _id)

                    
            
            sivybus = self.args
            sechoivybus = sivybus
            lprint('Ivy will broadcast on %s ', sechoivybus)

                # initialising the bus
            IvyInit(IVYAPPNAME,     # application name for Ivy
                    sisreadymsg,    # ready message
                    0,              # main loop is local (ie. using IvyMainloop)
                    oncxproc,       # handler called on connection/disconnection
                    ondieproc)      # handler called when a <die> message is received
            IvyStart(sivybus)
            if self.com == "PUB":
                sleep(1)
                self.client = IvyGetApplication('Receiver')   

            self.is_initialized = True
            

    def send_message(self, message):
            IvySendDirectMsg(self.client,1, message)

            
    @staticmethod
    def lprint(fmt, *arg):
            IVYAPPNAME = 'pyhello'
            print(IVYAPPNAME + ': ' + fmt % arg)

    def onmsgproc(self,agent, *larg):
        #self.lprint('Received from %r: [%s] ', agent, larg[1])
        t1= time.time()
        tmp = [self.id, larg[1], t1]
        self.plt_data.append(tmp)  
        self.id+=1


        
    
        
        
    
            
    def receive_message(self,message_count,queue,total_rec,direct_msg,flag):
        
        IvyBindDirectMsg(self.onmsgproc)
       
        sleep(2)
        

        while(self.send_end != "LAST_MESSAGE"):
            print(self.send_end)
            self.send_end = queue.get()
            print(self.send_end)

        if not direct_msg:
            if self.pop_hello:
                self.plt_data= self.plt_data[total_rec:]
        return self.plt_data
    
    def stopsocket(self):
        IvyStop()