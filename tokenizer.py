import re
from collections import defaultdict, OrderedDict
import sys


# tokenize function only handle the basic english characters with basic rules
def tokenize(file):  # O(n)
    """read file and turns file into a string"""

    # with open(file, 'r', errors="ignore", encoding="utf-8") as f:
    #     file_contents = f.read()  # O(n)
    #     text = str(file_contents)
    #     # print(text)
    """tokenize the string with regular expression"""
    # text = text.lower()
    text = file.lower()
    text = text.replace("_", " ")
    tokens = re.findall(r'[a-zA-Z0-9]+', text)  # O(n)
    return tokens


def tokenize_file(file):
    """read file and send to the tokenize machine by lines"""
    token = []
    # if file.endswith(".docx"):
    #     try:
    #         doc = docx.Document(file)
    #         for line in doc:  # O(n)
    #             line = line.strip()
    #             # print(line)
    #             token += tokenize(line)
    #     except Exception as e:
    #         print("An exception occurred:", type(e).__name__)
    #         print("Exception code:", sys.exc_info()[0])

    try:
        with open(file, 'r', errors="ignore", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:  # O(n)
                line = line.strip()
                # print(line)
                token += tokenize(line)
    except FileNotFoundError:
        print("File not found error: Please check the file path and name.")
    except PermissionError:
        print("Permission error: You do not have permission to access this file.")
    except UnicodeDecodeError:
        print("Unicode decode error: The file is not encoded in the expected format.")
    except IOError:
        print("IO error: There is an input/output error.")
    except ValueError:
        print("Value error: The file is not in the expected format.")
    except Exception as e:
        print("An exception occurred:", type(e).__name__)
        print("Exception code:", sys.exc_info()[0])
    return token



# Process the tokens into a dict and sort the dict base on the token frequency
def computeWordFrequencies(tokens):
    dict1 = defaultdict(default_value)
    """add up the times a token appears into the defaultdict"""
    for i in tokens:  # O(n)
        dict1[i] += 1
    """sort the dict into correct order(decrease order by times(value))"""
    sorted_data = OrderedDict(sorted(dict1.items(), key=lambda x: (-x[1], x[0])))  # O(nlogn)
    return sorted_data


def default_value():
    return 0


# print out the result
# def resultPrint(dict_map):
#     """print the result"""
#     for k, v in dict_map.items():  # O(n)
#         print(k + " - " + str(v))
#     return


def main(text):
    if text != "":
        return computeWordFrequencies(tokenize(text))
    else:
        exit()
        print("Need at least 1 file to run")
        return 1

# if __name__ == "__main__":
#     main(sys.argv)