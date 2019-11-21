import sys, random, socket

def printUsage():
    print('Usage: awget.py <URL> -c <chainfile>')


def getRequestByteString(hopList, URL):
    # Convert hopList to bytestring
    byteString = "0,"
    for hop in hopList:
        byteString += hop + ","
    byteString += URL
    return byteString

def createConnection(address, port, hopList, URL):
    byteString = getRequestByteString(hopList, URL)

    # Send bytestring over socket connection to next SS
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((address, port))
        sock.sendall(byteString.encode())


def readFile(URL, fileName = "chaingang.txt"):
    hopList = []

    try:
        with open(fileName, "r") as file:
            for line in file:
                hopList.append(line.rstrip("\n\r"))
        numHops = int(hopList.pop(0))
        randomSS = random.randint(0, numHops - 1)
        nextHop = hopList[randomSS]
        ssInfo = nextHop.split(" ")
        ssAddress = ssInfo[0]
        ssPort = int(ssInfo[1])
        createConnection(ssAddress, ssPort, hopList, URL)
    except IOError:
        print("Could not open/read file " + fileName + "\nExiting...")
        exit(1)


def main():
    print("Hello from awget.py")
    argv = sys.argv[1:]
    numArgs = len(argv)

    if numArgs == 1:
        # Read Local chain file
        URL = argv[0]
        readFile(URL)
    elif numArgs == 3 and argv[1] == '-c':
        # Use custom chainfile
        URL = argv[0]
        fileName = argv[2]
        readFile(URL, fileName)
    else:
        printUsage()



if __name__ == '__main__':
    main()
