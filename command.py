class Command:
    def __init__(self, raw, session):
        self.raw = raw
        self.session = session
        parts = raw.split("|")
        self.timestamp = int(parts[0])
        self.cmd = parts[1]
        if len(parts) == 3:
            self.payload = parts[2]
        else:
            self.payload = ""