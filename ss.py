import sys, socket
# acts as both the client and server
# there is 1 ss running on each machine.
# When the ss starts it prints the hostname and port it is listening to,
# and then waits for connections
# Once, connection arrives, the ss reads the list of remaining ss's in the request
# and if the list is not empty, strips itself from the list and forwards the request to a randomly
# chosen ss in the list. If the ss is the last entry on the list, it extracts the URL of the desired
# document and executes the system() command to issue a wget to retrieve the document,
# and then forwards the document back to the previous ss.
# once the document is forwarded, the ss erases the local copy of the file and tears down the connection
def printUsage():
    print('Usage: ss.py <PORT>')


def createConnection(hostname, port = 8099):
    print("Running on " + hostname + ":" + str(port))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((hostname, port))
        sock.listen()
        connection, address = sock.accept()
        with connection:
            print("Connected by", address)
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                hopList = data.decode().split(",")
                print(hopList)


def main():
    print("Hello from ss.py")
    argv = sys.argv[1:]
    numArgs = len(argv)
    hostname = socket.gethostname()

    if numArgs == 1:
        port = int(argv[0])
        createConnection(hostname, port)
    elif numArgs == 0:
        # use default port
        createConnection(hostname)
    else:
        printUsage()

if __name__ == '__main__':
    main()
