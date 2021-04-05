import socket
import sys
import re  # regular-expression library, yes we've got some fun

from services import services

MAX_PORTS = 65353


def help():
    print(f"[HELP]  usage: python {sys.argv[0]} <target-address> <starting-port> <ending-port>")


def isAddressValid(address):
    isValid = re.search(
        "^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$",
        address)
    if not isValid:
        print("[ERROR]: The target address is not valid IP address")
        help()
        exit(5)


def checkLenArgs(list):
    if len(list) < 4:
        print("[ERROR] Please specify the address ,the starting port and the ending port")
        help()
        exit(1)


def checkIntPorts(list):
    try:
        port1 = int(list[2])
        port2 = int(list[3])
    except ValueError:
        print(f"[ERROR] The port should be an integer number")
        help()
        exit(2)
    return port1, port2


def checkValidPort(port):
    if port < 0 or port >= MAX_PORTS:
        print(f"[ERROR] Port should be between 0 and {MAX_PORTS - 1}")
        help()
        exit(4)


def checkSmaller(port1, port2):
    if port1 > port2:
        print(f"[ERROR]: Ending port should be greater than the starting port.")
        help()
        exit(3)


def checkArgs():
    checkLenArgs(sys.argv)
    isAddressValid(sys.argv[1])
    host = str(sys.argv[1])
    startingPort, endingPort = checkIntPorts(sys.argv)
    checkValidPort(startingPort)
    checkValidPort(endingPort)
    checkSmaller(startingPort, endingPort)
    return host, startingPort, endingPort


def savePort(f, portNumber):
    f.write(f"Port {portNumber}\n")


def portScanner(f, host_port):
    port = host_port[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex(host_port):
        print(f"[-]  Port {port} is closed")
    else:
        savePort(f, port)
        service = services.get(port)
        if service:
            print(f"[+]  Port {port} is open. {service} is found")
        else:
            print(f"[+]  Port {port} is open")
    sock.close()


def main():
    host, port1, port2 = checkArgs()
    f = open("open-ports.txt", 'a')
    for port in range(port1, port2 + 1):
        host_port = (host, port)
        portScanner(f, host_port)
    f.close()


if __name__ == "__main__":
    main()
