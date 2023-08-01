import datetime
import re
import string
from time import sleep, time
import time
import matplotlib.pyplot as plt
from statistics import mean
import ivy.ivy
from abstract_protocol import AbstractProtocol


class MessageReceiver:
    def __init__(self, protocol_obj, bus, length=''):
        self.protocol_obj = protocol_obj
        self.bus = bus
        self.plt_data = []
        self.data = []
        self.length = length
        self.protocol = bus

    def draw_graph(self, protocole, message_count, multi_rec):

        plt.plot(range(1, message_count + 1), self.plt_data, 'ro')
        plt.xlabel('Message number')
        plt.ylabel('Time (s)')
        title = "temps individuels d'émission de " + str(message_count) + " messages de " + str(
            self.length) + " caractères avec " + str(protocole)
        plt.title(title, loc='center', wrap=True)
        if not multi_rec:
            print("La moyenne est ", mean(self.plt_data))
        chemin_dossier = "graphiques"
        nom_fichier = 'graph ' + str(self.bus) + ' ' + str(message_count) + 'msgs de ' + str(self.length) + ' carac.png'
        chemin_complet = chemin_dossier + "/" + nom_fichier
        plt.savefig(chemin_complet)  # Enregistre le graphique dans un fichier
        plt.close()  # Ferme la figure pour libérer les ressources

    def receive_messages(self, message_count, flag_count):
        return self.protocol_obj.receive_messages(message_count, flag_count)

    def analyze_messages(self):
        self.protocol_obj.stopsocket()
        print(self.data)
        print(len(self.data))

        # TODO: à déplacer dans XXX_protocol receive_messages
        if flag_count > 0:

            if self.protocol != "ivy":
                for i in range(message_count):
                    start_time = float(self.data[0][1].split("#")[1])

                    if self.data:

                        '''elements = message.split(" ")
                        elements.pop()
                        print(elements)
                        contenus = [element.split("=")[1].strip() for element in elements]
                        print(contenus)'''
                        pattern = ' '.join(f"flag{i}=(\\S*)" for i in range(10))
                        match = re.search(pattern, self.data[i][1])

                        if match:
                            values = match.groups()
                            values = values[:-1]
                            print(values)
                        else:
                            print("no match")
                        message, t0 = self.data[i][1].split("#")
                        t0 = float(t0)

                end_time = time.time()
                maintenant = datetime.datetime.now()
                # Formater la date et l'heure selon le format souhaité
                format_date_heure = "%d/%m/%Y %H:%M:%S"
                date_heure_formatee = maintenant.strftime(format_date_heure)
                print("Temps total de communication  : " + str(date_heure_formatee), (end_time - start_time))
            else:
                end_time = time.time()
                maintenant = datetime.datetime.now()
                # Formater la date et l'heure selon le format souhaité
                format_date_heure = "%d/%m/%Y %H:%M:%S"
                date_heure_formatee = maintenant.strftime(format_date_heure)
                print("Temps total de communication : " + str(date_heure_formatee), (end_time - start_time))
                # print("Temps total de communication : ", (end_time - float(self.data[0][-1])))



        else:
            start_time = float(self.data[0][1].split("#")[1])
            for i in range(message_count):
                if self.data:
                    t0 = float(self.data[i][1].split("#")[1])
                    time_interval = self.data[i][2] - t0
                    self.plt_data.append(time_interval)
            if multi_rec:
                # if(nmbre_rec == total_rec-1):
                maintenant = datetime.datetime.now()
                format_date_heure = "%d/%m/%Y %H:%M:%S"
                date_heure_formatee = maintenant.strftime(format_date_heure)
                # sleep(2)
                result = f"receiver_{str(nmbre_rec)}#{str(self.data[-1][2] - start_time)}"
                self.init_ivy(result)
                # print("Temps total de communication de tous les receveurs  au "+str(date_heure_formatee)+" : ", (self.data[-1][2] - start_time))
            else:
                maintenant = datetime.datetime.now()

                format_date_heure = "%d/%m/%Y %H:%M:%S"
                date_heure_formatee = maintenant.strftime(format_date_heure)
                sleep(1)
                print("Temps total de communication  au " + str(date_heure_formatee) + " : ",
                      (self.data[-1][2] - start_time))

            self.draw_graph(self.bus, message_count, multi_rec)
