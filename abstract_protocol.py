import json
import logging
from abc import ABC, abstractmethod
from time import sleep

from ivy.ivy import IvyServer, IvyApplicationDisconnected, IvyApplicationConnected


class AbstractProtocol(ABC):
    def __init__(self, ivybus_test_manager, com, id_rec=''):
        if com == "PUB":
            IVYAPPNAME = "Sender_secondaire"
        else:
            IVYAPPNAME = f"Receiver_{id_rec}_secondaire"

        sisreadymsg = f"ready {IVYAPPNAME}"
        self.receivers_count = 0
        self.results = []
        self.results_received = 0

        def oncxproc(agent, event_type):
            if event_type == IvyApplicationDisconnected:
                if "Receiver" in str(agent):
                    self.receivers_count = self.receivers_count - 1
            elif event_type == IvyApplicationConnected:
                if "Receiver" in str(agent):
                    self.receivers_count = self.receivers_count + 1

            # print('currents Ivy application are [%s]', self.ivybus2.get_clients())

        def ondieproc(agent, _id):
            print('received the order to die from %r with id = %d', agent, _id)
            self.stopsocket()

        def on_results(agent, data):
            self.results_received += 1
            self.results.append(json.loads(data.replace("'", '"')))
            # print(f"results received: {self.results}")

        self.ivybus_test_manager = IvyServer(IVYAPPNAME,  # application name for Ivy
                                             sisreadymsg,  # ready message
                                             oncxproc,  # handler called on connection/disconnection
                                             ondieproc)

        self.ivybus_test_manager.bind_msg(on_results, 'RESULTS=(.*)')
        self.ivybus_test_manager.start(ivybus_test_manager)

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

    # def send_ready(self):
    #     self.ivybus2.send_msg(f"ready :{self.IVYAPPNAME}")
