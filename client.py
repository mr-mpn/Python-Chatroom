import socket
import threading

host = '127.0.0.1'
port = 9090

nickname = input("Please choose a nickname:  ")
client = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)

client.connect((host,port)) #Client is now connected to the server

#we need a thread for every message sent

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii') #the message is coming from the server
            if message == 'Nick': #server is asking for the nickname of the connected client
                client.send(nickname.encode('ascii')) #client sends it's nickname to the server
            else:
                print(message) #shows the message coming from the server
        except:
            print("An error occurred:")
            client.close()
            break
        
        
# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))
            
            
receive_thread = threading.Thread(target = receive)
receive_thread.start()

write_thread = threading.Thread(target = write)
write_thread.start()