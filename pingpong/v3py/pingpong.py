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

        epoll_fd = select.epoll()
        epoll_fd.register(server.fileno(), select.EPOLLIN)
        conn = {}

        while True:
            epoll_list = epoll_fd.poll()

            for fd, event in epoll_list:
                if fd == server.fileno():
                    client, address = server.accept()
                    client.setblocking(0)
                    epoll_fd.register(client.fileno(), select.EPOLLIN | select.EPOLLET)
                    logging.info("established connection with %s:%s" % client.getpeername())
                    conn[client.fileno()] = client
                elif event & select.EPOLLIN:
                    data = ''
                    s = conn[fd]
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
                        '''
                        CAUTIONS:
                        it might to lead to a mistake if "stick package" happens,
                        but in our scenario, the packets are too small(4B) to be stick.
                        LOL
                        '''
                        epoll_fd.modify(fd, select.EPOLLET | select.EPOLLOUT)
                    else:
                        logging.info("shutdown connection with %s:%s" % s.getpeername())
                        epoll_fd.unregister(fd)
                        s.close()
                        del conn[fd]
                elif event & select.EPOLLOUT: 
                    s = conn[fd]
                    s.send('pong')
                    epoll_fd.modify(fd, select.EPOLLIN | select.EPOLLET)
                elif event & select.EPOLLHUP:
                    s = conn[fd]
                    logging.info("shutdown connection with %s" % s.getpeername())
                    epoll_fd.unregister(fd)
                    s.close()
                    del conn[fd]
                else:
                    pass
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

