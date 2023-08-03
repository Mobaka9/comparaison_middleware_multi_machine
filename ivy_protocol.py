import getopt
import logging
import os
import string
import threading
from time import sleep, time
import sys
import time
from abstract_protocol import AbstractProtocol
from ivy.ivy import IvyServer, IvyApplicationDisconnected, IvyApplicationConnected


class IvyProtocol(AbstractProtocol):

    def __init__(self, port, com, client_id, ivybus_test_manager):
        AbstractProtocol.__init__(self, ivybus_test_manager, com, client_id)
        self.is_initialized = False
        self.send_end = ""
        self.last_received_msg_id = 0
        self.plt_data = []

        self.wait = True
        self.com = com
        self.client = ""
        self.total = 0
        self.ivybus = None
        self.port = port
        


    def initialize(self):

        if self.com == "PUB":
            IVYAPPNAME = 'Sender'

        else:
            IVYAPPNAME = f'Receiver_{self.client_id}'

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
            pass
            # print("in callback")
            # if event_type == IvyApplicationDisconnected:
            #     lprint('Ivy application %r was disconnected', agent)
            # elif event_type == IvyApplicationConnected:
            #     lprint('Ivy application %r was connected', agent)
            # lprint('currents Ivy application are [%s]', self.ivybus.get_clients())

        def ondieproc(agent, _id):
            lprint('received the order to die from %r with id = %d', agent, _id)

        sivybus = self.port
        sechoivybus = sivybus
        lprint('Ivy will broadcast on %s ', sechoivybus)

        # initialising the bus
        self.ivybus = IvyServer(IVYAPPNAME,  # application name for Ivy
                                sisreadymsg,  # ready message
                                oncxproc,  # handler called on connection/disconnection
                                ondieproc)

        self.ivybus.start(sivybus)
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

    def onmsgprocready(self, agent, *larg):
        pass

    #     print(larg[0])
    #     str_ready = "RECEIVER_READY "+str(agent)
    #     print(f"test entre {str_ready}" )
    #     self.queue.put(str_ready)

    def onmsgprocbind(self, agent, *larg):
        # self.lprint('Received from %r: [%s] ', agent, larg[1])
        t1 = time.time()
        data = float(larg[0].split("start_time=")[1])
        self.durations.append({"msg_id": self.last_received_msg_id,
                                   "start_time": data,
                                   "end_time": t1,
                                   "duration": (t1 - data),
                                   "recv_id": self.client_id
                                   })
        logging.error(f"client {self.client_id} message #{self.last_received_msg_id} received at {t1}")
        self.last_received_msg_id += 1

    def onmsgproc2(self, agent, *larg):
        t1 = time.time()
        self.durations.append({"msg_id" : self.last_received_msg_id,
                               "start_time" : float(larg[-1]),
                               "end_time": t1,
                               "duration": (t1 - float(larg[-1])),
                                 "recv_id":self.client_id
                                 })
        logging.error(f"client {self.client_id} message #{self.last_received_msg_id} received at {t1}")
        self.last_received_msg_id += 1

    def receive_messages(self, message_count, flag_count):

        if flag_count > 0:
            regexp = ' '.join(f"flag{i}=(\\S*)" for i in range(flag_count)) + " start_time=(\\S*)"
            self.ivybus.bind_msg(self.onmsgproc2, regexp)
        else:
            self.ivybus.bind_msg(self.onmsgprocbind, '(.*)')
            #self.ivybus.bind_msg(self.onmsgprocbind, 'bonjour(.*)')
        self.send_ready_message()

        # sleep(2)

        while len(self.durations) != message_count:
            pass
            # print(self.plt_data)
        # if self.pop_hello:
        #     self.plt_data= self.plt_data[total_rec:]
        return self.durations

    def stopsocket(self):
        logging.error(f"client {self.client_id}({self.com}) STOPPING sockets")
        self.ivybus.stop()
        self.test_manager_stop()
