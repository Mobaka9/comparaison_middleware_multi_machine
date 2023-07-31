import zmq
from abstract_protocol import AbstractProtocol
import time
from time import sleep


class ZeroMQProtocol(AbstractProtocol):
    def __init__(self, port, com, logger):
        self.port = port
        self.socket = None
        self.context= None
        self.com = com
        self.plt_data = []
        self.id = 0
        self.send_end = ""
        self.socket_test = None
        self.topic = "10001"
        self.port_test = "5557"
        self.logger = logger

    def initialize(self):
        self.context = zmq.Context()
        if self.com == "PUB":
            self.socket = self.context.socket(zmq.PUB)
            self.socket.setsockopt(zmq.SNDHWM,1000000)
            self.socket.bind("tcp://*:%s" % self.port)
            

            #sleep(3)

        else:
            self.socket = self.context.socket(zmq.SUB)
            self.socket.setsockopt(zmq.RCVHWM, 1000000) 
            self.socket.connect("tcp://localhost:%s" % self.port)
            
        
          

    def send_message(self, message):
        #sleep(0.0001)

        topic_message = str(self.topic) + "&" + str(message)  # Ajouter le topic au message
        self.socket.send_string(topic_message)



    def receive_message(self,message_count,queue,total_rec,direct_msg,flag):
        #initialisation

        topicfilter = "10001"
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "10002")

        for i in range(message_count):
            #print(i)
            string = self.socket.recv()
            t1 = time.time()
            #topic, messagedata = string.split()
            topic, messagedata = string.decode('utf-8').split("&")
            #print(messagedata)
            
            #if topic == "10001" :
            self.id+=1
            tmp= [self.id, messagedata,t1]
            self.plt_data.append(tmp)

                
        while(self.send_end != "LAST_MESSAGE"):
            self.send_end = queue.get()

        
        return(self.plt_data)

    def stopsocket(self):
        try:
            self.socket.close()

        except:
            pass # log or print any EXC-case here, as needed

        finally:
            self.context.term()