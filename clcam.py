from vidstream import StreamingServer
from vidstream import ScreenShareClient
from vidstream import AudioSender
from vidstream import CameraClient
from vidstream import AudioReceiver
from datetime import datetime
import pyautogui
import threading
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
lancer_envoi_ap_video()
