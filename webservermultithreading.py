import threading

import socket
import threading
import logging
from time import sleep

# define logging format with date, time, and message
logging.basicConfig(
    format='(%(threadName)-10s) %(asctime)s %(message)s', level=logging.DEBUG)

def reactor(host, port):
        # create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # configure socket to reuse address
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind to the port
    server.bind((host, port))

    # queue up to 5 requests
    server.listen(5)

    # log the server start
    logging.debug("Listening on " + host + ":" + str(port))

    while True:
        # establish a connection
        conn, addr = server.accept()

        # logging.debug("Got a connection from %s" % str(addr))

        # create a thread to handle the client
        clientThread = threading.Thread(
            target=client_handler, args=(conn, addr))

        # start the thread
        clientThread.start()

def client_handler(conn, addr):
    """ Handle client connection """
    # log the connection
    logging.debug('Connected by ' + str(addr))

    # create
    try:
        # read index.html
        with open('index.html', 'r') as f:
            file_data = f.read()
            f.close()
        
        # send http response header
        conn.send(b'HTTP/1.0 200 OK\r\n')
        conn.send(b'Content-Type: text/html\n')
        conn.send(b'\n')
        # send index.html
        conn.send(file_data.encode())
        # print closing message
        logging.debug('Connection closed by ' + str(addr))
        return
    finally:
        # print closing message
        logging.debug('Connection closed by ' + str(addr))
        # close connection
        conn.close()


if __name__ == '__main__':
    reactor('localhost',8080)
