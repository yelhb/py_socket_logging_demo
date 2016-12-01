#! -*- coding: utf8 -*-

import os
import sys
import time
import struct
import pickle
import logging
import SocketServer

from multiprocessing import Process

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/lib/')

import log
import log_socket

class LogRecordStreamHandler(SocketServer.StreamRequestHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data):
        return pickle.loads(data)

    def handleLogRecord(self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)

class LogRecordSocketReceiver(SocketServer.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = 1

    def __init__(self, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

def receiver():
    log_path = os.path.dirname(os.path.realpath(__file__)) + '/log/'
    log_name = "mainlog"
    log.init_log(log_path + log_name, logging.DEBUG)

    tcpserver = LogRecordSocketReceiver()

    tcpserver.serve_until_stopped()  


def sender(s_id):
    log_socket.init_log()
    
    cnt = 100

    while cnt > 0:
        logging.info("Thread %d, CURRENT TIME: %s" % (s_id, str(time.time())))
        cnt -= 1
        time.sleep(2)

def main():
    
    p_list = []
    p_receiver = Process(target=receiver, name="receiver")
    p_list.append(p_receiver)
    p_receiver.start()

    for i in range(3):
        p = Process(target=sender, name="sender_%d" % i, args=(i,))
        p_list.append(p)
        p.start()

    for p in p_list:
        p.join()

if __name__ == "__main__":
    main() 
