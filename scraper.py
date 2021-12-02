## I will not pretend that this code isn't disgusting lol
## I've never written python, nor have I ever used beautifulsoup before
## so yeah... please contribute!

## usage:
## rtfw [Wiki Page]
##  lists all the sections under contents on a given wiki page
## rtfw [wiki page] [section]
##  prints the contents of the section on the given wiki page

import requests
import sys
from bs4 import BeautifulSoup
 

## this one cuts up a string containing the tags for each of the 
## things under the wiki's "contents" header
## it then writes it to a list
## it will also grab the numbers that appear before them 
## (but it writes those numbers to the list after the given title)

def cutSubStringAtAHREF(string, start=None):
    if start is not None:
        i = start
    else:
        i = 0
    buffer = ""
    retList = []
    # sudo c style for loop using a while true
    # there might be a better way to do this???
    while True:
        if string[i:i + 6] == "a href":
            i = i + 9
            while True:
                if not string[i] == '"':
                    buffer = buffer + string[i]
                    i = i + 1
                else:
                    retList.append(buffer)
                    buffer = ""
                    i = i + 2
                    while True:
                        if string[i] == ">":
                            i = i + 1
                            while True:
                                if string[i] == "<":
                                    break
                                else:
                                    buffer = buffer + string[i]
                                    i = i + 1
                            break
                        else:
                            i = i + 1
                    retList.append(buffer)
                    buffer = ""
                    break
        elif i == len(string):
            return retList
        else:
            i = i + 1

## this guy prints the contents of the list made in the previous function
## again this is probably a really bad way to do this
## but brute forcing stuff is fun!

def printContents(contents):
    print("Contents: ")
    index = 0
    while True:
        if index == len(contents):
            break
        else:
            length = len(contents[index + 1])
            while length > 0:
                print("", end=' ')
                length = length - 1
            print(contents[index + 1], end=' ')
            print(contents[index])
            index = index + 2

# prints the section of the arch wiki page asked for
# given a string with the name of the section and the name of the following section
# it looks for the line containing a \n before and after [section]
# and cuts the text out between it and the string [followingsection] meeting the same criteria
# this function is totally broken and this is a terrible way to do this
# and in hindsight I'm not sure how we're going to handle the last line
def printSection(section, followingSection, pageText):

    index = 0

    test = section.replace('_', ' ')
    test2 = followingSection.replace('_', ' ')
    while True:
        ## find the first occurance of the string so we can ignore it
        ## since this is just the contents section
        if (pageText[index:index + len(test) + 1] == test + '\n'):
            break
        else:
            index = index + 1

    index = index + len(test) + 1
    
    # my professors say I use while True too much
    # buT I LOVE IT
    while True:
        if pageText[index:index + len(test) + 1] == test + '\n':
            while True:
                if pageText[index:index + len(test2) + 1] == test2 + '\n':
                    break
                else:
                    print(pageText[index], end='')
                    index = index + 1
            break
        else:
            index = index + 1

# there's probably a library function that does this
# this codebase is getting more and more illegible by the MINUTE lol 
def findStringLocationInList(string, list):
    # oh wow another while true
    # didn't see that coming
    i = 0
    while True:
        if list[i] == string:
            return i
        elif i == len(list):
            break
        else:
            i = i + 1
    return 0 

# int main(int argc, char* argv[]) 
# {
if len(sys.argv) == 3:
    page = requests.get("https://wiki.archlinux.org/title/" + sys.argv[1]) # Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup

    subjects = soup.find_all('div', class_='toc')
    contents = cutSubStringAtAHREF(str(subjects))
    printContents(contents)
# if we're printing out the contents of a section of the wiki page
elif len(sys.argv) == 4:
    page = requests.get("https://wiki.archlinux.org/title/" + sys.argv[1]) # Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup

    subjects = soup.find_all('div', class_='toc')
    contents = cutSubStringAtAHREF(str(subjects))
     
    contentsSection = findStringLocationInList(sys.argv[2], contents)
    if contentsSection != 0:
        pageText = str(soup.get_text())
        printSection(contents[contentsSection - 1], contents[contentsSection + 1], pageText)
    else:
        print("Invalid syntax")

    
else:
    print("Invalid syntax")
# }
