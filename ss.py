import sys, socket, random, os, tempfile

def printUsage():
    print('Usage: ss.py <PORT>')


def removeSelf(hopList, port):
    ip = socket.gethostbyname(socket.gethostname())
    searchString = ip + " " + str(port)
    hopList.remove(searchString)
    return hopList


def listToString(list, URL):
    listString = URL + ","
    lastElement = len(list) - 1
    for element in list:
        if element == list[lastElement]:
            listString += element
        else:
            listString += element + ","
    return listString


def readInSegments(tempFile, buffer = 1024):
    while True:
        content = tempFile.read(buffer)
        if not content:
            break
        yield content


def createServer(hostname, port = 8099):
    # 2. ss prints the hostname and port, it is running on. To find hostname you can use gethostname.
    # 3. Create the socket and fill in its values. Then Bind the socket.
    # 4. Create a loop statement and set the socket in listen mode.
    # 5. Once a connection arrives, it reads the URL and the chain information.
    print("Running on " + hostname + ":" + str(port))

    # Create listening socket for connection requests
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((hostname, port))
    serverSocket.listen(1)

    # Loop in listen mode
    while True:
        clientSocket, clientAddress = serverSocket.accept()
        print("Client connected to server: ", clientAddress)

        clientMessage = clientSocket.recv(1024).decode()
        hopList = clientMessage.split(",")
        URL = hopList.pop(0)

        # TODO: create thread for connection
        # 6. Create a thread using pthread_create (or python equivalent) and pass the arguments.[Or use select()]
        hopList = removeSelf(hopList, port)
        if not hopList:
            # 7. If the chain list is empty:
            tempFile = tempfile.NamedTemporaryFile()
            os.system("wget " + "--output-document=" + tempFile.name + " " + URL)
            for line in readInSegments(tempFile):
                clientSocket.send(line)
            tempFile.close()
            clientSocket.close()
        else:
            # 8. If the chain list is not empty:
                numHops = len(hopList)
                randomSS = random.randint(0, numHops - 1)
                nextSS = hopList[randomSS]
                ssAddress = nextSS.split(" ")[0]
                ssPort = int(nextSS.split(" ")[1])

                # Connect to next SS
                ssSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ssSocket.connect((ssAddress, ssPort))

                # Send data and wait for response
                try:
                    # Format: [URL, ssAddr ssPort, ssAddr, ssPort, ...]
                    ssSocket.sendall(listToString(hopList, URL).encode())
                    tempFile = tempfile.NamedTemporaryFile(mode="ab+")
                    response = ssSocket.recv(1024)

                    tempFile.write(response)
                    while response:
                        response = ssSocket.recv(1024)
                        tempFile.write(response)

                    tempFile.seek(0)

                    for segment in readInSegments(tempFile):
                        clientSocket.send(segment)

                    tempFile.close()
                    clientSocket.close()
                    ssSocket.close()

                # TODO: will need to read data in chunks
                except KeyboardInterrupt:
                    print("Got keyboard interrupt")
                    exit(1)


def main():
    cmdLineArgs = sys.argv[1:]
    numArgs = len(cmdLineArgs)
    hostname = socket.gethostname()

    # 1. ss takes one optional argument, the port it will listen on. Example(./ss 20000)
    if numArgs == 1:
        port = int(cmdLineArgs[0])
        createServer(hostname, port)
    elif numArgs == 0:
        # use default port
        createServer(hostname)
    else:
        printUsage()


if __name__ == '__main__':
    main()
