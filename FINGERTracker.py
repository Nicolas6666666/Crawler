
class FINGERTracker:
    __instance = None
    __inited = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if type(self).__inited:
            return
        type(self).__inited = True

        self.fingerprints = dict()
        
    
    def add_fingerprint(self, url, fingerprint):
        self.fingerprints[url] = fingerprint
    
    def get_fingerhashes(self):
        return self.fingerprints.values()
    