from asyncio.windows_events import NULL
import socket
from PyQt5 import QtWidgets, uic
import sys
import sqlite3
import os
import threading
import pyautogui
import multiprocessing
from vidstream import StreamingServer

from vidstream import ScreenShareClient
from vidstream import AudioSender
from vidstream import AudioReceiver
from datetime import datetime
import cv2
import pyscreeze
import time
import sys
from vidstream import VideoClient
import numpy as np
from PyQt5.QtWidgets import QFileDialog, QDialog
from re import T
from vidstream import CameraClient

from videoshare import diffuser_moi

 
 


p=QtWidgets.QApplication(sys.argv)
global interface
interface=uic.loadUi("interface.ui")
global send_audio
global receiver_audio
global con
global Monsocket
global Mon_nom
global sorti
global local_f
global con1
global Monsocket1
global Nom_destinateur
global ip_server
global thread_serveur_video
global thread_client_video
global thread_client_audio
global thread_serveur_audio
global ETAT
ETAT=0
global local_cl
global port_c
global thread_envoyer_vocal
global thread_recevoir_vocal
thread_envoyer_vocal=NULL
thread_recevoir_voca=NULL
ip_server=""
Mon_nom="Zoulngarnaini"
Nom_destinateur=""


#fonctions d'envoi
def envoyer_alerte(conf):
    if(ETAT==1):
        con.send(conf.encode('utf8'))
    else:
        Monsocket.send(conf.encode('utf8'))
# serveur de partage d'ecran
def lancer_serveur_ap_video():
        
            local=""
            port=5002
            ports=4002
            ##
            try:
                recevoir_appel_video=StreamingServer(local,port)
                vocalrecevoir_appel_v=AudioReceiver(local,ports)
                thread_serveur_audio=threading.Thread(target=vocalrecevoir_appel_v.start_server)
                #
                thread_serveur_video=threading.Thread(target=recevoir_appel_video.start_server)
                thread_serveur_audio.start()
                thread_serveur_video.start()
                interface.arreter_video_call.setText(str("STOP"))
                interface.arreter_video_call.setHidden(False)
                print("Active")
                while (interface.arreter_video_call.text()=="STOP"):
                    continue
                recevoir_appel_video.stop_server()
                vocalrecevoir_appel_v.stop_server()
            except:
                 pyautogui.alert(" Une erreur est survenue")

##
def lancer_envoi_ap_video():
    port=5002
    ports=4002
    try:
        ar_s=ip_server
        envoyer=CameraClient(ar_s,port)
        thread_client_video=threading.Thread(target=envoyer.start_stream)
        
        #
        vocalsend=AudioSender(ar_s,ports)
        thread_client_audio=threading.Thread(target=vocalsend.start_stream)
        #
        thread_client_video.start()
        thread_client_audio.start()
        interface.arreter_video_call.setText(str("STOP"))
        interface.arreter_video_call.setHidden(False)
        print("client en cours")
        while interface.arreter_video_call.text()=="STOP":
            continue

        envoyer.stop_stream()
        vocalsend.stop_stream()
        pyautogui.alert("Fin dappel video ")
    except:
        pyautogui.alert(" Une erreur s'est produit veuillez reessayer")
    


##
#appel vocal
def racrocher_vocal():  
        try: 
          interface.stop_vocal.setText("STOPPER")
        except:
            pyautogui.alert("Une erreur est survenue")
        finally:
            return
            
def recevoir_appel_vocal():
    try:
        port= 8000
        global thread_serveur_audio
        
        global receiver_audio
        receiver_audio=AudioReceiver("192.168.56.1",port)
        thread_serveur_audio=threading.Thread(target=receiver_audio.start_server)
        thread_serveur_audio.start()
        print("serveur demarre sur 8000")
        interface.stop_vocal.setHidden(False)
        interface.stop_vocal.setText(str("STOP"))
        while (interface.stop_vocal.text()=="STOP"):
            continue
        receiver_audio.stop_server()
    except:
        pyautogui.alert(" Une s'est produit veuillez reessayer")
def envoyer_appel_vocal():
    port= 8000
    global thread_client_audio
    send_audio=AudioSender(ip_server,port)
    thread_client_audio=threading.Thread(target=send_audio.start_stream)
    thread_client_audio.start()
    print("client connecte au vocal")
    interface.stop_vocal.setText("STOP")
    interface.stop_vocal.setHidden(False)
    while (interface.stop_vocal.text()=="STOP"):
        continue
    #
    send_audio.stop_stream()

###Transfert des fichiers
def client_file_transfert():
    global Monsocket1
    Monsocket1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port=9990
    try:
        Monsocket1.connect((ip_server,port))
        receptc=threading.Thread(target=recv_file_client)
        receptc.start()
    except socket.error as er:
        print(er)
#
def send_file_client():
     NAME_FI=interface.zone_name_file.text()
     DN=NAME_FI.split("/")
     long=len(DN)
     print(long)

     f=DN[long-1]
     f_size=os.path.getsize(NAME_FI)
     val=str(f_size)+",b"
     Monsocket1.send(f.encode('utf8'))
     Monsocket1.send(val.encode('utf8')) 
     with open(NAME_FI,"rb") as file:
         pr=0
         interface.zone_progression.setText(str(f" envoi de {f}: {pr}%"))
         c=0
         while c<int(f_size):
             data=file.read()
             Monsocket1.sendall(data)
             c=c+len(data)
             if not data:
                 break
             #pr=(c/f_size)*100
             interface.zone_progression.setText(str(f" envoi de {f}: {pr}%"))
         interface.zone_progression.setText(str(f" envoi de {f} termine..."))
def recv_file_client():
    
    try:
         
         f=Monsocket1.recv(1024).decode('utf8')
         f_size1=Monsocket1.recv(1024).decode('utf8')
         f_sizef=f_size1.split(",")
         f_size=f_sizef[0]
         with open("file_transfert/"+f,"wb") as file:
             pr=0
             interface.zone_progression.setText(str(f" Reception de {f}: {pr}%"))
             c=0
             while c<int(f_size):
                 data=Monsocket.recv(1024)
                 c=c+len(data)
                 if not data:
                     break
                 data=file.write(data)
                 #pr=(c/f_size)*100
                 interface.zone_progression.setText(str(f" Reception de {f}: {pr}%"))
              
             interface.zone_progression.setText(str(f" Reception de {f} termine.."))
    except:
        print("erreur de reception")

def recv_file_server():
     try:
         f=con1.recv(1024).decode('utf8')
         f_size1=con1.recv(1024).decode('utf8')
         f_sizef=f_size1.split(",")
         f_size=f_sizef[0]
         with open("file_transfert/"+f,"wb") as file:
             pr=0
             print(f" Debut de reception...{f}")
             c=0
             while c<int(f_size):
                 interface.zone_progression.setText(str(f" Reception de {f}: {pr}%"))
                 data=con1.recv(1024)
                 c=c+len(data)
                 if not data:
                     break
                 data=file.write(data)
                 #pr=(c/f_size)*100
                 interface.zone_progression.setText(str(f" Reception de {f}: {pr}%"))
             print("Fin de reception")
             interface.zone_progression.setText(str(f" Reception de {f} termine."))
     except:
         print("Erreur de reception")

def send_file_server():
     NAME_FI=interface.zone_name_file.text()
     DN=NAME_FI.split("/")
     long=len(DN)

     f=DN[long-1]
     f_size=os.path.getsize(NAME_FI)
     val=str(f_size)+",b"
     con1.send(f.encode('utf8'))
     con1.send(val.encode('utf8')) 
     with open(NAME_FI,"rb") as file:
         print(f" Debut d\'envoi...{f}" )
         pr=0
         interface.zone_progression.setText(str(f" envoi de {f} {pr}%"))
         c=0
         
         while c<int(f_size):
             data=file.read()
             con1.sendall(data)
             c=c+len(data)
             if not data:
                 break
             #pr=(c/f_size)*100
             interface.zone_progression.setText(str(f" envoi de {f} {pr}%"))
         interface.zone_progression.setText(str(f" envoi de {f} en termine..."))

def server_file_transfert():
        local=""
        port=9990  
        try:
            global con1
            global local_f
            connex=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            connex.bind((local,port))
            connex.listen(1)
            con1,(ip,port)=connex.accept()
            recept=threading.Thread(target=recv_file_server)
            recept.start()
        except socket.error as e:
            print(e)
def send_file_file():
    if(interface.zone_name_file.text()==""):
        pyautogui.alert("Selectionner un fichier s'il vous plait")
        return
    else:
        if(ETAT==0):
            pyautogui.alert(" Veuillez vous connectez d'abord s'il vous plait")
            return activation_bouton_connexion()
        else:
            NAME_FI=interface.zone_name_file.text()
            if(ETAT==1):
                send_file_server()
            else:
                send_file_client()

##fin des fonctions de transfert de fichier



#Sauvegarde
def inseremoi_serveur_socket(Monsocket,local,port):
    try:
        requ=f"INSERT INTO client (Monsocket)values(\"{Monsocket}\")"
        conbase=sqlite3.connect("donnees.db")
        curseur=conbase.cursor()
        donnee=curseur.execute(requ)
        conbase.commit()
        conbase.close()
    except sqlite3.Error as e:
        print(" Erreur d'enregistrement du socket ",e)
def connexion_au_serveur():
    requ="SELECT Monsocket FROM client"
    conbase=sqlite3.connect("donnees.db")
    curseur=conbase.cursor()
    donnee=curseur.execute(requ)
    donnee=donnee.fetchone()
    conbase.close()
    return donnee

#boutton d'activation du l'ecran    
#Envoie de message en tant que client
def client_envoyer():
    H=interface.z_saisir.text()
    Monsocket.send(H.encode("utf8"))
    interface.z_envoyer.setText(str(H))
    interface.z_saisir.setText(str(""))
##Reception en tant que client
def client_recevoir():
    continuer=1

    while continuer:
        try:
            T=Monsocket.recv(1024).decode("utf8")
            tester_mot_recu(T)
        except:
            
            Monsocket.close()
            ETAT=0
            continuer=0
            pyautogui.alert(" Le client vient de se deconnecter")
        
## fonctions chargees d'affichage des messages et assurant les declenchements des 
###fonctionnalites

def tester_mot_recu(T)   :   
        if(T=="JE_SUIS_PRET_A_RECEVOIR_TON_ECRAN"):
                screen_client()

        elif(T=="JE_VEUX_PARTAGER_UN_FICHIER"):
            MSG="JE_SUIS_PRET_A_RECEVOIR_UN_FICHIER"
            
            if(ETAT==1):
                recv_file_server()
                envoyer_alerte(MSG)
            else:
                recv_file_client()
                envoyer_alerte(MSG)
        elif(T=="JE_SUIS_PRET_A_RECEVOIR_UN_FICHIER"):
            if(ETAT==1):
                send_file_server()
            else:
                send_file_client()
        elif(T=="JE_VEUX_VOIR_LA_DIFFUSION"):
            try:
                mathread=threading.Thread(target=diffuser_moi)
                mathread.start()
                
            except:
                pyautogui.alert(" Une erreur s'est produite")

        elif(T=="UNE_VIDEO_A_PARTAGER"):
            interface.diffusion_video_disponible.setText(str(" Video de diffusion disponible"))
        elif(T=="JE_VEUX_PARTAGER_MON_ECRAN"):
                 info= " ECRAN DE "+Nom_destinateur+" Disponible"
                 alerte_disponible(info)
        elif(T=="ARRETER_APPEL_VOCAL_EN COURS_E"):
              #send_audio.stop_stream()
              pass
        elif(T=="ARRETER_APPEL_VOCAL_EN COURS_R"):
            receiver_audio.stop_server()

        elif(T=="JE_SUIS_PRET_A_RECEVOIR_APPEL_VIDEO"):
            time.sleep(2)
            t5=threading.Thread(target=lancer_envoi_ap_video)
            t5.start()

            t6=threading.Thread(target=lancer_serveur_ap_video)
            t6.start()
            

        elif(T=="JE_VEUX_FAIRE_UN_APPEL_VIDEO"):
            confir=pyautogui.confirm(text=" Vous avez un appel video entrant",buttons=['Accepter','Rejetter'])
            if(confir=="Accepter"):
                conf="JE_SUIS_PRET_A_RECEVOIR_APPEL_VIDEO"
                envoyer_alerte(conf)
                t2=threading.Thread(target=lancer_serveur_ap_video)
                t2.start()
                time.sleep(3)
                t5=threading.Thread(target=lancer_envoi_ap_video)
                t5.start()
                
                
                
            else:
                conf="APPEL_VIDEO_REJETTER"
                if(ETAT==1):
                    con.send(conf.encode('utf8'))
                else:
                    Monsocket.send(conf.encode('utf8'))
                if(ETAT==1):
                    con.send(conf.encode('utf8'))

                return 
               
        elif(T=="JE_SUIS_PRET_A_RECEVOIR_APPEL"):
                #time.sleep(3)
                try:
                    thread_envoyer_vocal=threading.Thread(target=envoyer_appel_vocal)
                    thread_envoyer_vocal.start()
                    #time.sleep(1)
                    thread_recevoir_vocal=threading.Thread(target=recevoir_appel_vocal)
                except:
                    return
                
                
        elif(T=="JE_VEUX_EMETTRE_UN_APPEL_VOCAL"):
              choix=pyautogui.confirm(text="VOUS_AVEZ_UN_APPEL_ENTRANT",buttons=['Accepter','Refuser'])
              if(choix=="Accepter"):
                appel="JE_SUIS_PRET_A_RECEVOIR_APPEL"
                try:
                    thread_recevoir_vocal=threading.Thread(target=recevoir_appel_vocal)
                    thread_recevoir_vocal.start()
                    envoyer_alerte(appel)
                    time.sleep(3)
                    thread_envoyer_vocal=threading.Thread(target=envoyer_appel_vocal)
                    thread_envoyer_vocal.start()
                except:
                    return

                
              else :
                 appel="APPEL_VOCAL_REFFUSE"
                 envoyer_alerte(appel)
               
        elif(T=="FIN_CONNEXION"):
            if(ETAT==1):
                fermer_serveur()
            else:
                changer_ETAT_cl()
        elif(T=="APPEL_VOCAL_REFFUSE"):
            try:
                 interface.appel_V.setText("APPEL VOCAL")
                 interface.bt__rejetter_V.setText("APPEL VOCAL REJETTE ")
            except :   
                return
        else:
                 interface.z_recevoir.setText(str(T))
                 
             
def   fermer_serveur():
    con.close()
    con1.close()
#partie l'affichage du nom et l'adresse de l'utilisateur
#se connecter a un serveur
def changer_ETAT_cl():
    global ETAT
    Monsocket.close()
    Monsocket1.close()
    ETAT=0
def se_connecter_v():
     if(ETAT==2):
            verif=pyautogui.confirm(text=" Voulez vraiment vous deconnecter?", buttons=['Oui','Annuler'])
            if(verif=="Oui"):
                try:
                    envoyer_alerte("FIN_CONNEXION")
                    Monsocket.close()
                    Monsocket1.close()
                    changer_ETAT_cl()
                    return
                except:
                    return
            else:
                return
     else:
        se_connecter()

def se_connecter():  
   
        try:
            global Monsocket
            local=pyautogui.prompt(" Entrez l'adresse du serveur ")
            if(local==""):
                local="127.0.0.1"
            global ip_server
            ip_server=local
            port= 9984
            Monsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            Monsocket.connect((local,port))
            client_file_transfert()
            global ETAT
            ETAT=2
            print("\n La Machine est connectee sur",local,"port ",port )
            interface.z_adresse.setText(str(local))
            interface.ip_serveur.setText(str(local))
            Monsocket.send(Mon_nom.encode('utf8'))
            Nom_destinateur=Monsocket.recv(1024).decode('utf8')
            interface.Mon_nom.setText(str(Nom_destinateur))
            interface.creer_client.setText(str("Client connecte"))
            inseremoi_serveur_socket(Monsocket,local,port)
            T1=threading.Thread(target=client_recevoir)
            T1.start()  
        except socket.error as e:
            interface.z_adresse.setText(str(e))



#partie messagerie
# serveur
def connexion_au_client():
    requ="SELECT con FROM serveur"
    conbase=sqlite3.connect("donnees.db")
    curseur=conbase.cursor()
    donnee=curseur.execute(requ)
    donnee=donnee.fetchone()
    return donnee
# Serveur envoie les messages
def ser_envoyer():
    
    try:
        H=interface.z_saisir.text()
        con.sendall(H.encode('utf8'))
        interface.z_envoyer.setText(str(H))
        interface.z_saisir.setText(str("")) 
    except:
        return
##serveur recoit ses messages
def ser_recevoir():
    try:
        while ETAT==1:
            T=con.recv(1024).decode('utf8')
            tester_mot_recu(T)
        con.close()
    except:
        return
 
##creation du serveur

def creer_serveur():
    local=""
    port= 9984
    def accepter():
        try:
            F=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            F.bind((local,port))
            try:
                interface.creer_serveur.setText(str("Serveur en ecoute"))
                F.listen(1)
                print("serveur en cours execution")
                global con
                global local_cl
                global port_cl
                global ip_server
                (con, (local_cl,port_cl))=F.accept()
                global ETAT
                ETAT=1
                ip_server=local_cl
                #
                server_file_transfert()
                #
                try:
                
                    Nom_destinateur=con.recv(1024).decode('utf8')
                    con.send(Mon_nom.encode('utf8'))  
                    interface.Mon_nom.setText(str(Nom_destinateur))
                    interface.z_adresse.setText(str(local_cl))
                    interface.ip_client.setText(str(local_cl))
                    interface.creer_serveur.setText(str("Serveur connecte"))
                    T1=threading.Thread(target=ser_recevoir)
                    T1.start()
                    
                    
            
                except socket.error as e:
                    pyautogui.alert(" Erreur survenue lors de la creation du serveur ", e)
                    return
            except:
                pyautogui.alert(f" Une erreur est survenue assurez que le port {port_cl} n'est utilise par aucun processus")
                return
        except:
            pyautogui.alert(" Une erreur est survenue")
            return
    t_thread=threading.Thread(target=accepter)
    t_thread.start() 


# partager de  l'ecran
def lancer_s():
    interface.arreter_video_call.setHidden(False)
    interface.arreter_video_call.setText(str("STOP"))
    try:
        ip=""
        print(ip)
        port=8888
        interface.screen_recevoir.setHidden(False)
        rec=StreamingServer("",port)
        t1=threading.Thread(target=rec.start_server)
        interface.arreter_video_call.setHidden(False)
        t1.start()
        print("Serveur screen a demarer sur le port ",port)
        while (interface.arreter_video_call.text()=="STOP")  :
            continue
        rec.stop_server()
        interface.arreter_video_call.setHidden(True)
    except:
        pyautogui.alert(" Une erreur s'est produit veuillez vous assurez \n que le serveur est bien bien connecte")
#fonctions 
           
def screenServ():
    
    Mon_signal="JE_SUIS_PRET_A_RECEVOIR_TON_ECRAN"
    if(ETAT==0):
       pyautogui.alert(" Veuillez vous connecter d'abord")
       return
    try:
        envoyer_alerte(Mon_signal)
        def lancer_s():
            try:
                ip=""
                port=8888
                interface.screen_recevoir.setHidden(False)
                rec=StreamingServer(ip,port)
                t1=threading.Thread(target=rec.start_server)
                interface.screen_recevoir.setHidden(False)
                t1.start()
                interface.arreter_video_call.setHidden(False)
                interface.arreter_video_call.setText(str("STOP"))
                print("Serveur screen a demarer sur le port ",port)
                while (interface.arreter_video_call.text()=="STOP"):
                    
                        continue
                rec.stop_server()
                interface.arreter_video_call.setHidden(True)
            except:
                return

        t_serv=threading.Thread(target=lancer_s)
        t_serv.start()
    except:
        pyautogui.alert(" Une erreur est survenue veuillez reessayez")
    

# Transferer mon ecran
def activer_monpartage_ecran():
   if(ETAT==0):
       pyautogui.alert(" Vous devez vous connectez d\'abord")
       return
   if(interface.Desactiver.text()!="ACTIVER"):
   
        Mon_signal="JE_VEUX_PARTAGER_MON_ECRAN"
        envoyer_alerte(Mon_signal)
      
        interface.Desactiver.setText(str("ACTIVER"))         
        
   else:
      interface.Desactiver.setText(str("DESACTIVER"))
      return
#notification qu'un ecran est disponible

def alerte_disponible(info):
   interface.Machine_disponible.setText(str(info))
# fonctions de partage d'ecran
def screen_client():
    try:
        port=8888
        sen=ScreenShareClient(ip_server,port)
        t2=threading.Thread(target=sen.start_stream)
        interface.screen_recevoir.setText(str("STOP"))
        interface.screen_recevoir.setHidden(False)
        t2.start()
        while (interface.Desactiver.text()!='DESACTIVER'):
            continue
        sen.stop_stream()
    except:
        pyautogui.alert(" Une erreur est survenue")
## Enregistrement de son ecran de travail
def lancer_dif():
    t1=threading.Thread(target=serveur_diffuser)
    t1.start()
    envoyer_alerte("JE_VEUX_VOIR_LA_DIFFUSION")

def serveur_diffuser():
    ser=StreamingServer('192.168.173.1',9010)
    t2=threading.Thread(target=ser.start_server)
    t2.start()
    print("Serveur en cours")
    interface.diffusion_en_c.setHidden(False)
    interface.arreter_diffusion.setHidden(False)
    interface.arreter_diffusion.setText(str("ARRETER"))
    
    while (interface.arreter_diffusion.text()=="ARRETER"):
        continue
    ser.stop_server()
    pyautogui.alert(" Fin de la video de la reception")
    
def diffuser_moi():
    
    name_f=interface.name_file_to_broad.text()
    if (name_f!=""):
        try:
            client=VideoClient(ip_server,9010,name_f)
            t1=threading.Thread(target=client.start_stream)
            t1.start()
            print("client en cours dif")
            while True:
                continue
            client.stop_stream()
            pyautogui.alert(" Fin de la video de la reception")
        except:
            pyautogui.alert("Une erreur est survenu")
            return
    else:
        return
def go_to_diffusion():
    try:
        if(ETAT==0):
            pyautogui.alert("Veuillez vous connecter d'abord!!!")
            return
        if(interface.name_file_to_broad.text()!=""):
           envoyer_alerte("UNE_VIDEO_A_PARTAGER")
        else:
            return
    except:
        return
def capturebureau():
    reslt=pyautogui.size()
    fps=15.0
    dt=str(datetime.now())
    dt=dt.split(".")
    print(dt[0])
    filenm = "screen_recorder/Ecran.avi"
    img=pyautogui.screenshot()
    codec= cv2.VideoWriter_fourcc('M','P','4','V')
    global sorti
    sorti=cv2.VideoWriter(filenm,codec,fps,reslt)
    x=1
    c=pyautogui.confirm('Voulez allez enregistrement l ecran de votre espace de travail')
    if c=="OK":
            interface.Arreter_enreg_bureau.setHidden(False)
            interface.en_cours_bur.setText(" En cours ...")
            while True:
                img = pyautogui.screenshot()
                frame= np.array(img)
                frame= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                sorti.write(frame);
            

  	
def initialiseur_ap_vid():
    if (ETAT==0):
        pyautogui.alert(" Veuillez vous connectez d'abord")
        return
    else:
        ALERTE="JE_VEUX_FAIRE_UN_APPEL_VIDEO"
        envoyer_alerte(ALERTE)
def arret_dif():
    interface.arreter_diffusion.setText(str("STOP"))
    return
## Arreter l'enregistrement d'ecran

def destroy_bureau():
        sorti.release() 
        interface.en_cours_bur.setText("")
        interface.Arreter_enreg_bureau.setHidden(True)
#         


def initialisation_bd():
   try:
        con=sqlite3.connect("donnees.db")
        curseur=con.cursor()
        requ1="CREATE TABLE IF NOT EXISTS serveur(id integer PRIMARY KEY AUTOINCREMENT,con VARCHAR,local_cl VARCHAR,port VARCHAR,name_user VARCHAR)"
        requ2="CREATE TABLE IF NOT EXISTS client(id integer PRIMARY KEY AUTOINCREMENT,Monsocket VARCHAR,local VARCHAR, port VARCHAR)"
        curseur.execute(requ1)
        curseur.execute(requ2)
        con.commit()
        con.close()
   except sqlite3.Error as er:
        print(" Erreur initialisation de la base de donnees ",er)
    
    

def initialisation():
    interface.diffusion_en_c.setHidden(True)
    interface.screen_recevoir.setHidden(True)
    interface.frame_accueil.setHidden(False)
    interface.frame_appel.setHidden(True)
    interface.frame_discussion.setHidden(True)
    interface.frame_screenshare.setHidden(True)
    interface.frame_transfert.setHidden(True)
    interface.frame_diffusion.setHidden(True)
    interface.frame_connexion.setHidden(True)
    interface.frame_parametres.setHidden(True)
    interface.frame_apropos.setHidden(True)
    interface.Arreter_enreg_video.setHidden(True)
    interface.Arreter_enreg_bureau.setHidden(True)
    interface.arreter_video_call.setHidden(True)
    #
    interface.stop_vocal.setHidden(True)
    #
    interface.bt_diffuser.setHidden(True)
    interface.diffusion_en_c.setHidden(False)
    
def activation_bouton_accueil():
    interface.frame_accueil.setHidden(False)
    interface.frame_appel.setHidden(True)
    interface.frame_discussion.setHidden(True)
    interface.frame_screenshare.setHidden(True)
    interface.frame_transfert.setHidden(True)
    interface.frame_diffusion.setHidden(True)
    interface.frame_connexion.setHidden(True)
    interface.frame_parametres.setHidden(True)
    interface.frame_apropos.setHidden(True)

def activation_bouton_discussion():
    interface.frame_accueil.setHidden(True)
    interface.frame_appel.setHidden(True)
    interface.frame_discussion.setHidden(False)
    interface.frame_screenshare.setHidden(True)
    interface.frame_transfert.setHidden(True)
    interface.frame_diffusion.setHidden(True)
    interface.frame_connexion.setHidden(True)
    interface.frame_parametres.setHidden(True)
    interface.frame_apropos.setHidden(True)
def activation_bouton_appel():
    interface.frame_accueil.setHidden(True)
    interface.frame_appel.setHidden(False)
    interface.frame_discussion.setHidden(True)
    interface.frame_screenshare.setHidden(True)
    interface.frame_transfert.setHidden(True)
    interface.frame_diffusion.setHidden(True)
    interface.frame_connexion.setHidden(True)
    interface.frame_parametres.setHidden(True)
    interface.frame_apropos.setHidden(True)
def activation_bouton_screenshare():
    interface.frame_accueil.setHidden(True)
    interface.frame_appel.setHidden(True)
    interface.frame_discussion.setHidden(True)
    interface.frame_screenshare.setHidden(False)
    interface.frame_transfert.setHidden(True)
    interface.frame_diffusion.setHidden(True)
    interface.frame_connexion.setHidden(True)
    interface.frame_parametres.setHidden(True)
    interface.frame_apropos.setHidden(True)
def activation_bouton_transfert():
    interface.frame_accueil.setHidden(True)
    interface.frame_appel.setHidden(True)
    interface.frame_discussion.setHidden(True)
    interface.frame_screenshare.setHidden(True)
    interface.frame_transfert.setHidden(False)
    interface.frame_diffusion.setHidden(True)
    interface.frame_connexion.setHidden(True)
    interface.frame_parametres.setHidden(True)
    interface.frame_apropos.setHidden(True)
def activation_bouton_diffusion():
    interface.frame_accueil.setHidden(True)
    interface.frame_appel.setHidden(True)
    interface.frame_discussion.setHidden(True)
    interface.frame_screenshare.setHidden(True)
    interface.frame_transfert.setHidden(True)
    interface.frame_diffusion.setHidden(False)
    interface.frame_connexion.setHidden(True)
    interface.frame_parametres.setHidden(True)
    interface.frame_apropos.setHidden(True)

def activation_bouton_connexion():
    interface.frame_accueil.setHidden(True)
    interface.frame_appel.setHidden(True)
    interface.frame_discussion.setHidden(True)
    interface.frame_screenshare.setHidden(True)
    interface.frame_transfert.setHidden(True)
    interface.frame_diffusion.setHidden(True)
    interface.frame_connexion.setHidden(False)
    interface.frame_parametres.setHidden(True)
    interface.frame_apropos.setHidden(True)
def activation_bouton_parametres():
    interface.frame_accueil.setHidden(True)
    interface.frame_appel.setHidden(True)
    interface.frame_discussion.setHidden(True)
    interface.frame_screenshare.setHidden(True)
    interface.frame_transfert.setHidden(True)
    interface.frame_diffusion.setHidden(True)
    interface.frame_connexion.setHidden(True)
    interface.frame_parametres.setHidden(False)
    interface.frame_apropos.setHidden(True)
def activation_bouton_apropos():
    interface.frame_accueil.setHidden(True)
    interface.frame_appel.setHidden(True)
    interface.frame_discussion.setHidden(True)
    interface.frame_screenshare.setHidden(True)
    interface.frame_transfert.setHidden(True)
    interface.frame_diffusion.setHidden(True)
    interface.frame_connexion.setHidden(True)
    interface.frame_parametres.setHidden(True)
    interface.frame_apropos.setHidden(False)

def envoyer():
    if (ETAT==0):
        pyautogui.alert("veuillez vous connectez d'abord")
        return
    else:
         if(ETAT==1):
             ser_envoyer()
         else:
              client_envoyer()
def stopper_rec_screen():
    try:
        interface.screen_recevoir.setText("STOPPER")
        interface.screen_recevoir.setHidden(True)
    except:
        return
#
def lancer_ap_vid():
    if (ETAT==0):
        pyautogui.alert("veuillez vous connectez d'abord")
        return

    else:
        ms="JE_VEUX_FAIRE_UN_APPEL_VIDEO"
        envoyer_alerte(ms)
    

 #fonction lance appel  
def lancer_appel():
    if (ETAT==0):
        pyautogui.alert("veuillez vous connectez d'abord")
        return

    else:
        ms="JE_VEUX_EMETTRE_UN_APPEL_VOCAL"
        if(ETAT==1):
          con.send(ms.encode('utf8'))
        else :
            Monsocket.send(ms.encode('utf8'))
        interface.appel_V.setText(str("Appel en cours"))  
        return    
def send_me_file():
     Le_nom=interface.zone_name_file.text()
     if(Le_nom!=""):
        if(ETAT==0):
            pyautogui.alert(" Veuillez vous connectez d'abord")  
            return activation_bouton_connexion()   
        else:
            try:
                MSG="JE_VEUX_PARTAGER_UN_FICHIER"
                envoyer_alerte(MSG)
                if(ETAT==1):
                    send_file_server()
                else:
                    send_file_client()
            except:
                return
     else:
           pyautogui.alert(" Veuillez selectionnez un fichier")

def select_file_send():
    monfichier=QFileDialog.getOpenFileName()
    Le_nom=monfichier[0]
     
    if(Le_nom==""):
        pyautogui.alert(" Selectionner d'abord un fichier")
        return
    interface.zone_name_file.setText(str(Le_nom))
    #send_me_file(Le_nom)
def select_file_to_broad():
    try:
        monfichier=QFileDialog.getOpenFileName()
        Le_nom=monfichier[0]
        
        if(Le_nom==""):
            pyautogui.alert(" Vous n'avez selectionne aucun fichier")
            return
        interface.name_file_to_broad.setText(str(Le_nom))
        interface.bt_diffuser.setHidden(False)
    except:
        return

def lancer_cap_bureau():
    t_bureau=threading.Thread(target=capturebureau)
    t_bureau.start()
def arret_appel_video():
    interface.arreter_video_call.setText("ARRETER")

initialisation()
initialisation_bd()
#interface.act.clicked.connect(mettre)
interface.bt_accueil.clicked.connect(activation_bouton_accueil)
interface.bt_discussion.clicked.connect(activation_bouton_discussion)
interface.bt_appel.clicked.connect(activation_bouton_appel)
interface.bt_screenshare.clicked.connect(activation_bouton_screenshare)
interface.bt_transfert.clicked.connect(activation_bouton_transfert)
interface.bt_connexion.clicked.connect(activation_bouton_connexion)
interface.bt_diffusion.clicked.connect(activation_bouton_diffusion)
#
interface.bt_parametres.clicked.connect(activation_bouton_parametres)
interface.Machine_disponible.clicked.connect(screenServ)
interface.bt_apropos.clicked.connect(activation_bouton_apropos)
#
interface.Desactiver.clicked.connect(activer_monpartage_ecran)
interface.bt_envoyer.clicked.connect(envoyer)
interface.screen_recevoir.clicked.connect(stopper_rec_screen)
#
interface.creer_client.clicked.connect(se_connecter_v)
interface.creer_serveur.clicked.connect(creer_serveur)
#appel video
interface.appel_vi.clicked.connect(initialiseur_ap_vid)
#
#interface.appel_V.clicked.connect(recevoir_appel)
interface.appel_V.clicked.connect(lancer_appel)
#outils
interface.Enregistrer_bureau.clicked.connect(lancer_cap_bureau)
interface.select_file.clicked.connect(select_file_send)
interface.send_file.clicked.connect(send_file_file)
##
interface.select_to_broad.clicked.connect(select_file_to_broad)

##
interface.bt_diffuser.clicked.connect(go_to_diffusion)

interface.arreter_video_call.clicked.connect(arret_appel_video)

#

interface.arreter_diffusion.clicked.connect(arret_dif)
interface.diffusion_video_disponible.clicked.connect(lancer_dif)
interface.appel_vi.clicked.connect(lancer_ap_vid)
interface.stop_vocal.clicked.connect(racrocher_vocal)
interface.Arreter_enreg_bureau.clicked.connect(destroy_bureau)
interface.show()
p.exec()
#Systemexit()