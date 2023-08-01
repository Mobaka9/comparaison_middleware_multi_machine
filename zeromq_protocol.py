import zmq
from abstract_protocol import AbstractProtocol
import time
from time import sleep


class ZeroMQProtocol(AbstractProtocol):
    def __init__(self, port, com, client_id, ivybus_test_manager):
        AbstractProtocol.__init__(self, ivybus_test_manager, com, client_id)
        self.port = port
        self.socket = None
        self.context = None
        self.com = com
        self.plt_data = []
        self.last_received_msg_id = 0
        self.send_end = ""
        self.socket_test = None
        self.topic = "10001"
        self.port_test = "5557"

    def initialize(self):
        self.context = zmq.Context()
        if self.com == "PUB":
            self.socket = self.context.socket(zmq.PUB)
            self.socket.setsockopt(zmq.SNDHWM, 1000000)
            self.socket.bind("tcp://*:%s" % self.port)

            # sleep(3)

        else:
            self.socket = self.context.socket(zmq.SUB)
            self.socket.setsockopt(zmq.RCVHWM, 1000000)
            self.socket.connect("tcp://localhost:%s" % self.port)

    def send_message(self, message):
        # sleep(0.0001)

        topic_message = str(self.topic) + "&" + str(message)  # Ajouter le topic au message
        self.socket.send_string(topic_message)

    def receive_messages(self, message_count, flag_count):
        # initialisation

        topicfilter = "10001"
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "10002")

        for _ in range(message_count):
            # print(i)
            string = self.socket.recv()
            t1 = time.time()
            # topic, messagedata = string.split()
            topic, messagedata = string.decode('utf-8').split("&")
            # print(messagedata)

            #TODO: Il faut mettre le regexp match ici

            self.durations.append({"msg_id": self.last_received_msg_id,
                                   "start_time": float(messagedata.split("start_time=")[1]),
                                   "end_time": t1,
                                   "duration": (t1 - float(messagedata.split("start_time=")[1])),
                                   "recv_id": self.client_id
                                   })

            # if topic == "10001" :
            self.last_received_msg_id += 1
            tmp = [self.last_received_msg_id, messagedata, t1]
            self.plt_data.append(tmp)

        # while (self.send_end != "LAST_MESSAGE"):
        #     self.send_end = queue.get()

        return self.durations

    def stopsocket(self):
        try:
            self.socket.close()

        except:
            pass  # log or print any EXC-case here, as needed

        finally:
            self.context.term()
