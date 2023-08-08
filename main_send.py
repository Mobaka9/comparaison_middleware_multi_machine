import argparse
import csv
import logging
import random
import string
import time
# from ingescape_protocol import IngescapeProtocol
from ivy_protocol import IvyProtocol
from zeromq_protocol import ZeroMQProtocol
from time import sleep




def main_send(protocol, message_count, port, length, sender_sleep_duration, flag_count, nbr_receivers,
              device, ivybus_test_manager):
    com = "PUB"
    if protocol == 'ivy':
        args = port
        # if direct_msg:
        #     protocol_obj = IvyDirectProtocol(args, port, com, ivybus_test_manager)
        #     protocol_obj.initialize()
        # else:
        # TODO : le main_receive ne gère pas le cas IvyDirect
        protocol_obj = IvyProtocol(port, com, 'send', ivybus_test_manager)
        protocol_obj.initialize()

    elif protocol == 'zeromq':
        port = int(port)
        # port+=1
        protocol_obj = ZeroMQProtocol(port, com, 'send', ivybus_test_manager)
        protocol_obj.initialize()
    # elif protocol == 'kafka':
    #     protocol_obj = KafkaProtocol(com,logger)
    #     protocol_obj.initialize()
    # elif protocol == 'ingescape':
    #     protocol_obj = IngescapeProtocol(com, port, device, ivybus_test_manager)
    #     protocol_obj.initialize()

    else:
        print("Protocole invalide spécifié")
        return

    logging.info('Démarrage du sender')

    protocol_obj.wait_for_all_receivers(nbr_receivers)
    logging.error("ALL RECEIVERS READY !")

    message_rand = generate_message_load(flag_count, length)

    for i in range(message_count):
        start_time = time.time()
        message = str(message_rand) + str(start_time)
        logging.warning(f"Message #{i} sent.")
        protocol_obj.send_message(message)
        sleep(sender_sleep_duration)

    print("envoi termine")

    results = protocol_obj.wait_for_all_results(nbr_receivers)
    
    write_csv_results(results)

    protocol_obj.stopsocket()
    print(f"-------------{results}")

    temps_totaux=[]
    for i in range(nbr_receivers):
        print(f"fnr{i}")
        temps_totaux.append((results[0][i][-1]["end_time"]) - (results[0][i][0]["start_time"]))
        

def generate_message_load(flag_count, length):
    length_of_string = int(length)
    message_rand = ""
    if flag_count > 0:
        for j in range(flag_count):
            message_rand = message_rand + "flag" + str(j) + "=" + ''.join(
                random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)) + " "

        message_rand = message_rand + "start_time="
    else:
        message_rand = ''.join(
            random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)) + "start_time="
    return message_rand


def write_csv_results(results):
    data_file = open('results.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)
    header_row = 0
    for data in results:
        for receiver_data in data:
            if header_row == 0:
                header = receiver_data.keys()
                csv_writer.writerow(header)
                header_row += 1
            csv_writer.writerow(receiver_data.values())
    data_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Envoi de messages entre 2 terminaux avec 3 middleware', add_help=True)
    parser.add_argument('--protocol', help='Protocole à utiliser (ivy, zeromq, kafka)')
    parser.add_argument('--message_count', default=1, type=int, help='Nombre de messages à envoyer')
    parser.add_argument('--message_length', type=int, help='taille des messages à envoyer')
    parser.add_argument('--flag_count', default=0, type=int, help='Nombre de match regexp')
    parser.add_argument('--port', help='Port ou addresse (seulement pour ivy)')
    parser.add_argument('--sleep', help='temps attente entre messages (s)')
    parser.add_argument('--log_level', default='FATAL', help='Niveau de configuration de la journalisation')
    parser.add_argument('--direct_msg', action='store_true', help="envoyer des messages ivy avec ivydirectmsg")
    parser.add_argument('--device', default=None, help='nom du peripherique réseau utilisé pour ingescape')
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

    main_send(param.protocol, param.message_count, param.port, param.message_length, param.sleep, param.flag_count,
              param.nbr_processes,
              param.device, param.ivybus_test_manager)
