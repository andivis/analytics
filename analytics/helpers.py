import io
import os.path


def getFile(fileName):
    if not os.path.isfile(fileName):
        return ""

    f = open(fileName, "r")
    return f.read()


def getLines(fileName):
    if not os.path.isfile(fileName):
        return []

    with open(fileName) as f:
        return f.readlines()


def toFile(s, fileName):
    with io.open(fileName, "w", encoding="utf-8") as text_file:
        print(s, file=text_file)


def appendToFile(s, fileName):
    with io.open(fileName, "a", encoding="utf-8") as text_file:
        print(s, file=text_file)


def numbersOnly(s):
    return ''.join(filter(lambda x: x.isdigit(), s))


def findBetween(s, first, last):
    try:
        start = s.index(first) + len(first)
    except ValueError:
        start = 0

    try:
        if not last:
            end = len(s)
        else:
            end = s.index(last, start)
    except ValueError:
        end = len(s)

    return s[start:end]

def getNested(j, keys):
    try:
        element = j

        i = 0

        for key in keys:
            if not key in element:
                break;
            
            element = element[key]

            if i == len(keys - 1):
                return element

            i += 1
    except:
        return ""

def stringToFloatingPoint(s):
    result = 0.0

    temporary = ""

    for c in s:
        if c.isdigit() or c == ".":
            temporary += c

    try:
        result = float(temporary)
    except:
        result = 0.0

    return result