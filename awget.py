import sys, random, socket

def printUsage():
    print('Usage: awget.py <URL> -c <chainfile>')


def createConnection(address, port, hopList):
    byteString = ""
    for hop in hopList:
        if hop == hopList[len(hopList) - 1]:
            byteString += hop
        else:
            byteString += hop + ","

    print(byteString)
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
        createConnection(ssAddress, ssPort, hopList)
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
