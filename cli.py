import uuid
import json
import socket
import threading
import rsa


from Crypto.PublicKey import RSA
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()


client_uuid = str(uuid.uuid4())
target_uuid = ""

# Server configuration
HOST = 'localhost'
PORT = 5000



# Create a client socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def senderClient(client_socket):
    data = {
        'uuid': client_uuid,
        'public_key': str(public_key)
    }
    data_string = json.dumps(data)


    client_socket.send(bytes(data_string, 'utf-8'))

    while True:
        message = input("Select Options:\n 1-send message \n 2-exit\n Enter number you selected: ")
        if(message == "1"):
            target = input("send target uuid:")
            message = input("Enter message: ")
            target_uid = target
            print(json.dumps({'type':'send_uid','target_uid':target,'self_uuid':str(client_socket)}))
            client_socket.send(bytes(json.dumps({'type':'send_uid','target_uid':target,'self_uuid':str(client_socket)}), 'utf-8') )




#         client_socket.send(message.encode())





def receiverClient(client_socket):
    while True:
        # Receive a response from the server
        response = client_socket.recv(1024).decode()
        response = json.loads(response)
        if response['step'] == 'none':
            if response['type'] == 'allUsers':
#                 print(response['message'])
                for k,v in response["message"].items():
                    print(k,v)
        if response["step"] == '2' :

            # TODO public_key server
            decrypt_target_public_key_uid_target_uid_self  = rsa.decrypt(public_key, response["message"] )
            if(target_uid):
                print("fuck")
        if response["step"] == '2' :

            # TODO public_key server
            decrypt_target_public_key_uid_target_uid_self  = rsa.decrypt(public_key, response["message"] )
            if(target_uid):
                print("fuck")


        print(f'Received response: {response}')

if __name__ == '__main__':

    threading.Thread(target=receiverClient, args=(client_socket,)).start()
    threading.Thread(target=senderClient, args=(client_socket,)).start()
