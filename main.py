import argparse
import logging
import os
import platform
import subprocess
import sys
import multiprocessing
from main_send import main_send
from main_receive import main_receive
from time import sleep


def start_zookeeper():
    subprocess.run(['zookeeper-server-start', '/usr/local/etc/kafka/zookeeper.properties'])


def start_kafka():
    subprocess.run(['kafka-server-start', '/usr/local/etc/kafka/server.properties'])



def main():
    

    


    parser = argparse.ArgumentParser(description='Envoi de messages entre 2 terminaux avec 3 middleware', add_help=True)
    parser.add_argument('--protocol', help='Protocole à utiliser (ivy, zeromq, kafka)')
    parser.add_argument('--message_count', default = 1, type=int, help='Nombre de messages à envoyer')
    parser.add_argument('--port', help='Port ou addresse (seulement pour ivy)')
    parser.add_argument('--length',default='3000', help='longueur du message à envoyer (3000 carac par défaut)')
    parser.add_argument('--log_level', default='FATAL', help='Niveau de configuration de la journalisation')
    parser.add_argument('--sleep',default='0',type = float, help="Temps du sleep à mettre entre l'envoi de chaque message")
    parser.add_argument('--flag', action='store_true', help="activer les flags pour simuler l'utilisation de regexp")
    parser.add_argument('--flag_count', default = 1, type=int, help='Nombre de flags à envoyer')
    parser.add_argument('--receive', action='store_true', help="executer en tant que receveur")
    parser.add_argument('--send', action='store_true', help="executer en tant que sender")
    parser.add_argument('--nbr_processes', default = 1, type=int, help='Nombre de receveurs créés')
    parser.add_argument('--direct_msg', action='store_true', help="envoyer des messages ivy avec ivydirectmsg")
    parser.add_argument('--device', default=None,help='nom du peripherique réseau utilisé pour ingescape')

#n

    param = parser.parse_args()


    # Configurer la journalisation
    logging.basicConfig(
        level=param.log_level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log',mode='w')
        ]
    )

    logger = logging.getLogger(__name__)
    multi_recv = False
    if param.nbr_processes != 1:
        multi_recv = True
   
    queue = multiprocessing.Queue()
    logger.info('Démarrage du programme')
    nmbre_rec= param.nbr_processes
    recv_processes=[]
    if not param.send and not param.receive:
        for i in range(nmbre_rec):
            receive_process = multiprocessing.Process(target=main_receive, args=(param.protocol, param.message_count, param.port,param.length, queue, logger, param.flag, i,param.nbr_processes, multi_recv,param.direct_msg, param.device))
            recv_processes.append(receive_process)
        send_process = multiprocessing.Process(target=main_send, args=(param.protocol, param.message_count, param.port, param.length, queue, logger, param.sleep, param.flag, param.flag_count, param.nbr_processes, param.direct_msg, param.device))
        for i in range(nmbre_rec):
            recv_processes[i].start()
        send_process.start()
        send_process.join()
        for i in range(nmbre_rec):
            receive_process.join()
    elif param.receive:
        for i in range(nmbre_rec):
            receive_process = multiprocessing.Process(target=main_receive, args=(param.protocol, param.message_count, param.port,param.length, queue, logger, param.flag, i,param.nbr_processes, multi_recv,param.direct_msg, param.device))
            recv_processes.append(receive_process)
        for i in range(nmbre_rec):
            recv_processes[i].start()
        for i in range(nmbre_rec):
            receive_process.join()
    elif param.send:
        send_process = multiprocessing.Process(target=main_send, args=(param.protocol, param.message_count, param.port, param.length, queue, logger, param.sleep, param.flag, param.flag_count, param.nbr_processes, param.direct_msg, param.device))
        send_process.start()
        send_process.join()        
    
    #sleep(2)



    logger.info('Fin du programme')
if __name__ == '__main__':
    main()
