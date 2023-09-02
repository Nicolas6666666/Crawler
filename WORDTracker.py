from collections import defaultdict
from stop_words import STOP_WORDS


class WORDTracker:
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
        self.largest_word_count = 0
        self.largest_url = ""
        self.words_count = defaultdict(lambda: 0)
    
    
    def update_word_count(self, dictionary):
        for k,v in dictionary.items():
            if k not in STOP_WORDS:
                self.words_count[k] += v
    
    
    def update_max(self, url,  max):
        if self.largest_word_count < max:
            self.largest_word_count = max
            self.largest_url = url
    
    def get_largest_word_count(self):
        return self.largest_url, self.largest_word_count
    
    # TODO: sort
    def get_50_words_count(self):
        split_index = 50
        first_50 = dict(list(self.words_count.items())[:split_index]) 
        return first_50
        