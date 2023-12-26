import re
from urllib.parse import urlparse
import scraperhelper as sh
# from simhash import Simhash
from collections import defaultdict
from URLTracker import URLTracker
from WORDTracker import WORDTracker
from FINGERTracker import FINGERTracker

# from difflib import SequenceMatcher

# TODO cases to handle
# https://mse.ics.uci.edu/%20
# https://www.informatics.uci.edu/?page_id=87 
# domains are: ["www.ics.uci.edu", "www.cs.uci.edu", "www.informatics.uci.edu", "www.stat.uci.edu"]
# index.html is the same as HOME !
# remove the fragment of URL


# parsed_urls = []
# finger_lib = []
# ics_subdomains = defaultdict(lambda: 0)
# unique_url_count = 0

# largest_url_word_count = 0
# largest_url = ""

# last_url = ""
# last_path = ""
# def def_value():
#     return 0

# words_count = defaultdict(def_value)

# stopwords_list = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are',\
#     "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', \
#         "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down',\
#             'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours\tourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']



def scraper(url, resp):
    frontier = extract_next_links(url, resp)
    frontier = [link for link in frontier if is_valid(link)]
    return frontier
    

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    # print(resp.url)
    # print(resp.status)
    # print("url: " + url)
    # print("resp.url: " + resp.url)
    # print("resp.status: " + str(resp.status))
    # print(resp.raw_response.content)
    
    url_tracker = URLTracker()
    word_tracker = WORDTracker()
    finger_tracker = FINGERTracker()
    
    # check for a url trap here:
    # get the path
    parsed = urlparse(url)
    # print(url + "---" + parsed.path)

    # print(parsed.path)

    
    # print()
    # global largest_url
    # global largest_url_word_count
    # global words_count
    # global finger_lib
    # global unique_url_count
    # global ics_subdomains
    
    add_to_frontier = []
    # if the domain changes then the fingerpring []
    
    
    if sh.connect_status_check(resp.status):
        # make finger print and check similairity
        page_content = str(resp.raw_response.content)
        if page_content == "":
            return []
        finger = sh.check_simhush(page_content, finger_tracker.get_fingerhashes())
        if finger == []:
            return []
        # finger = ('%x' % Simhash(get_features(page_content)).value)
        # for i in finger_lib:
        #     if string_similarity(finger,i) >= 70:
        #         return []
        finger_tracker.add_fingerprint(resp.url, finger)
        # finger_lib.append(finger)
        # add to all unique urls 
        url_tracker.add_new_unique()
        # check if ics.uci.edu domain 
        # sub_domain_url, a_page = sh.check_ics_domain(url, url_tracker)
        sh.check_ics_domain(url, url_tracker)
        
        # if sub_domain_url != "":
        #     if a_page:
        #         ics_subdomains[sub_domain_url]+=1
                
        links = sh.parse_page(resp.url, resp.raw_response.content)
        # print("LINK-----" ,resp.url)
        tokenized_result = sh.tokenize(resp.url, resp.raw_response.content)
        # print(tokenized_result)
        # add non stop words tokens to the dict
        word_tracker.update_word_count(tokenized_result)
        # for k,v in tokenized_result.items():
        #     if k not in stopwords_list:
        #         words_count[k] += v
        # count the total word count in html file(include english stop words)
        word_tracker.update_max(resp.url, sum(tokenized_result.values()))
        
        # max_num = sum(tokenized_result.values())
        # if largest_url_word_count < max_num:
        #     largest_url_word_count = max_num
        #     largest_url = resp.url
        # print(words_count)
        # print(largest_url)
        # print(largest_url_word_count)
        # print(tokenized_result)

        # for link in links:
        #     if(is_valid(link) and (link not in parsed_urls)):
        #         # tokenize and do necessary checks
        #         add_to_frontier.append(link)
        #         parsed_urls.append(link)
        
        for link in links:
            if(is_valid(link) and not url_tracker.is_parsed(link)):
                add_to_frontier.append(link)
                url_tracker.add_parsed(url)
                
        # add_to_frontier = [link for link in links if is_valid(link)]
        # for link in add_to_frontier:
        #     print(link)
        # print(parsed_urls)
        
        ### CHECKS THE TRACKERS:
        print()
        print(f"1. URL with largest word count: {word_tracker.get_largest_word_count()[0]}")
        print("------------------------------------------------------------------------------------------------")
        print(f"1.1 max word count: {word_tracker.get_largest_word_count()[1]} ")
        print("2. First 50 common words: ")
        for key, value in word_tracker.get_50_words_count().items():
            print(f"{key} --- {value}")
        print("------------------------------------------------------------------------------------------------")
        print(f"3. Number of  Unique URLs: {url_tracker.get_unique_url_count()}")        
        print("------------------------------------------------------------------------------------------------")
        print("4. ICS domains:")
        for key, value in url_tracker.get_ics_subdomains().items():
            print(f"{key} --- {value}")
        print("------------------------------------------------------------------------------------------------")
        print()
        return add_to_frontier
    else:
        file1 = open("InvalidResponses.txt", "a")  # append mode
        file1.write(url + "---"  + str(resp.status) + "\n")
        file1.close()
    # print(resp.raw_response.content)

    return list()



def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not sh.match_to_domains(parsed.netloc):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico|img"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise

