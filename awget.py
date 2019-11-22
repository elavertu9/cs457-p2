import sys, random, socket, os

def printUsage():
    print('Usage: awget.py <URL> -c <chainfile>')


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


def createConnection(hopList, URL):
    # 8. Find a random ss from the list. You can use rand() function. Seed the value to get different random number each time. Python may do this automatically for you.
    # 9. Once you have the ss, IP address and port number, create the socket and fill in its values.
    # 10. Send a connect request to the ss.
    # 11. Once the connect request is accepted, strip the ss details from the chainlist and then send the URL and chainlist to the ss.
    # 12. Wait till you receive the file.
    # Gather nextSS info
    numHops = int(hopList.pop(0))
    randomSS = random.randint(0, numHops - 1)
    nextSS = hopList[randomSS]
    ssAddress = nextSS.split(" ")[0]
    ssPort = int(nextSS.split(" ")[1])

    # Create connection to nextSS
    ssSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssSocket.connect((ssAddress, ssPort))

    # Send information and wait for response
    try:
        # Format: [URL, ssAddr ssPort, ssAddr, ssPort, ...]
        ssSocket.sendall(listToString(hopList, URL).encode())

        fileName = getFileName(URL)
        file = open(fileName, "wb")
        response = ssSocket.recv(1024)
        file.write(response)
        while response:
            response = ssSocket.recv(1024)
            file.write(response)

        file.close()
        ssSocket.close()


        # TODO: handle response, this should be when the requested file has been delivered
        # Will need to read data in chunks
    except KeyboardInterrupt:
        print("Got keyboard interupt")
        exit(1)



def main():
    cmdLineArgs = sys.argv[1:]
    numArgs = len(cmdLineArgs)

    # 1. awget will have up to two command line arguments:
    # 2. Example ./awget [-c chainfile]
    # 3. The URL should point to the document you want to retrieve.
    # 4. Passing the chainfile as an argument is optional
    # 5. If chainfile is not specified awget should read the chain configuration from a local file called chaingang.txt.
    # 6. If no chainfile is given at the command line and awget fails to locate the chaingang.txt file, awget should print an error message and exit.
    # 7. If awget can read both URL and chainfile correctly, proceed.
    if numArgs == 1:
        # Read local chain file
        URL = cmdLineArgs[0]
        hopList = readChainFile()
        createConnection(hopList, URL)
    elif numArgs == 3 and cmdLineArgs[1] == '-c':
        # Use custom chain file
        URL = cmdLineArgs[0]
        chainFile = argv[2]
        hopList = readChainFile(chainFile)
        createConnection(hopList, URL)
    else:
        printUsage()



    # 13. Create a looping statement to receive the file in chunks.
    # 14. Save the data received in a local file. The file name should be same as the file requested. For
        # Example: For example, when given URL is http://www.cs.colostate.edu/~cs457/p2.html the file saved will be named p2.html
    # 15. When URL with no file name is specified, fetch index.html, that is, awget of www.google.com will fetch a file called index.html.


if __name__ == '__main__':
    main()
