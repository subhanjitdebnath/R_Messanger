import socket
import threading

# List to keep track of connected clients
clients = []
online_list = {}
sentTo =""


def update_online_list(client_socket, name, addr):
    online_list[name] = client_socket
    print(f"Registered : {name} against address : {addr}")


def remove_online_list(client_socket):
    for k,v in online_list:
        if v == client_socket :
            online_list.pop(k)


def sendmsg(to, message, sender_socket):
    client = online_list[to]
    if client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)


def sendonlineList(sender_socket):
    online_guys ="*** FRIENDS ONLINE ********\n"
    for k in online_list.keys():
        online_guys += "** "+k + "\n"
    online_guys += "*************************\n"
    for client in clients:
        try:
            client.send(online_guys.encode())
        except:
            clients.remove(client)


def handle_client(client_socket, addr):
    print(f"[+] New connection from {addr}")
    clients.append(client_socket)
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"[{addr}] {message}")
            if "RegisterMe" in message:
                update_online_list(client_socket, str(message).split("$")[1], addr)
                sendonlineList(client_socket)
            else:
                jmessage_frame = str(message).split("$")
                sendmsg(jmessage_frame[2],f"{jmessage_frame[0]} :{jmessage_frame[1]}",client_socket)

        except:
            break
    print(f"[-] Connection closed from {addr}")
    sendonlineList(client_socket)
    #clients.remove(client_socket)
    client_socket.close()

def start_server(host='10.170.169.107', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("********************* SERVER DETAILS *********************")
    print(f"** Server IP Address : {host} \n** Port : {port}")
    print("********************** SERVER LOGS ***********************")

    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    start_server(local_ip)
