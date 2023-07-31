import getopt
import os
import string
from time import sleep, time
import sys
import time
from abstract_protocol import AbstractProtocol
from ivy.ivy import IvyServer, IvyApplicationDisconnected, IvyApplicationConnected

class IvyProtocol(AbstractProtocol):
    
    def __init__(self,args,logger,com,queue):
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
        self.total=0
        self.queue=queue
        self.ivybus=None
    
    
   
        
    def initialize(self):
        
            if self.com == "PUB":
                IVYAPPNAME = 'Sender'

            else:
                IVYAPPNAME = 'Receiver'

            sivybus = ''
            sisreadymsg = f"ready {IVYAPPNAME}"                              
            def lprint(fmt, *arg):

                print(IVYAPPNAME + ': ' + fmt % arg)

                
            def usage(scmd):
                lpathitem = string.split(scmd, '/')
                fmt = '''Usage: %s [-h] [-b self.IVYBUS | --self.ivybus=self.IVYBUS]
                where
                \t-h provides the usage message;
                \t-b self.IVYBUS | --self.ivybus=self.IVYBUS allow to provide the self.IVYBUS string in the form
                \t adresse:port eg. 127.255.255.255:2010
                '''
                print(fmt % lpathitem[-1])
            
            def oncxproc(agent, event_type):
                print("in callback")
                if event_type == IvyApplicationDisconnected:
                    #lprint('Ivy application %r was disconnected', agent)
                    if self.com == "PUB":
                        self.queue.put(f"close_sock {agent}")
                elif event_type == IvyApplicationConnected:
                    #lprint('Ivy application %r was connected', agent)
                    if self.com == "PUB":
                        str_ready = "RECEIVER_READY "+str(agent)
                        print(f"ok test entre {str_ready}" )
                        print(f"queue: {self.queue}")
                        self.queue.put(str_ready)
                lprint('currents Ivy application are [%s]', self.ivybus.get_clients())


            def ondieproc(agent, _id):
                lprint('received the order to die from %r with id = %d', agent, _id)

                    
            sivybus = self.args
            sechoivybus = sivybus
            lprint('Ivy will broadcast on %s ', sechoivybus)

                # initialising the bus
            self.ivybus = IvyServer(IVYAPPNAME,     # application name for Ivy
            sisreadymsg,    # ready message              
            oncxproc,       # handler called on connection/disconnection
            ondieproc)

            self.ivybus.start(sivybus)
            print("bon fichier")
    # binding on dedicated message : starting with 'hello ...'
    # binding to every message
            
            if self.com == "PUB":
                sleep(1)
                self.ivybus.bind_msg(self.onmsgprocready, 'ready(.*)')

            self.is_initialized = True
            

    def send_message(self, message):
            self.ivybus.send_msg(message)


            
    @staticmethod
    def lprint(fmt, *arg):
            IVYAPPNAME = 'pyhello'
            print(IVYAPPNAME + ': ' + fmt % arg)

    def onmsgprocready(self,agent, *larg):
        pass
    #     print(larg[0])
    #     str_ready = "RECEIVER_READY "+str(agent)
    #     print(f"test entre {str_ready}" )
    #     self.queue.put(str_ready)

    def onmsgprocbind(self,agent, *larg):
        #self.lprint('Received from %r: [%s] ', agent, larg[1])
        t1= time.time()
        tmp = [self.id, larg[0], t1]
        print(tmp)
        self.plt_data.append(tmp)  
        self.id+=1
        
    def onmsgproc2(self, agent, *larg):
        t1= time.time()
        self.msg = larg[self.id]
        tmp = [self.id, larg[:50],t1, larg[-1]]
        self.plt_data.append(tmp)
        self.id+=1
        self.pop_hello = False
        
        
    
            
    def receive_message(self,message_count,queue,total_rec,direct_msg,flag):
        
       
        if flag:
            self.ivybus.bind_msg(self.onmsgproc2, 'flag0=(\S*) flag1=(\S*) flag2=(\S*) flag3=(\S*) flag4=(\S*) flag5=(\S*) flag6=(\S*) flag7=(\S*) flag8=(\S*) flag9=(\S*) flag10=(\S*) flag11=(\S*) flag12=(\S*) flag13=(\S*) flag14=(\S*) flag15=(\S*) flag16=(\S*) flag17=(\S*) flag18=(\S*) flag19=(\S*) flag20=(\S*) flag21=(\S*) flag22=(\S*) flag23=(\S*) flag24=(\S*) flag25=(\S*) flag26=(\S*) flag27=(\S*) flag28=(\S*) flag29=(\S*) flag30=(\S*) flag31=(\S*) flag32=(\S*) flag33=(\S*) flag34=(\S*) flag35=(\S*) flag36=(\S*) flag37=(\S*) flag38=(\S*) flag39=(\S*) flag40=(\S*) flag41=(\S*) flag42=(\S*) flag43=(\S*) flag44=(\S*) flag45=(\S*) flag46=(\S*) flag47=(\S*) flag48=(\S*) flag49=(\S*) flag50=(\S*) flag51=(\S*) flag52=(\S*) flag53=(\S*) flag54=(\S*) flag55=(\S*) flag56=(\S*) flag57=(\S*) flag58=(\S*) flag59=(\S*) flag60=(\S*) flag61=(\S*) flag62=(\S*) flag63=(\S*) flag64=(\S*) flag65=(\S*) flag66=(\S*) flag67=(\S*) flag68=(\S*) flag69=(\S*) flag70=(\S*) flag71=(\S*) flag72=(\S*) flag73=(\S*) flag74=(\S*) flag75=(\S*) flag76=(\S*) flag77=(\S*) flag78=(\S*) flag79=(\S*) flag80=(\S*) flag81=(\S*) flag82=(\S*) flag83=(\S*) flag84=(\S*) flag85=(\S*) flag86=(\S*) flag87=(\S*) flag88=(\S*) flag89=(\S*) flag90=(\S*) flag91=(\S*) flag92=(\S*) flag93=(\S*) flag94=(\S*) flag95=(\S*) flag96=(\S*) flag97=(\S*) flag98=(\S*) flag99=(\S*) flag100=(\S*) flag101=(\S*) flag102=(\S*) flag103=(\S*) flag104=(\S*) flag105=(\S*) flag106=(\S*) flag107=(\S*) flag108=(\S*) flag109=(\S*) flag110=(\S*) flag111=(\S*) flag112=(\S*) flag113=(\S*) flag114=(\S*) flag115=(\S*) flag116=(\S*) flag117=(\S*) flag118=(\S*) flag119=(\S*) flag120=(\S*) flag121=(\S*) flag122=(\S*) flag123=(\S*) flag124=(\S*) flag125=(\S*) flag126=(\S*) flag127=(\S*) flag128=(\S*) flag129=(\S*) flag130=(\S*) flag131=(\S*) flag132=(\S*) flag133=(\S*) flag134=(\S*) flag135=(\S*) flag136=(\S*) flag137=(\S*) flag138=(\S*) flag139=(\S*) flag140=(\S*) flag141=(\S*) flag142=(\S*) flag143=(\S*) flag144=(\S*) flag145=(\S*) flag146=(\S*) flag147=(\S*) flag148=(\S*) flag149=(\S*) flag150=(\S*) flag151=(\S*) flag152=(\S*) flag153=(\S*) flag154=(\S*) flag155=(\S*) flag156=(\S*) flag157=(\S*) flag158=(\S*) flag159=(\S*) flag160=(\S*) flag161=(\S*) flag162=(\S*) flag163=(\S*) flag164=(\S*) flag165=(\S*) flag166=(\S*) flag167=(\S*) flag168=(\S*) flag169=(\S*) flag170=(\S*) flag171=(\S*) flag172=(\S*) flag173=(\S*) flag174=(\S*) flag175=(\S*) flag176=(\S*) flag177=(\S*) flag178=(\S*) flag179=(\S*) flag180=(\S*) flag181=(\S*) flag182=(\S*) flag183=(\S*) flag184=(\S*) flag185=(\S*) flag186=(\S*) flag187=(\S*) flag188=(\S*) flag189=(\S*) flag190=(\S*) flag191=(\S*) flag192=(\S*) flag193=(\S*) flag194=(\S*) flag195=(\S*) flag196=(\S*) flag197=(\S*) flag198=(\S*) flag199=(\S*) #(\S*)')
        else:
            self.ivybus.bind_msg(self.onmsgprocbind, 'hello(.*)')
            self.ivybus.bind_msg(self.onmsgprocbind, 'bonjour(.*)')
 
            
        
        sleep(2)
        

        while len(self.plt_data) != message_count:
            pass
        #print(self.plt_data)
        # if self.pop_hello:
        #     self.plt_data= self.plt_data[total_rec:]
        return self.plt_data
    
    def stopsocket(self):
        
        print("total",self.total)
        if self.com!="SUB":
            print("sub")
        self.ivybus.stop()