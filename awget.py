import sys
import getopt
# Takes up to 2 command line args
    # awget <URL> [-c chainfile]
    # if no chainfile supplied, read the local file called chaingang.txt
    # else if problems with file, print error and exit

def printUsage():
    print('Usage: awget.py <URL> -c <chainfile>')


def main():
    print("Hello from awget.py")
    argv = sys.argv[1:]
    numArgs = len(argv)

    if numArgs == 1:
        # Read Local chain file
        URL = argv[0]
        print("Reading chaingang.txt")
    elif numArgs == 3 and argv[1] == '-c':
        # Use custom chainfile
        URL = argv[0]
        print("Reading custom chain file in argv[2]")
    else:
        printUsage()



if __name__ == '__main__':
    main()
