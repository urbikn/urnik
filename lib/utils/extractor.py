#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

"""
    Class meant to extrat lines from downloaded file and transform data into
    a Course object.
    
    In a nutshell: returns list of every occuring class in week
"""

import sys, os, json, inspect

path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if path not in sys.path:
    sys.path.insert(0, path)

from course import Course

class Extractor:
    __classList = None
    __ignoreLine = None # ignores lines in file with specific list of values

    def __init__(self, ignore={}):
        self.__ignoreLine = ignore 
        self.__classList = []


    def __removeEntries(self, list):
        """
            Removes entries in list based on what the ignore lines the user suggested
            
            return: list(type=string)
        """
        
        for index, data in enumerate(list):
            for ignore in self.__ignoreLine:
                if ignore in data:
                    del list[index]

        list = self.__removeChars(list)

        # Location doesn't want to be found, so I bruteforce removed it
        for i in self.__ignoreLine:
            if "LOC" in i:
                return list[1:]
        
        return list

    def __removeChars(self, list):
        """
            Removes keys, ':' and strips values of whitespaces. Format example of text:
            Key:value <- removes key 
            
            return: list(type=string)
        """
        newList = []
        
        for entiry in list:
            entiry = entiry.split(":")[1].strip()
            newList.append(entiry)

        return newList
    
    
    def getClassList(self):
        return self.__classList
    
    
    def getDummyList(self):
        """
            Returns a list containing 6 lines just saying that you don't have
            class.
            
            return: list(type=Course)
        """
        self.__classList = []
        for index in range(0,6):
            data = Course(index, "", "Danes nimaš pouka.", "", "")
            self.__classList.append( data )

        return self.getClassList()


    def extractFromFile(self, file):
        """
            Reads lines from file and based on the value of line it recreates a new
            list or a new Course object or appends lines to the list.
                
            return: None
        """
        for index, line in enumerate(file):
            # initialize variables and list 
            if "BEGIN:VEVENT" in line:
                lines = []

            # Creates a Course object
            elif "END:VEVENT" in line:
                # Removes the lines that shouldn't be in list
                data = self.__removeEntries(lines)
                course = Course()
                course.setValues(data)
                self.__classList.append( course )
            
            else:
                try:
                    # Fuck newlines
                    lines.append(line.strip("\n"))
                except:
                    pass
    
    
if __name__ == "__main__":
    with open("../../data/data.ics") as file:
        extractor = Extractor(ignore = {"UID","DTSTAMP","LOCATION"})
        extractor.extractFromFile(file)

        if( len(extractor.getClassList()) == 0):
            print("\nThe list is empty.")
            print("The program didn't have any data to extract.")
            print("Looks like you don't have any classes this week.\n")

            for course in extractor.getDummyList():
                course.printValues()

        else:
            for classes in extractor.getClassList():
                classes.printValues()
                print("\n")




