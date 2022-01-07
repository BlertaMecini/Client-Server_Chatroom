import tkinter as tk
import socket
import threading


# Creating the window 
window = tk.Tk()
window.title("Sever")

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

