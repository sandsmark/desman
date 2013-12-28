# -*- coding: utf-8 -*-
"""
This file contains two classes, TestServer and Tester.
TestServer is responsible for listening locally on a specified port
and dispatching new Tester-threads for incoming connections.
The Tester-objects are responsible for communicating with a Master, and
running tests locally.
"""

import socket, hmac, threading, os, config, connection

class TestServer(threading.Thread):
    """
    Socket server listening for connections, and dispatching children.
    """

    def __init__(self):
        threading.Thread.__init__(self)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

    def run(self):
        """
        Run thread.
        """
        # Keep track of children for killing
        children = []

        try:
            self.running = True
            self.sock.bind(('', config.TESTER_PORT))
            self.sock.listen(2)

            while self.running:
                clientsock, clientaddress = self.sock.accept()
                print ("New connection from:" + clientaddress)

                if len(children) > config.MAX_CHILDREN:
                    # Try to see if any of the children are dead
                    for i in range(len(children)):
                        if children[i].running is False:
                            del children[i]
                    
                    # If it didn't help, just disconnect, and go back to
                    # waiting for the next connection.
                    if len(children) > config.MAX_CHILDREN:
                        clientsock.close()
                        continue

                client = Tester(clientsock)
                client.start()
                children.append(client)

        except socket.error, errmessage:
            print (" GENERAL ERROR FAIL: " + errmessage)
            print ("shit failed, dying.")
            self.sock.close()

        # Reap children
        for child in children:
            child.stop()
            child.join()
        print ("stopped!")

class Tester(threading.Thread):
    """
    Thread responsible for running tests locally, for a master.

    """
    def __init__(self, sock):
        threading.Thread.__init__(self)

        self.connection = connection.Connection(sock)
        self.running = True

    def run(self):
        """
        This is the main method, running for the lifetime of the thread.
        It receives command from the connecting machine, and returns results
        from the test.
        """

        try:
            if self.read_message() is not "HELLO":
                raise IOError("Did not receive handshake.")

            while self.running:
                self.connection.send_message("OK")
                message = self.connection.read_message() # Receive command to run.
                if message[:3] == "run ":
                    self.connection.send_message(self.run_test(message[3:]))
                elif message == "ping":
                    self.connection.send_message("pong")
                else:
                    raise IOError("Received unknown command '" + message + "'.")
        except IOError, errmessage:
            print ("communication error: " + errmessage)
            print ("shit failed, child dying")
        except:
            print ("unhandled exception")
        finally:
            self.connection.close()

        return

    def run_test(self, test):
        """
        Tries to run a test locally, and send back any results.
        """
        if test in config.LOCAL_TESTS:
            path = config.TESTS_PATH + test # Path to the test to run

            # Check to see if we can execute the path.
            if not os.access(path, os.X_OK):
                raise Exception("Unable to execute test.")

            for line in os.popen(path).readlines():
                self.send_message(line)
            self.send_message("FIN")
        else:
            raise IOError("Asked to run non-enabled test.")

