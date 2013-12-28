import socket

class Connection():

    def __init__(self, sock):
        self.sock.file_descriptor = sock.makefile()
        self.counter = 0

    def send_message(self, string):
        """
        Sends a message through the file descriptor, and also sends a 
        checksum for verification purposes.
        """
    
        self.file_descriptor.write(string + "\n")
        self.counter += 1
        secret = config.KEY + str(self.counter)
        self.file_descriptor.write(hmac.new(secret, string).hexdigest() + "\n")
    
    def read_message(self):
        """
        Reads a message from the file descriptor, and also verifies the 
        checksum.
        This is vulnerable to mitm, but who cares.
        It is not vulnerable to replay attacks.
        """
    
        string = self.file_descriptor.readline().strip()
        checksum = self.file_descriptor.readline().strip()
        self.counter += 1
        secret = config.KEY + str(self.counter)
        if checksum is not hmac.new(secret, string).hexdigest():
            raise IOError("Received invalid hmac.")
    
        return string

    def close(self):
        self.sock.close()

