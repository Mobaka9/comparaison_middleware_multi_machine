import argparse
import logging

#from ingescape_protocol import IngescapeProtocol
from zeromq_protocol import ZeroMQProtocol
from ivy_protocol import IvyProtocol
from message_analyzer import MessageReceiver

from time import sleep

count = 0


def main_receive(protocol, message_count, port, regexp_match_count, recv_id, ivybus_test_manager):
    #    protocol, message_count, port, length, flag, i,
    #    nmbre_rec, multi_recv, direct_msg, device

    logging.error("Instanciating RECEIVER")
    com = "SUB"
    if protocol == 'ivy':
        protocol_obj = IvyProtocol(port, com, recv_id, ivybus_test_manager)
        protocol_obj.initialize()
    elif protocol == 'zeromq':
        port = int(port)
        # port +=1
        protocol_obj = ZeroMQProtocol(port, com, ivybus_test_manager)
        protocol_obj.initialize()
    # elif protocol == 'kafka':
    #     protocol_obj = KafkaProtocol(com)
    #     protocol_obj.initialize()
    # elif protocol == 'ingescape':
    #     protocol_obj = IngescapeProtocol(com, port, device, index_recv)
    #     protocol_obj.initialize()
    else:
        print("Unsupported protocol: " + str(protocol))
        return

    logging.info('Démarrage du receveur')

    # receiver = MessageReceiver(protocol_obj, protocol)
    results = protocol_obj.receive_messages(message_count, regexp_match_count)
    logging.warning(f"Recv #{recv_id} All messages received, sending results...")
    # results = receiver.analyze_messages()

    protocol_obj.send_results(results)
    logging.warning(f"Recv #{recv_id} RESULTS sent !")
    protocol_obj.stopsocket()
    '''sender = MessageSender(protocol_obj)
    sender.send_messages(message_count)'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Envoi de messages entre 2 terminaux avec 3 middleware', add_help=True)
    parser.add_argument('--protocol', help='Protocole à utiliser (ivy, zeromq, kafka)')
    parser.add_argument('--client_id', help='identifiant du client', default="test")
    parser.add_argument('--message_count', default=1, type=int, help='Nombre de messages à envoyer')
    parser.add_argument('--flag_count', default=0, type=int, help='Nombre de match regexp')
    parser.add_argument('--port', help='Port ou addresse (seulement pour ivy)') #TODO: pourquoi seulement pour IVY alors que ZMQ l'utilise ?
    parser.add_argument('--log_level', default='FATAL', help='Niveau de configuration de la journalisation')
    # parser.add_argument('--device', default=None, help='nom du peripherique réseau utilisé pour ingescape')
    parser.add_argument('--ivybus_test_manager', help='ivy bus pour la synchro des tests')


    param = parser.parse_args()

    # Configurer la journalisation
    logging.basicConfig(
        level=param.log_level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log', mode='w')
        ]
    )

    main_receive(param.protocol, param.message_count, param.port, param.flag_count, param.client_id, param.ivybus_test_manager)