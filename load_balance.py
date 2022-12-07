import logging
import threading
from websocket_server import WebsocketServer
from socket import *

# API https://github.com/Pithikos/python-websocket-server
# Note that list structure is thread-safe in python. Deadlock is not possible in this program


# task queue
tasks = []

ips = ["192.122.236.104", "171.67.92.155", "129.110.253.31"]

clients = [None] * 3
available_machine = [False, False,
                     False]  # list to lock backend machines and block potential data transferring to the working machines
dict = {}  # dictionary to store pending messages


# This function is called when the load and balance server is receiving message from frontend
def message_received(client, server, message):
    clientID = client["id"]
    # Received URI
    if clientID in dict:  # If the client hasn't finished receiving messages, append the continued message to the dictionary
        dict[clientID][1] += message
        if (message.endswith("\n")):  # URI ends with '\n' indicates end of message
            print("get full message")
            tasks.append((dict[clientID][0], dict[clientID][1]))  # append a tuple of client and its completed message
            dict.pop(clientID)  # remove the finished client from the dictionary
    else:  # situation when the message is new
        if (message.endswith("\n")):  # URI ends with '\n' indicates end of message
            tasks.append((client, message))
        else:  # otherwise add this new client-message pair to the dictionary
            dict[clientID] = [client, message]  # store temp message


# This function is called when load balance is needed to handle multiple thread situation
def load_balance():
    # This function is executed by a thread. Take out a task and send to appropriate backend machines
    while True:
        if True in available_machine and len(tasks) != 0:
            index = available_machine.index(True)
            available_machine[index] = False  # 锁死
            task = tasks.pop(0)
            client = task[0]  # get client
            message = task[1] + "\n"  # get url
            clients[index] = client  # store the client info
            threading.Thread(target=task_handler,
                             args=(index, message)).start()  # start a thread to handle the task in a backend machine


# load balancing server and backend machine interaction
def task_handler(index, message):
    print("available machine: " + str(index))
    s = socket(AF_INET, SOCK_STREAM)  # Establish TCP connection with the backend
    s.connect((ips[index], 12345))
    s.send(message.encode())  # send image as URI
    res = s.recv(4096)  # receive result from backend
    client = clients[index]
    clients[index] = None
    server.send_message(client, res.decode())  # send result back to frontend
    available_machine[index] = True  # unlock the available machine
    s.close()  # close socket


if __name__ == '__main__':
    # ask what mode
    mode = int(input("1. Machine1\n2. Machine2\n3. Machine3\n4. Auto LoadBalancing\n\n"))
    if mode < 4:
        available_machine[mode - 1] = True
    elif mode == 4:
        available_machine[0] = True
        available_machine[1] = True
        available_machine[2] = True
    server = WebsocketServer(host='192.41.233.54', port=12345)  # create websocket
    lb_thread = threading.Thread(target=load_balance)  # start load_balance
    server.set_fn_message_received(message_received)
    lb_thread.start()
    server.run_forever()  # Run websocket server
    print("ok")
