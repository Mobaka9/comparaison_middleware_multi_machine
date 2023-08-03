import json
import logging
from abc import ABC, abstractmethod
from time import sleep

from ivy.ivy import IvyServer, IvyApplicationDisconnected, IvyApplicationConnected


class AbstractProtocol(ABC):
    def __init__(self, ivybus_test_manager, com, id_rec=''):
        self.com=com
        if self.com == "PUB":
            IVYAPPNAME = "Sender_secondaire"
        else:
            IVYAPPNAME = f"Receiver_{id_rec}_secondaire"
        
        sisreadymsg = f"ready {IVYAPPNAME}"
        self.receivers_count = 0
        self.results = []
        self.durations = []
        self.client_id = id_rec
        self.results_received = 0
        self.allow_send_ready = False
        self.ready_sent = False

        
        

        def oncxproc(agent, event_type):
            if event_type == IvyApplicationDisconnected:
                print(f'Ivy application {agent} was disconnected')
                
            elif event_type == IvyApplicationConnected:
                print(f"agent: {agent} by {IVYAPPNAME}")
                if self.com == "SUB":
                    if "Sender" in str(agent) :
                        self.allow_send_ready = True
                print(f'Ivy application {agent} was connected')


            # print('currents Ivy application are [%s]', self.ivybus2.get_clients())
        def ondieproc(agent, _id):
            print('received the order to die from %r with id = %d', agent, _id)
            self.stopsocket()

        def on_results(agent, data):
            print(f"resultats recu {self.results_received}")
            self.results_received += 1
            self.results.append(json.loads(data.replace("'", '"')))
            # print(f"results received: {self.results}")
        
        def callback_ready(agent, *larg):
            self.receivers_count += 1

        self.ivybus_test_manager = IvyServer(IVYAPPNAME,  # application name for Ivy
                                             sisreadymsg,  # ready message
                                             oncxproc,  # handler called on connection/disconnection
                                             ondieproc)

        if self.com=="PUB":
            self.ivybus_test_manager.bind_msg(callback_ready,'Ready(.*)')
        self.ivybus_test_manager.bind_msg(on_results, 'RESULTS=(.*)')
        self.ivybus_test_manager.start(ivybus_test_manager)
    
    
        
        
    def send_ready_message(self):
        print("entered")
        while self.allow_send_ready != True:
            
            pass
        if not self.ready_sent:
            self.ivybus_test_manager.send_msg(f"Ready to receive")
        self.ready_sent=True
        

    def wait_for_all_receivers(self, count):
        while self.receivers_count != count:
            logging.error(f"wait_for_all_receivers({self.receivers_count}, {count})")
            sleep(0.1)


    def wait_for_all_results(self, count):
        while self.results_received != count:
            print(f"Sender wait for results: {len(self.results)}")
            sleep(0.1)
        return self.results

    def send_results(self, results):
        self.ivybus_test_manager.send_msg(f"RESULTS={results}")

    def test_manager_stop(self):
        self.ivybus_test_manager.stop()

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def receive_messages(self, message_count, flag_count):
        pass

    @abstractmethod
    def stopsocket(self):
        pass
