
import sys
import ingescape as igs
import getopt
import os
import string
from time import sleep, time
import sys
import time
from abstract_protocol import AbstractProtocol

def string_input_callback(iop_type, iop_name, value_type, value, my_data):
    #igs.output_set_int("out", value)
    #igs.info(f"received {value}")
    callback_self = my_data
    if isinstance(callback_self,IngescapeProtocol):
        #print("hey")
        t1= time.time()
        tmp = [callback_self.id, value, t1]
        callback_self.plt_data.append(tmp) 
        #print(f"{callback_self.id_rec}receiving message number {callback_self.id}") 
        callback_self.id+=1
    else:
        print("error callback_self")


def on_agent_event_callback(event, uuid, name, event_data, my_data):
    callback_self=my_data
    if isinstance(callback_self,IngescapeProtocol):
        
        if event == igs.PEER_ENTERED:
            print(f"{callback_self.APPNAME}: PEER_ENTERED about {name}")
        elif event == igs.PEER_EXITED:
            print(f"{callback_self.APPNAME}: PEER_EXITED about {name}")
        elif event == igs.AGENT_ENTERED:
            print(f"{callback_self.APPNAME}: AGENT_ENTERED about {name}")
        elif event == igs.AGENT_UPDATED_DEFINITION:
            print(f"{callback_self.APPNAME}: AGENT_UPDATED_DEFINITION about {name}")
        elif event == igs.AGENT_KNOWS_US:
            print(f"{callback_self.APPNAME}: AGENT_KNOWS_US about {name}")
            if callback_self.com =="PUB":
                if "Receiver" in name:
                    str_ready = "RECEIVER_READY "+str(name)
                    print(f"test entre {str_ready}" )
                    callback_self.queue.put(str_ready)   
        elif event == igs.AGENT_EXITED:
            print(f"{callback_self.APPNAME}: AGENT_EXITED about {name}")
            if callback_self.com == "PUB":
                if "Receiver" in name:
                    callback_self.queue.put(f"close_sock {name}")
                
        elif event == igs.AGENT_UPDATED_MAPPING:
            print(f"{callback_self.APPNAME}: AGENT_UPDATED_MAPPING about {name}")
        elif event == igs.AGENT_WON_ELECTION:
            print(f"{callback_self.APPNAME}: AGENT_WON_ELECTION about {name}")
        elif event == igs.AGENT_LOST_ELECTION:
            print(f"{callback_self.APPNAME}: AGENT_LOST_ELECTION about {name}")
        else:
            print(f"{callback_self.APPNAME}: UNKNOWN event about {name}")
    else:
        print(f"{callback_self.APPNAME}: error callback event")

class IngescapeProtocol(AbstractProtocol):
    
    def __init__(self,com,port,device,id_rec,queue):
        self.is_initialized = False
        self.port = port
        self.send_end = ""
        self.id = 0
        self.plt_data = []
        self.wait = True
        self.device=device
        self.com = com
        self.client=""
        self.id_rec=id_rec
        self.APPNAME=""
        self.queue = queue
        self.ready_sent=False
        self.count_close=0

        
        
    def initialize(self):
        
            if self.com == "PUB":
                IGSAPPNAME = 'Sender'

            else:
                IGSAPPNAME = 'Receiver_'+str(self.id_rec)
            self.APPNAME=IGSAPPNAME

            
            # def oncxproc(agent, connected):
            #     if connected == IvyApplicationDisconnected:
            #         lprint('Ivy applicatio)n %r was disconnected', agent)
            #     else:
            #         lprint('Ivy applicatio)n %r was connected', agent)
            #     lprint('currents Ivy a)pplication are [%s]', IvyGetApplicationList())


            # def ondieproc(agent, _id):
            #     lprint('received the o)rder to die from %r with id = %d', agent, _id)

            print(f'Ingescape {IGSAPPNAME} will communicate on device {self.device} and port {self.port}')
            igs.agent_set_name(IGSAPPNAME)
            igs.log_set_console(True)
            igs.log_set_file(True, None)
            igs.definition_set_version("1.0")
            igs.observe_agent_events(on_agent_event_callback, self)
            igs.net_set_high_water_marks(0)
            #igs.net_raise_sockets_limit()
            igs.log_set_console_level(igs.LOG_FATAL)
            
            if self.com=="PUB":
                igs.output_create("out", igs.STRING_T, None)
            else:
                igs.input_create("in", igs.STRING_T, None)
                igs.observe_input("in", string_input_callback, self)
                igs.mapping_add("in", "Sender", "out")
            
            igs.start_with_device(self.device, int(self.port))


            self.is_initialized = True
            

    def send_message(self, message):
            #sleep(0.00001)
            #IvySendDirectMsg(self.client,1, message)
            igs.output_set_string("out", message)
    
    

    def receive_message(self,message_count,queue,total_rec,direct_msg,flag):
            

        #sleep(5)
        
        while len(self.plt_data) != message_count:
            pass
            # sleep(1)
            # print(f"{self.APPNAME} not finished")

        # queue.put(f"close_sock {self.APPNAME}")
        
        # print("close sent by rcv for snd")
        # print(self.plt_data)
        # print(len(self.plt_data))

        # while(self.send_end != "LAST_MESSAGE"):
        #     print(self.send_end)
        #     self.send_end = queue.get()
        #     print(self.send_end)
        return self.plt_data
    
    def stopsocket(self):
        print(f"trying to close {self.APPNAME}")
        igs.stop()
        