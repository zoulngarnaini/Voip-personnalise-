from vidstream import StreamingServer
import threading

ser=StreamingServer("",9009)
t2=threading.Thread(target=ser.start_server)
t2.start()
print("Serveur en cours")
while True:
    continue