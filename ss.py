import sys, socket, random, os, tempfile, threading

def printUsage():
    print('Usage: ss.py -p <PORT>\n\tNo argument will use default port 8099')


def printHopList(hopList):
    for hop in hopList:
        addr = hop.split(" ")[0]
        port = hop.split(" ")[1]
        print(addr + ", " + port)


# removeSelf(): removes current ss from chainlist
def removeSelf(hopList, port):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    searchString = ip + " " + str(port)
    searchString2 = hostname + " " + str(port)
    if searchString in hopList:
        hopList.remove(searchString)
    if searchString2 in hopList:
        hopList.remove(searchString2)
    return hopList


# listToString(): return list and url in string format to be sent to next ss
def listToString(list, URL):
    listString = URL + ","
    lastElement = len(list) - 1
    for element in list:
        if element == list[lastElement]:
            listString += element
        else:
            listString += element + ","
    return listString


# readInSegments(): reads contents from file and returns them in defined buffer size
def readInSegments(tempFile, buffer = 1024):
    while True:
        content = tempFile.read(buffer)
        if not content:
            break
        yield content


# fileNotEmpty(): checks if file is empty
def fileNotEmpty(file):
    file.seek(0)
    line = file.read()
    if line == b'':
        return False
    else:
        return True


# getFileName(): determine file name based on the URL
def getFileName(URL):
    commonTopLevelDomains = ["com", "org", "net", "us", "co", "int", "mil", "edu", "gov", "ca", "cn", "fr", "ch", "au", "in",
                            "de", "jp", "nl", "uk", "mx", "no", "ru", "br", "se", "es"]
    filename = os.path.basename(URL)
    matchFlag = False
    if filename != "":
        splitName = filename.split(".")
        size = len(splitName)
        for domain in commonTopLevelDomains:
            if domain == splitName[size - 1]:
                matchFlag = True
        if matchFlag == True:
            name = "index.html"
        else:
            name = filename
    else:
        name = "index.html"
    return name


# isValidPort(): checks if port is within the valid port range
def isValidPort(port):
    return port > 0 and port < 65536


def handleConnection(clientSocket, port, hopList, URL):
    hopList = removeSelf(hopList, port)

    print("Request: " + URL)
    if not hopList:
        # If the chain list is empty:
        print("Chainlist is empty")
        print("Issuing wget for file " + getFileName(URL))
        tempFile = tempfile.NamedTemporaryFile()
        os.system("wget " + "--output-document=" + tempFile.name + " " + URL + " > /dev/null 2>&1")

        if fileNotEmpty(tempFile):
            tempFile.seek(0)
            print("File received")
            print("Relaying file...")
            for line in readInSegments(tempFile):
                clientSocket.send(line)
            print("Goodbye!")
            tempFile.close()
            clientSocket.close()
        else:
            print("Failed to retrieve file")
            print("Relaying error")
            errorString = "Unable to retrieve file from URL: " + URL
            clientSocket.sendall(errorString.encode())
            print("Goodbye!")
            tempFile.close()
            clientSocket.close()
    else:
        # If the chain list is not empty:
        numHops = len(hopList)
        randomSS = random.randint(0, numHops - 1)
        nextSS = hopList[randomSS]
        ssAddress = nextSS.split(" ")[0]
        ssPort = int(nextSS.split(" ")[1])

        print("Chainlist is ")
        printHopList(hopList)
        print("Next SS is " + ssAddress + ", " + str(ssPort))

        # Connect to next SS
        ssSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssSocket.connect((ssAddress, ssPort))

        # Send data and wait for response
        try:
            # Format: [URL, ssAddr ssPort, ssAddr, ssPort, ...]
            ssSocket.sendall(listToString(hopList, URL).encode())

            print("Waiting for file...")

            tempFile = tempfile.NamedTemporaryFile(mode="ab+")
            response = ssSocket.recv(1024)
            errorCheck = response.decode()
            responseCheck = errorCheck.split(" ")
            if responseCheck[0] == "Unable":
                errorString = "Unable to retrieve file from URL: " + URL
                clientSocket.sendall(errorString.encode())
                print("Failed to retrieve file")
                print("Relaying error")
                print("Goodbye!")
                tempFile.close()
                ssSocket.close()
            else:
                tempFile.write(response)
                while response:
                    response = ssSocket.recv(1024)
                    tempFile.write(response)

                tempFile.seek(0)

                print("Relaying file...")

                for segment in readInSegments(tempFile):
                    clientSocket.send(segment)

                tempFile.close()
                clientSocket.close()
                ssSocket.close()
        except KeyboardInterrupt:
            print("Got keyboard interrupt")
            exit(1)


# createServer(): creates socket and handles client connections
def createServer(hostname, port = 8099):
    print("SS " + hostname + "(" + socket.gethostbyname(hostname) + "), " + str(port) + ":")

    # Create listening socket for connection requests
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((hostname, port))
    serverSocket.listen(1)

    # Loop in listen mode
    while True:
        clientSocket, clientAddress = serverSocket.accept()
        clientMessage = clientSocket.recv(1024).decode()
        hopList = clientMessage.split(",")
        URL = hopList.pop(0)

        clientThread = threading.Thread(target = handleConnection, args = (clientSocket, port, hopList, URL), daemon=True)
        clientThread.start()


def main():
    cmdLineArgs = sys.argv[1:]
    numArgs = len(cmdLineArgs)
    hostname = socket.gethostname()

    if numArgs == 0:
        # Use default port
        createServer(hostname)
    elif cmdLineArgs[0] == "-p" or cmdLineArgs[0] == "-P":
        port = int(cmdLineArgs[1])
        if isValidPort(port):
            # Use custom port
            createServer(hostname, port)
        else:
            print("Invalid port number\nExiting...")
            exit(1)
    else:
        printUsage()


if __name__ == '__main__':
    main()
