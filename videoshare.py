from vidstream import VideoClient
import threading
def diffuser_moi():
    client=VideoClient(ip_server,9009,"206.mp4")
    t1=threading.Thread(target=client.start_stream)
    t1.start()
    print("client en cours")
    while True:
        continue
