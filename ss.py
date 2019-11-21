import sys, socket, random, os, array

def printUsage():
    print('Usage: ss.py <PORT>')


# getByteString(): returns a bytestring in the request format
def getRequestByteString(hopList, URL):
    numHops = len(hopList)
    byteString = "0,"

    if numHops > 1:
        for hop in hopList:
            byteString += hop + ","
        byteString += URL
    else:
        byteString += hopList[0] + "," + URL
    return byteString


# getResponseByteString(): returns byteString of file opened in binary
def getResponseByteString(URL):
    # 1 indicates reply
    byteString = b"1,"

    fileName = getFileName(URL)

    try:
        with open(fileName, "rb") as file:
            for line in file:
                byteString += line + b","
        byteString += fileName.encode()
        return byteString
    except IOError:
        print("Could not open/read file " + fileName + "\nExiting...")
        exit(1)



# goToNextHop(): sends the data to the next hop in the SS list
def goToNextHop(address, port, hopList, URL):
    byteString = getRequestByteString(hopList, URL)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((address, port))
        sock.sendall(byteString.encode())


# getFileName(): determine file name based on the URL
def getFileName(URL):
    commonTopLevelDomains = ["com", "org", "net", "us", "co", "int", "mil", "edu", "gov", "ca", "cn", "fr", "ch", "au", "in"
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


def backTrack(prevIP, port, URL):
    byteString = getResponseByteString(URL)
    print(byteString)
    print(port)
    print(prevIP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((prevIP, port))
        sock.sendall(b'hello world')



def handleClient(hopList, hostname, port, URL, prevAddress):
    # Remove self from hopList
    ip = socket.gethostbyname(hostname)
    removeStr = ip + " " + str(port)
    numHops = len(hopList)

    if numHops == 1:
        hopList.pop(0)
    else:
        for i in range(numHops - 1):
            if hopList[i] == removeStr:
                hopList.pop(i)

    # Reassign numHops post removal
    numHops = len(hopList)

    # Check if last hop
    if numHops == 0:
        # call wget
        print("I am the last hop, getting file: " + URL)
        command = "wget " + URL
        os.system(command)
        backTrack(prevAddress[0], port, URL)
    elif numHops == 1:
        # Go to Last Hop
        print("Going to last hop")
        nextHop = hopList[0]
        ssInfo = nextHop.split(" ")
        ssAddress = ssInfo[0]
        ssPort = int(ssInfo[1])
        goToNextHop(ssAddress, ssPort, hopList, URL)
    else:
        # not done yet go to next hop
        randomSS = random.randint(0, numHops - 1)
        nextHop = hopList[randomSS]
        ssInfo = nextHop.split(" ")
        ssAddress = ssInfo[0]
        ssPort = int(ssInfo[1])
        goToNextHop(ssAddress, ssPort, hopList, URL)


def createConnection(hostname, port = 8099):
    print("Running on " + hostname + ":" + str(port))

    # Create listening socket for connection requests from awget.py
    ssSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssSocket.bind((hostname, port))
    ssSocket.listen(1)

    while True:
        connectedSocket, connectedAddress = ssSocket.accept()
        print("Connected by", connectedAddress)
        data = connectedSocket.recv(1024).decode()
        print(data)
        dataSplit = data.split(",")
        version = dataSplit.pop(0)
        print(dataSplit)
        if version == "0":
            print("Request")
            hopList = dataSplit
            URL = hopList.pop(len(hopList) - 1)
            print(version)
            print(URL)
            handleClient(hopList, hostname, port, URL, connectedAddress)
        elif version == "1":
            print("Reply")
            fileData = dataSplit
            fileName = fileData.pop(len(fileData) - 1)
            print(version)
            print(fileName)
        else:
            print("Unkown")


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
