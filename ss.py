import sys, socket, random

def printUsage():
    print('Usage: ss.py <PORT>')


def goToNextHop(address, port, hopList, URL):
    # Convert hopList to bytestring
    byteString = ""
    numHops = len(hopList)

    if numHops > 1:
        for hop in hopList:
            byteString += hop + ","
        byteString += URL
    else:
        byteString = hopList[0] + "," + URL

    # Send bytestring over socket connection to next SS
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((address, port))
        sock.sendall(byteString.encode())


def handleClient(hopList, hostname, port, URL):
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
                URL = hopList.pop(len(hopList) - 1)
                handleClient(hopList, hostname, port, URL)


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
