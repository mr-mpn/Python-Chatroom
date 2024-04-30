import socket
import threading

host = '127.0.0.1'
port = 9090

server = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
server.bind((host , port))
server.listen()


clients = []
nicknames = []

def broadcast(message):  #sends a message to all the connected clients
    for client in clients :
        client.send(message.encode('ascii'))
        
        
def handle(client):
    while True:
        try:  #if there are no errors from the client
            message = client.recv(1024).decode('ascii')  #1024 bytes
            broadcast(message)
        except:  #for when a client is removed, meaning there is an error
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]  #client and its nickname have the same indexes 
            broadcast(f"{nickname} Left the chat ...")
            print(f"{nickname} left the chatroom")
            nicknames.remove(nickname)
            break
        
        
def receive():
    while True:
        client , address = server.accept()  #server accepts the clients connection
        #Reminder : When a connection is accepted with server.accept() then a new socket is created (client)
        print(f"Connected with {str(address)}")  #This print is not broadcasted, it's only used in the console
        
        client.send('Nick'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        
        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} has joined the chatroom")
        
        client.send("You are connected to the server".encode('ascii'))
        
        thread = threading.Thread(target=handle, args=(client,))#we need multi threading 
        thread.start()
        
print("SERVER IS LISTENING ...")   
receive()
