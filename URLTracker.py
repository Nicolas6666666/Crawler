from collections import defaultdict




class URLTracker:
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

        self.parsed_urls = []
        self.ics_subdomains = defaultdict(lambda: 0)
        self.unique_url_count = 0
  
    
    def add_new_unique(self):
        self.unique_url_count+=1
    
    def add_ics_subdomain(self, url, path):
        if path != "":
            self.ics_subdomains[url]+=1
        else:
            self.ics_subdomains[url] = 0
    
    def is_parsed(self, url):
        return url in self.parsed_urls
    
    def add_parsed(self, url):
        self.parsed_urls.append(url)
    
    def get_ics_subdomains(self):
        return self.ics_subdomains

    def get_unique_url_count(self):
        return self.unique_url_count
    

    


    
    
    
    
    
    

    


