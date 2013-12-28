import uuid

class Master
    def __init__(self):
        self.known_hosts = []
        self.is_master = False
        self.id = uuid.uuid1()
        self.current_master = ""
