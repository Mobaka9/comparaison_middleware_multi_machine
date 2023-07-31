import datetime
import re
import string
from time import sleep, time
import time
import matplotlib.pyplot as plt
from statistics import mean
import ivy.ivy


class MessageReceiver:
    def __init__(self, protocol_obj, bus, length):
        self.protocol_obj = protocol_obj
        self.bus = bus
        self.plt_data = []
        self.data=[]
        self.length = length
        self.protocol = bus
    
    
    def draw_graph(self, protocole, message_count, multi_rec):
        
        plt.plot(range(1, message_count+1), self.plt_data, 'ro')
        plt.xlabel('Message number')
        plt.ylabel('Time (s)')
        title = "temps individuels d'émission de "+str(message_count)+" messages de "+str(self.length)+" caractères avec "+str(protocole)
        plt.title(title, loc='center', wrap=True)
        if not multi_rec:
            print("La moyenne est ", mean(self.plt_data))
        chemin_dossier = "graphiques"
        nom_fichier = 'graph '+str(self.bus)+' '+str(message_count)+'msgs de '+str(self.length)+' carac.png'
        chemin_complet = chemin_dossier + "/" + nom_fichier
        plt.savefig(chemin_complet)  # Enregistre le graphique dans un fichier
        plt.close()  # Ferme la figure pour libérer les ressources

        
    def receive_messages(self, message_count, queue, flag,nmbre_rec,total_rec, multi_rec,direct_msg):
            self.data = self.protocol_obj.receive_message(message_count,queue,total_rec,direct_msg,flag)
            self.protocol_obj.stopsocket()
            print(self.data)
            print(len(self.data))

            if(flag):
                if self.protocol != "ivy":
                    for i in range(message_count):
                        start_time = float(self.data[0][1].split("#")[1])

                        if self.data : 
                            
                            '''elements = message.split(" ")
                            elements.pop()
                            print(elements)
                            contenus = [element.split("=")[1].strip() for element in elements]
                            print(contenus)'''
                            pattern = r'flag0=(\S*) flag1=(\S*) flag2=(\S*) flag3=(\S*) flag4=(\S*) flag5=(\S*) flag6=(\S*) flag7=(\S*) flag8=(\S*) flag9=(\S*) flag10=(\S*) flag11=(\S*) flag12=(\S*) flag13=(\S*) flag14=(\S*) flag15=(\S*) flag16=(\S*) flag17=(\S*) flag18=(\S*) flag19=(\S*) flag20=(\S*) flag21=(\S*) flag22=(\S*) flag23=(\S*) flag24=(\S*) flag25=(\S*) flag26=(\S*) flag27=(\S*) flag28=(\S*) flag29=(\S*) flag30=(\S*) flag31=(\S*) flag32=(\S*) flag33=(\S*) flag34=(\S*) flag35=(\S*) flag36=(\S*) flag37=(\S*) flag38=(\S*) flag39=(\S*) flag40=(\S*) flag41=(\S*) flag42=(\S*) flag43=(\S*) flag44=(\S*) flag45=(\S*) flag46=(\S*) flag47=(\S*) flag48=(\S*) flag49=(\S*) flag50=(\S*) flag51=(\S*) flag52=(\S*) flag53=(\S*) flag54=(\S*) flag55=(\S*) flag56=(\S*) flag57=(\S*) flag58=(\S*) flag59=(\S*) flag60=(\S*) flag61=(\S*) flag62=(\S*) flag63=(\S*) flag64=(\S*) flag65=(\S*) flag66=(\S*) flag67=(\S*) flag68=(\S*) flag69=(\S*) flag70=(\S*) flag71=(\S*) flag72=(\S*) flag73=(\S*) flag74=(\S*) flag75=(\S*) flag76=(\S*) flag77=(\S*) flag78=(\S*) flag79=(\S*) flag80=(\S*) flag81=(\S*) flag82=(\S*) flag83=(\S*) flag84=(\S*) flag85=(\S*) flag86=(\S*) flag87=(\S*) flag88=(\S*) flag89=(\S*) flag90=(\S*) flag91=(\S*) flag92=(\S*) flag93=(\S*) flag94=(\S*) flag95=(\S*) flag96=(\S*) flag97=(\S*) flag98=(\S*) flag99=(\S*) flag100=(\S*) flag101=(\S*) flag102=(\S*) flag103=(\S*) flag104=(\S*) flag105=(\S*) flag106=(\S*) flag107=(\S*) flag108=(\S*) flag109=(\S*) flag110=(\S*) flag111=(\S*) flag112=(\S*) flag113=(\S*) flag114=(\S*) flag115=(\S*) flag116=(\S*) flag117=(\S*) flag118=(\S*) flag119=(\S*) flag120=(\S*) flag121=(\S*) flag122=(\S*) flag123=(\S*) flag124=(\S*) flag125=(\S*) flag126=(\S*) flag127=(\S*) flag128=(\S*) flag129=(\S*) flag130=(\S*) flag131=(\S*) flag132=(\S*) flag133=(\S*) flag134=(\S*) flag135=(\S*) flag136=(\S*) flag137=(\S*) flag138=(\S*) flag139=(\S*) flag140=(\S*) flag141=(\S*) flag142=(\S*) flag143=(\S*) flag144=(\S*) flag145=(\S*) flag146=(\S*) flag147=(\S*) flag148=(\S*) flag149=(\S*) flag150=(\S*) flag151=(\S*) flag152=(\S*) flag153=(\S*) flag154=(\S*) flag155=(\S*) flag156=(\S*) flag157=(\S*) flag158=(\S*) flag159=(\S*) flag160=(\S*) flag161=(\S*) flag162=(\S*) flag163=(\S*) flag164=(\S*) flag165=(\S*) flag166=(\S*) flag167=(\S*) flag168=(\S*) flag169=(\S*) flag170=(\S*) flag171=(\S*) flag172=(\S*) flag173=(\S*) flag174=(\S*) flag175=(\S*) flag176=(\S*) flag177=(\S*) flag178=(\S*) flag179=(\S*) flag180=(\S*) flag181=(\S*) flag182=(\S*) flag183=(\S*) flag184=(\S*) flag185=(\S*) flag186=(\S*) flag187=(\S*) flag188=(\S*) flag189=(\S*) flag190=(\S*) flag191=(\S*) flag192=(\S*) flag193=(\S*) flag194=(\S*) flag195=(\S*) flag196=(\S*) flag197=(\S*) flag198=(\S*) flag199=(\S*) #(\S*)'
                            match = re.search(pattern, self.data[i][1])
                            
                            if match:
                                values = match.groups()
                                values = values[:-1]
                                print(values)
                            else:
                                print("no match")
                            message, t0 = self.data[i][1].split("#")
                            t0= float(t0)
                    
                    end_time=time.time()
                    maintenant = datetime.datetime.now()
                    # Formater la date et l'heure selon le format souhaité
                    format_date_heure = "%d/%m/%Y %H:%M:%S"
                    date_heure_formatee = maintenant.strftime(format_date_heure)
                    print("Temps total de communication  : "+str(date_heure_formatee), (end_time - start_time))
                else:
                    end_time=time.time()
                    maintenant = datetime.datetime.now()
                    # Formater la date et l'heure selon le format souhaité
                    format_date_heure = "%d/%m/%Y %H:%M:%S"
                    date_heure_formatee = maintenant.strftime(format_date_heure)
                    print("Temps total de communication : "+str(date_heure_formatee), (end_time - start_time))
                    #print("Temps total de communication : ", (end_time - float(self.data[0][-1])))

                    

            else: 
                start_time = float(self.data[0][1].split("#")[1])
                for i in range(message_count):
                    if self.data : 
                        t0 = float(self.data[i][1].split("#")[1]) 
                        time_interval = self.data[i][2] - t0
                        self.plt_data.append(time_interval)
                if multi_rec:
                    # if(nmbre_rec == total_rec-1):
                        maintenant = datetime.datetime.now()
                        format_date_heure = "%d/%m/%Y %H:%M:%S"
                        date_heure_formatee = maintenant.strftime(format_date_heure)
                        #sleep(2)
                        result=f"receiver_{str(nmbre_rec)}#{str(self.data[-1][2] - start_time)}"
                        self.init_ivy(result)
                        # print("Temps total de communication de tous les receveurs  au "+str(date_heure_formatee)+" : ", (self.data[-1][2] - start_time))
                else:
                    maintenant = datetime.datetime.now()

                    format_date_heure = "%d/%m/%Y %H:%M:%S"
                    date_heure_formatee = maintenant.strftime(format_date_heure)
                    sleep(1)
                    print("Temps total de communication  au "+str(date_heure_formatee)+" : ", (self.data[-1][2] - start_time)) 



                self.draw_graph(self.bus, message_count, multi_rec) 

    def init_ivy(self,resultat):
        
            IVYAPPNAME="Result_sender"
            sivybus = ''
            sisreadymsg = f"ready {IVYAPPNAME}"                              
            def lprint(fmt, *arg):

                print(fmt % arg)

                
            def usage(scmd):
                lpathitem = string.split(scmd, '/')
                fmt = '''Usage: %s [-h] [-b IVYBUS | --ivybus=IVYBUS]
                where
                \t-h provides the usage message;
                \t-b IVYBUS | --ivybus=IVYBUS allow to provide the IVYBUS string in the form
                \t adresse:port eg. 127.255.255.255:2010
                '''
                print(fmt % lpathitem[-1])
            
            def oncxproc(agent, event_type):
                if event_type == IvyApplicationDisconnected:
                    lprint('Ivy application %r was disconnected', agent)
                else:
                    lprint('Ivy application %r was connected', agent)

                lprint('currents Ivy application are [%s]', IvyGetApplicationList())


            def ondieproc(agent, _id):
                lprint('received the order to die from %r with id = %d', agent, _id)

                    
            
            broadcast = self.args.split(":")
            port1=int(broadcast[1])
            sechoivybus = broadcast[0]+":"+str(port1+1)
            
            lprint('Ivy will broadcast on %s ', sechoivybus)

                # initialising the bus
            IvyInit(IVYAPPNAME,     # application name for Ivy
                    sisreadymsg,    # ready message
                    0,              # main loop is local (ie. using IvyMainloop)
                    oncxproc,       # handler called on connection/disconnection
                    ondieproc)      # handler called when a <die> message is received
            IvyStart(sechoivybus)
            sleep(2)
            IvySendMsg
            (resultat)
                