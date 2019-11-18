import sys
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


def main():
    print("Hello from ss.py")


if __name__ == '__main__':
    main()
