import re
from html import parser
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from simhash import Simhash
from difflib import SequenceMatcher
from tokenizer import main as tokenizer
import requests

# parsed = urlparse('http://user:pass@NetLoc:80/path;parameters?query=argument#fragment')


def is_all_ascii(string):
    #checks if a given string contains only ASCII characters
    for char in string:
        if ord(char) > 127:
            return False
    return True

def _is_valid(anchor):
    #checks if an anchor link is valid
    # print("_________", anchor)
    
    if anchor is None:
        return False
    if anchor == "":
        return False
    
    if anchor == "/":
        return False
    
    #if anchor is a single character
    # if len(anchor) < 2:
    #     return False
    
    
    # check if the anchor is a single # character 
    if len(anchor) > 0 and "#"  == anchor[0]:
        return False

    if "mailto:" in anchor or "ftp:" in anchor or "tel:" in anchor or "sms:" in anchor:
        return False
    
    if "javascript:void(0)" in anchor:
        return False
    
    if "://" in anchor:
        if not ("http://" in anchor or 'https://' in anchor):
            return False 
    
    if not is_all_ascii(anchor):
        return False
    return True

def _absolutesize(url, anchor):    
    # absolutesized_url = ""
    # parsed_url = urlparse(url)
    # print(anchor)
    # domain = parsed_url.scheme + "://"  + parsed_url.netloc
    # path = parsed_url.path
    # absolutesized_url = urljoin(url, anchor)
    # return absolutesized_url
    return urljoin(url, anchor)
    
# def _absolutesize(url, anchor):
#     #takes a URL and an anchor link and returns an absolute URL
#     absolutesized_url = ""
#     parsed_url = urlparse(url)
#     # print(anchor)

#     domain = parsed_url.scheme + "://"  + parsed_url.netloc
#     path = parsed_url.path
        
    # print("DOMAIN " + domain)
    # print("***")
    # print("ANCHOR: " + anchor)
    
    # already absolute
    
    
    
    # if anchor.startswith("http") or anchor.startswith("https"):
    #     return anchor
    

    
    # # link to another domain
    # if anchor.startswith("//"):
    #     return domain.split(":")[0] + ":" + anchor
    
    
    # # an .html is referring to .html with path
    # # https://www.ics.uci.edu/~babaks/BWR/Home.html
    # # /Home_files/calcium.txt
    
    # # an .html is referring to  path/path/.html
    # if("." in path and "." in anchor and "/" in anchor):
    #     new_path = url.split("/")
    #     new_path = "/".join(new_path[:-1]) + "/" if not anchor.startswith("/") else ""
    #     path_to_html = anchor.split("/")
    #     return new_path + anchor 
    #     # return new_path + path_to_html[-1]
        
        
    # if("." in path and "." in anchor and "/" not in anchor): 
    #     new_path = url.split("/")
    #     new_path = "/".join(new_path[:-1]) + "/" if not anchor.startswith("/") else ""
    #     return new_path + anchor
    
    
    # # an .html is referring to .html only without path
    # if("." in path and "." in anchor and "/" not in anchor): # https://www.ics.uci.edu/~babaks/codes.html and activities.html
    #     new_path = url.split("/")
    #     new_path = "/".join(new_path[:-1]) + "/" if not anchor.startswith("/") else ""
    #     return new_path + anchor

        
    # # directory is referring to an .html     
    # if ("." in anchor):
    #     return url + ("/" if not anchor.startswith("/") else "") + anchor # https://www.ics.uci.edu/~babaks and codes.html

    # # if .html is referring to a path
    # if ("." in path):  # http://www.cnn.com/news/financial/index.html  # images/nasdaq.jpg -> http://www.cnn.com/news/financial/images/nasdaq.jpg
    #     new_path = url.split("/")
    #     new_path = "/".join(new_path[:-1]) +  "/" if not anchor.startswith("/") else "" 
    #     return new_path + anchor
    # else:
    #     return domain +  ("/" if not anchor.startswith("/") else "") + anchor # slash

def _check_length(text):
    return len(text) > 1800

def connect_status_check(status_num):
    if status_num == 200:
        return True
    else:
        print("NOT OK: " + str(status_num))
        return False

def _delete_fragment(absolutesized_url):
    parsed = urlparse(absolutesized_url)
    if parsed.fragment != "":
        return absolutesized_url[:absolutesized_url.index("#")]
    else:
        return absolutesized_url

# def _add_www(url):
#     parsed = urlparse(url)
#     if(not parsed.neloc.startswith("www")):
        

def tokenize(link, content):
    # TODO
    soup = BeautifulSoup(content, "html.parser")
    # first check if it is high enough textual value page
    text = soup.get_text()
    if not _check_length(text):
        return dict()
    # includes css too texts = soup.findAll(text=True)
    # print(soup.get_text())
    freq_dict = tokenizer(text)
    # print(soup.get_text())
    return freq_dict
    
    

def parse_page(url, content):
    '''
    takes a URL and the HTML content of a page, parses the content with BeautifulSoup, extracts all anchor tags,
    and returns a list of valid absolute links. It also calls the tokenize() function to tokenize the page content
    and return a frequency dictionary of words.
    '''
    soup = BeautifulSoup(content, "html.parser")
    # tokenize(content)
    # check if the page has high textual information
    # Note, can't really do it here 
    #_is_high_textual(soup.get_text())
    # parse anchors
    anchors = soup.find_all("a")
    # print("anchors", anchors)
    # if not anchors:
    #     return []
    # for anchor in anchors:
        # print(anchor.get(""))
    # print("_____________________ ANCHORS __________________")
    # [print(anchor.get("href")) for anchor in anchors]
    # print("_____________________ END ANCHORS __________________")

    
    hrefs = [_delete_fragment(_absolutesize(url, anchor.get("href"))) for anchor in anchors if _is_valid(anchor.get("href"))]
    # print("_____________________ ABSOLUTESIZED __________________")
    # [print(e) for e in hrefs]
    # print("_____________________ END ABSOLUTESIZED __________________")

    
    return hrefs

def match_to_domains(netloc):
    #matches any of the domains specified in the domains list using a regular expression match
    domains = [r".*ics\.uci\.edu.*", r".*cs\.uci\.edu.*", r".*informatics\.uci\.edu.*", r".*stat\.uci\.edu.*"]
    for domain in domains:
        if re.match(domain, netloc):
            return True
    return False


# possibilities:
# https://mds.ics.uci.edu
# https://www.ics.uci.edu/
# https://mdogucu.ics.uci.edu/workshops.html
# https://www.mdogucu.ics.uci.edu/workshops.html

def check_ics_domain(url, url_tracker):
    parsed = urlparse(url)
    # if the url refers to actual page within a domain rather than the domain itself
    a_page = False
    splitted_domain = parsed.netloc.split(".")
    # the domain is not ics.uci.edu
    if not all(part in splitted_domain for part in ["ics", "uci", "edu"]):
        return
    
    # if(parsed.path != ""):
    #     a_page = True 
    if "www" in splitted_domain:
        splitted_domain.remove("www")
    
    # print(splitted_domain, parsed.path)
    # 
    # if len(splitted_domain) > 3 and parsed.path != "":
    if len(splitted_domain) >3:
        # vision.ics.edu
        # subdomain_url = parsed.schema + "://" + ".".join(splitted_domain[:splitted_domain.index("ics")])
        # subdomain_url = parsed.schema + "://" + ".".join(splitted_domain[:splitted_domain.index("ics")])
        # url_tracker.add_ics_subdomain(subdomain_url)
        url_tracker.add_ics_subdomain(parsed.scheme + "://" + parsed.netloc, parsed.path)
        

        
    # return (subdomain_url, a_page)

            
    

def check_simhush(page_content:str, finger_lib):
    finger = ('%x' % Simhash(get_features(page_content)).value)
    for i in finger_lib:
        if string_similarity(finger,i) >= 70:
            return []
    return finger

def get_features(s):
    width = 2
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def string_similarity(str1, str2):
    matcher = SequenceMatcher(None, str1, str2)
    return int(round(matcher.ratio()*100))