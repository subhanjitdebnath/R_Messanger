import socket
import threading
import os

host_details = []
def get_serverdetails():
    print("********************* ENTER SERVER DETAILS *********************")
    ip = input("**     IP address of server : ")
    port = input("**     Port address of server : ")
    print("*****************************************************************")
    host_details.append(ip)
    host_details.append(port)


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(message)
        except:
            print("[-] Disconnected from server.")
            break

def start_client(host='10.170.169.107', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except:
        print("[-] Unable to connect to server.")
        return
    name = input("Enter your name: ")

    os.system('cls')
    print("********* WELCOME TO J-messanger *********")
    print(f"{name} is online . Type messages and press Enter to send. Type 'exit' to quit.\n")

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    registery_msg = f"RegisterMe${name}"
    client_socket.send(registery_msg.encode())
    while True:
        message = input()
        if message.lower() == 'exit':
            break
        to = input("To : ")
        full_message = f"{name}${message}${to}"
        client_socket.send(full_message.encode())

    client_socket.close()

if __name__ == "__main__":
    get_serverdetails()
    start_client(host_details[0], int(host_details[1]))
