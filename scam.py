from vidstream import StreamingServer
from vidstream import ScreenShareClient
from vidstream import AudioSender
from vidstream import AudioReceiver
from datetime import datetime
from vidstream import AudioReceiver
import pyautogui
import threading
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
                print(" Active")
                while True:
                    continue
                recevoir_appel_video.stop_server()
                vocalrecevoir_appel_v.stop_server()
            except:
                 pyautogui.alert(" Une erreur est survenue")

##
def lancer_envoi_ap_video():
    port=5002
    ports=4002
    ar_s="192.168.56.1"
    envoyer=CameraClient(ar_s,port)
    thread_client_video=threading.Thread(target=envoyer.start_stream)
    
    #
    vocalsend=AudioSender(ar_s,ports)
    thread_client_audio=threading.Thread(target=vocalsend.start_stream)
    #
    thread_client_video.start()
    thread_client_audio.start()

    print("client en cours")
    while True:
        continue

    envoyer.stop_stream()
    vocalsend.stop_stream()

 
