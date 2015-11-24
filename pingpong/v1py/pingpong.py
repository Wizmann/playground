import sys
import socket
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
)


class Server(object):
    def __init__(self, port, sleep=0):
        self.port = port
        self.sleep = sleep

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self.port))
        s.listen(1)
        while True:
            client, address = s.accept()
            logging.info('start to get packet from client[%s:%s]' %
                    (address[0], address[1]))
            cnt = 0
            while True:
                info = client.recv(1024)
                if not info:
                    break
                client.send("pong")
                cnt += 1
            logging.info('stop to get packet from client[%s:%s], cnt = %d' %
                    (address[0], address[1], cnt))
            client.close()
        s.close()

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
            time.sleep(self.sleep)

        logging.info("ping pong is finished")
        client.shutdown(socket.SHUT_RDWR)
        client.close()


if __name__ == '__main__':
    if sys.argv[1] == 'server':
        s = Server(9000)
        s.start()
    elif sys.argv[1] == 'client':
        c = Client('127.0.0.1', 9000, loop=1000000)
        c.start()
