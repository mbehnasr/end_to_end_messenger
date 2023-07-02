import socket
import threading
import json
# Server configuration


from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP


"""

recipient_public_key = RSA.import_key(open('recipient_public_key.pem').read())

symmetric_key = AES.new(key=bytes.fromhex(''.join(['{:02x}'.format(x) for x in range(16)])), mode=AES.MODE_CBC)

cipher_rsa = PKCS1_OAEP.new(recipient_public_key)
encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)

users = json.load(open('users.json', 'r'))
encrypted_users = symmetric_key.encrypt(json.dumps(users).encode())

users_public_key = json.load(open('users_public_key.json', 'r'))
encrypted_users_public_key = symmetric_key.encrypt(json.dumps(users_public_key).encode())
 """


"""
with open('users.json.enc', 'wb') as f:
    f.write(encrypted_users)

with open('users_public_key.json.enc', 'wb') as f:
    f.write(encrypted_users_public_key)

with open('symmetric_key.enc', 'wb') as f:
    f.write(encrypted_symmetric_key)
 """

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import json

"""


def encrypt_users_and public_key():

    recipient_private_key = RSA.import_key(open('recipient_private_key.pem').read())

    encrypted_symmetric_key = open('symmetric_key.enc', 'rb').read()

    cipher_rsa = PKCS1_OAEP.new(recipient_private_key)
    symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)

    encrypted_users = open('users.json.enc', 'rb').read()
    decrypted_users = symmetric_key.decrypt(encrypted_users)
    users = json.loads(decrypted_users)

    encrypted_users_public_key = open('users_public_key.json.enc', 'rb').read()
    decrypted_users_public_key = symmetric_key.decrypt(encrypted_users_public_key)
    users_public_key = json.loads(decrypted_users_public_key)

 """







HOST = 'localhost'
PORT = 5000
import rsa
users_public_key= {}
private_key = ""
with open("private.pem") as p:
    private_key = p.read()

with open('users_public_key.json',"w") as f:
    f.write("[\n]")

with open('users.json',"w") as f:
    f.write("[\n]")

new_user = {}

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Store client sockets
client_sockets = []
connected_clients = {}



# TODO send public_key self to server
def RSA_encrypt_1(private_key,id_target,id_self,public_key_target):
    encrypt_message = rsa.encrypt(bytes(public_key_target+id_self+id_target, 'utf-8'), bytes(private_key,'utf-8'))
    return encrypt_message


"""

def handle_group_message(client_socket, message):
    # Extract group identifier and message from the received message
    group_id, group_message = message.split(":")

    # Forward the group message to all clients in the group
    if group_id in groups:
        for socket in groups[group_id]:
            if socket != client_socket:
                socket.send(group_message.encode())

def join_group(client_socket, group_id):
    # Add the client socket to the group
    if group_id not in groups:
        groups[group_id] = []
    groups[group_id].append(client_socket)

 """







def serverHandler(client_socket):
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024).decode()
            print(message)

            message = json.loads(message)
            if message["type"] == "send_uid" :
                print(f'Received message: {message}')
                with open('users.json') as file:
                        json_users = json.load(file)
#               socket.send(bytes(json.dumps({'step:'}))
                send_to_self = RSA_encrypt_1(private_key,message["target_uid"] ,message["self_uuid"],new_user[message["target_uid"]])
                client_socket.send(json.dumps({'step':'2', 'message': send_to_self}))



            # Forward the message to all connected clients
#             for socket in client_sockets:
#                 if socket != client_socket:
#                     socket.send(message.encode())
        except ConnectionResetError:
            # Handle client disconnection
            client_sockets.remove(client_socket)
            client_socket.close()
            break




def accept_connections():
    while True:
        client_socket, _ = server_socket.accept()

        client_sockets.append(client_socket)
        print(json.dumps({'login':'New client connected.'}))

        login = client_socket.recv(1024).decode()
        login = json.loads(login)

        new_user[login["uuid"]]= login["public_key"]

        with open('users_public_key.json', 'r') as add_me, open('users_public_key.json', 'r+') as add_to_me:
            add_me_data = json.loads(add_me.read())
            add_to_me_data = json.loads(add_to_me.read())
            add_to_me.seek(0)

            add_to_me.write(str(json.dumps(new_user)))

        with open('users_public_key.json','r') as f:
            users_public_key = json.loads(f.read())


        connected_clients[login["uuid"]] = str(client_socket)


        with open('users.json', 'r') as add_me, open('users.json', 'r+') as add_to_me:
            add_me_data = json.loads(add_me.read())
            add_to_me_data = json.loads(add_to_me.read())
            add_to_me.seek(0)
            add_to_me.write(str(json.dumps(connected_clients)))
#             file.write(allUsers)

        with open('users.json','r') as f:
            json_users = json.loads(f.read())
        for socket in client_sockets:
            socket.send(bytes(json.dumps({'step':'none', 'type':'allUsers','message':json_users}),"utf-8"))
        # Start a new thread to handle the client
        threading.Thread(target=serverHandler, args=(client_socket,)).start()

# Start accepting connections in a separate thread
threading.Thread(target=accept_connections).start()


