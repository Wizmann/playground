import sys
import socket
import time
import select
import errno
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
)

class Server(object):
    def __init__(self, port, sleep=0, timeout=10):
        self.port = port
        self.sleep = sleep
        self.timeout = timeout

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', self.port))
        server.listen(10)

        inputs, outputs = [server], []
        while True:
            readable, writable, exceptional = select.select(inputs, outputs, inputs, self.timeout)

            if not readable and not writable and not exceptional:
                logging.info("select time out")
                continue

            for s in readable:
                if s is server:
                    client, address = s.accept()
                    client.setblocking(0)
                    inputs.append(client)
                    logging.info("established connection with %s:%s" % address)
                else:
                    data = ''
                    while True:
                        try:
                            packet = s.recv(1024)
                            data += packet
                            if not packet:
                                break
                        except socket.error, e:
                            err = e.args[0]
                            if err in [errno.EAGAIN, errno.EWOULDBLOCK]:
                                logging.debug('no data available')
                                break
                            else:
                                logging.fatal(e)
                                sys.exit(-1)

                    if data:
                        logging.debug("recieved data from [%s]: %s" % 
                                (s.getpeername(), data))
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        logging.info("shutdown connection with %s:%s" % s.getpeername())
                        s.close()

            for s in writable:
                s.send('pong')
                outputs.remove(s)

            for s in exceptional:
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                logging.info("shutdown connection with %s" % s.getpeername())
        server.close()

class Client(object):
    def __init__(self, ip, port, loop=5000, sleep=0):
        self.ip = ip
        self.port = port
        self.loop = loop
        self.sleep = sleep

    def start(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.ip, self.port))

        logging.info("connection is built")

        for i in xrange(self.loop):
            client.send("ping")
            info = client.recv(1024)
            logging.debug("recieve from server: %s" % info)
            time.sleep(self.sleep)

        logging.info("ping pong is finished")
        client.shutdown(socket.SHUT_RD)
        client.close()

if __name__ == '__main__':
    if sys.argv[1] == 'server':
        s = Server(9000)
        s.start()
    elif sys.argv[1] == 'client':
        c = Client('127.0.0.1', 9000, loop=1000000)
        c.start()
