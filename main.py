import argparse
import logging
import multiprocessing
from main_send import main_send
from main_receive import main_receive


def start_receivers(protocol, message_count, port, regexp_match_count, nmbre_rec, ivybus_test_manager):
    recv_processes = []
    for i in range(nmbre_rec):
        receive_process = multiprocessing.Process(target=main_receive, args=(
            protocol, message_count, port, regexp_match_count, i, ivybus_test_manager))
        recv_processes.append(receive_process)
        recv_processes[i].start()

    return recv_processes


def start_sender_and_wait(protocol, message_count, port, length, sleep, flag_count, nbr_processes,
                          device, ivybus_test_manager):
    send_process = multiprocessing.Process(target=main_send, args=(
        protocol, message_count, port, length, sleep, flag_count, nbr_processes, device, ivybus_test_manager))
    send_process.start()
    send_process.join()


def main(nmbre_rec, protocol, message_count, port, length, flag_count, direct_msg, device,
         sleep, send_only, receive_only, ivybus_test_manager):
    logging.info('Démarrage du programme')

    if not send_only and not receive_only:
        recv_procs = start_receivers(protocol, message_count, port, flag_count,
                                     nmbre_rec, ivybus_test_manager)
        start_sender_and_wait(protocol, message_count, port, length, sleep, flag_count, nmbre_rec,
                              device, ivybus_test_manager)
        for proc in recv_procs:
            proc.join()

    elif receive_only:
        recv_procs = start_receivers(protocol, message_count, port, flag_count,
                                     nmbre_rec, ivybus_test_manager)
        for proc in recv_procs:
            proc.join()

    elif send_only:
        start_sender_and_wait(protocol, message_count, port, length, sleep, flag_count, nmbre_rec,
                              device, ivybus_test_manager)

    logging.info('Fin du programme')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Envoi de messages entre 2 terminaux avec 3 middleware', add_help=True)
    parser.add_argument('--protocol', help='Protocole à utiliser (ivy, zeromq, kafka)')
    parser.add_argument('--message_count', default=1, type=int, help='Nombre de messages à envoyer')
    parser.add_argument('--port', help='Port ou addresse (seulement pour ivy)')
    parser.add_argument('--length', default='3000', help='longueur du message à envoyer (3000 carac par défaut)')
    parser.add_argument('--log_level', default='FATAL', help='Niveau de configuration de la journalisation')
    parser.add_argument('--sleep', default='0', type=float,
                        help="Temps du sleep à mettre entre l'envoi de chaque message")
    parser.add_argument('--flag_count', default=0, type=int, help='Nombre de flags à envoyer')
    parser.add_argument('--receive', action='store_true', help="executer en tant que receveur")
    parser.add_argument('--send', action='store_true', help="executer en tant que sender")
    parser.add_argument('--nbr_receivers', default=1, type=int, help='Nombre de receveurs créés')
    parser.add_argument('--direct_msg', action='store_true', help="envoyer des messages ivy avec ivydirectmsg")
    parser.add_argument('--device', default=None, help='nom du peripherique réseau utilisé pour ingescape')
    parser.add_argument('--ivybus_test_manager', default='10.34.127.255:1111', help='ivy bus pour la synchro des tests')
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

    main(nmbre_rec=param.nbr_receivers,
         protocol=param.protocol,
         message_count=param.message_count,
         port=param.port,
         length=param.length,
         flag_count=param.flag_count,
         direct_msg=param.direct_msg,
         device=param.device,
         sleep=param.sleep,
         send_only=param.send,
         receive_only=param.receive,
         ivybus_test_manager=param.ivybus_test_manager
         )
