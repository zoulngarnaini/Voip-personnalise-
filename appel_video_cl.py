from re import T
from vidstream import CameraClient
from vidstream import StreamingServer
from vidstream import AudioSender
from vidstream import AudioReceiver
import threading
import time
global thread_serveur_video
global thread_client_video
global thread_client_audio
global thread_serveur_audio

def lancer_serveur_ap_video():
        local=""
        port=5001
        ports=4001
        ##
        recevoir_appel_video=StreamingServer(local,port)
        vocalrecevoir_appel_v=AudioReceiver(local,ports)
        thread_serveur_audio=threading.Thread(target=vocalrecevoir_appel_v.start_server)
        #
        thread_serveur_video=threading.Thread(target=recevoir_appel_video.start_server)
        thread_serveur_audio.start()
        thread_serveur_video.start()
        while input("")!="STOP":
            continue
        recevoir_appel_video.stop_server()
        vocalrecevoir_appel_v.stop_server()

##
def lancer_reception_ap_video():
    port=5001
    ports=4001
    envoyer=CameraClient(ip_server,port)
    thread_client_video=threading.Thread(target=envoyer.start_stream)
    thread_client_video.start()
    #
    vocalsend=AudioSender(ip_server,ports)


    thread_client_audio=threading.Thread(target=vocalsend.start_stream)
    thread_client_audio.start()

    print("serveur en cours")
    while input("")!="STOP":
        continue

    envoyer.stop_stream()
    vocalsend.stop_stream()
