# Necessary libraries
import tkinter as tk
import socket
import threading
import ssl


# Creating the window 
window = tk.Tk()
window.title("Server")

# Top frame consisting of two buttons widgets (btnStart, btnStop) for starting/stopping the server
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Start", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Host: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the connected clients area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=15, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

# Creating necessary variables 
server = None
HOST_ADDR = '0.0.0.0'
HOST_PORT = 5050
client_name = " "
clients = []
clients_names = []


# Certificate files 
server_cert = 'server.crt'
server_key = 'server.key'
client_certs = 'client.crt'

# Verify certificate
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)


# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT 
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    # Creating the server socket, with TCP 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Binding the address 
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # server is listening for client connection
    print("Server is waiting for requests")

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Host: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Stop server function
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)
    server.close()
    

# Acept clients function 
def accept_clients(the_server, y):
    while True:
        clientS, addr = the_server.accept()
        client = context.wrap_socket(clientS, server_side=True)
        print("SSL established. Peer: {}".format(client.getpeercert()))
        clients.append(client)

        # use a thread so as not to clog the gui thread
        threading._start_new_thread(send_receive_client_message, (client, addr))



# Function to receive message from current client and
# send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, clients_addr
    client_msg = " "

    # Send welcome message to client
    client_name  = client_connection.recv(4096).decode()
    welcome_msg = "Welcome " + client_name + ". Use 'exit' to quit"
    client_connection.send(welcome_msg.encode())


    clients_names.append(client_name)
    update_client_names_display(clients_names)  # Update connected clients names display


    while True:
        data = client_connection.recv(4096).decode()
        if not data: break
        if data == "exit": break

        client_msg = data

        idx = get_client_index(clients, client_connection)
        sending_client_name = clients_names[idx]

        for c in clients:
            if c != client_connection:
                server_msg = str(sending_client_name + "->" + client_msg)
                c.send(server_msg.encode())

    # Find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()

    update_client_names_display(clients_names)  # Update client names display


# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()


