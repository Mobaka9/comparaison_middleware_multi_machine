from abc import ABC, abstractmethod
from ivy.ivy import IvyServer, IvyApplicationDisconnected, IvyApplicationConnected


class AbstractProtocol(ABC):
    def __init__(self):
        self.ivybus2= None
        self.IVYAPPNAME=""

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def send_message(self, message, topic):
        pass

    @abstractmethod
    def receive_message(self):
        pass 
    
    @abstractmethod
    def stopsocket(self):
        pass
    
    def ivy_secondaire(self, args, com, id_rec, callback_ready):
        if com == "PUB":
            self.IVYAPPNAME = f"Sender_secondaire"
        else:
            self.IVYAPPNAME = f"Receiver_{id_rec}_secondaire"

        sivybus = ''
        sisreadymsg = f"ready {self.IVYAPPNAME}"                              
        def lprint(fmt, *arg):

            print(self.IVYAPPNAME + ': ' + fmt % arg)


        
        def oncxproc(agent, event_type):
            if event_type == IvyApplicationDisconnected:
                #lprint('Ivy application %r was disconnected', agent)
                if self.com == "SUB":
                    if "sender" in agent:
                        pass
            elif event_type == IvyApplicationConnected:
                lprint('Ivy application %r was connected', agent)

            lprint('currents Ivy application are [%s]', self.ivybus2.get_clients())


        def ondieproc(agent, _id):
            lprint('received the order to die from %r with id = %d', agent, _id)

                

        broadcast = args.split(":")
        port1=int(broadcast[1])
        sivybus = broadcast[0]+":"+str(port1+1)
        lprint('Ivy will broadcast on %s ', sivybus)

            # initialising the bus
        self.ivybus2 = IvyServer(self.IVYAPPNAME,     # application name for Ivy
                                sisreadymsg,    # ready message              
                                oncxproc,       # handler called on connection/disconnection
                                ondieproc)

        self.ivybus2.start(sivybus)
            
        if self.com=="SUB":
            self.ivybus2.bind_msg(callback_ready,'ready(.*)')
    
    def send_ready(self):
        self.ivybus2.send_msg(f"ready :{self.IVYAPPNAME}")
