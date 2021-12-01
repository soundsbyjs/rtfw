## I will not pretend that this code isn't absolutley disgusting lol
## I've never written python, nor have I ever used beautifulsoup before
## so yeah... please contribute!

## usage:
## archwiki -l [Wiki Page]
##  lists all the sections under contents on a given wiki page
## archwiki -v [wiki page] [section]
##  prints the contents of the section on the given wiki page

import requests
import sys
from bs4 import BeautifulSoup
 
# this is kind of a bad name for this function
# but basically it pulls out each of the sections of the article
# under Contents and returns a list
# it also grabs the numbers before them
# but those numbers occur after the name
# so the list from Vim looks like [ 'installation', '1', usage, '2' ]
def cutSubStringAtAHREF(string, start=None):
    if start is not None:
        i = start
    else:
        i = 0
    buffer = ""
    retList = []
    # sudo c style for loop using a while true
    # cuz this lang is dumb
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
# this function is totally broken
def printSection(section, followingSection):

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




# int main(int argc, char* argv[]) 
# {
if len(sys.argv) == 3 and sys.argv[1] == '-l':
    page = requests.get("https://wiki.archlinux.org/title/" + sys.argv[2]) # Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup

    subjects = soup.find_all('div', class_='toc')
    contents = cutSubStringAtAHREF(str(subjects))
    printContents(contents)

elif len(sys.argv) == 4 and sys.argv[1] == -v:
    page = requests.get("https://wiki.archlinux.org/title/" + sys.argv[2]) # Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup

    subjects = soup.find_all('div', class_='toc')
    contents = cutSubStringAtAHREF(str(subjects))
    
else:
    print("Invalid syntax")

# }
