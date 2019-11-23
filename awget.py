import sys, random, socket, os

def printUsage():
    print('Usage: awget.py <URL> -c <chainfile>\n\tNo argument will use default file: chaingang.txt')


def printHopList(hopList):
    for hop in hopList:
        addr = hop.split(" ")[0]
        port = hop.split(" ")[1]
        print(addr + ", " + port)


# readChainFile(): convert chainFile to list
def readChainFile(chainFile = "chaingang.txt"):
    hopList = []
    try:
        with open(chainFile, "r") as chainFile:
            for link in chainFile:
                hopList.append(link.rstrip("\n\r"))
        return hopList
    except IOError:
        print("Could not read file " + chainFile + "\nExiting...")
        exit(1)


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


# createConnection(): connect to next ss in chainlist
def createConnection(hopList, URL):
    # Gather nextSS info
    numHops = int(hopList.pop(0))
    randomSS = random.randint(0, numHops - 1)
    nextSS = hopList[randomSS]
    ssAddress = nextSS.split(" ")[0]
    ssPort = int(nextSS.split(" ")[1])

    print("Request: " + URL + "\nChainlist is ")
    printHopList(hopList)
    print("Next SS is " + ssAddress + ", " + str(ssPort))

    # Create connection to nextSS
    ssSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssSocket.connect((ssAddress, ssPort))

    # Send information and wait for response
    try:
        # Format: [URL, ssAddr ssPort, ssAddr, ssPort, ...]
        ssSocket.sendall(listToString(hopList, URL).encode())

        print("Waiting for file...")
        fileName = getFileName(URL)
        file = open(fileName, "wb")
        response = ssSocket.recv(1024)
        file.write(response)
        while response:
            response = ssSocket.recv(1024)
            file.write(response)

        print("Received file " + fileName)
        print("Goodbye!")
        file.close()
        ssSocket.close()
    except KeyboardInterrupt:
        print("Got keyboard interupt")
        exit(1)



def main():
    cmdLineArgs = sys.argv[1:]
    numArgs = len(cmdLineArgs)

    if numArgs == 1:
        # Read local chain file
        URL = cmdLineArgs[0]
        hopList = readChainFile()
        createConnection(hopList, URL)
    elif cmdLineArgs[1] == '-c' or cmdLineArgs[1] == "-C":
        # Use custom chain file
        URL = cmdLineArgs[0]
        chainFile = cmdLineArgs[2]
        hopList = readChainFile(chainFile)
        createConnection(hopList, URL)
    else:
        printUsage()


if __name__ == '__main__':
    main()
