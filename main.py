#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

import lib.utils.downloader as downloader
import lib.utils.extractor as extractor
import lib.utils.formater as formater
import lib.utils.filters as filters
import lib.utils.drawer as drawer
import lib.course as course

import os, sys, inspect, time, getopt, json, datetime
from pathlib import Path

def checkDownloadTime():
    '''
    Checks if the calendar was downloaded this week. If not, saves new week in process_data.json and returns True.
    '''

    date = datetime.datetime.now()
    week = datetime.date( date.year, date.month, date.day ).isocalendar()[1]
    path = Path.cwd() / 'config' / 'process_data.json'

    with open( path , 'r') as file:
        data = json.load(file)
    
    if( data["week"] < week  ):
        
        data["week"] = week
        with open( path, 'w') as file:
            json.dump(data, file)

        return True

    return False


if __name__ == "__main__":

    # Check if it wasn't a force run ( so not manually wanting to download data )
    if "force_download" not in sys.argv[1:]:
        if( not checkDownloadTime() ):
            sys.exit()

    print("\n\t---- Downloading ----" )
    downloadPath = os.path.abspath(os.path.join( os.getcwd(), "data"))
    download = downloader.Download("RIT UN", downloadPath)  
    download.setUp()
    download.downloadUrnik()
    download.stop()

    print("\n\t---- Extraction ----" )
    with open("data/data.ics") as file:
        print("Start Extracting file")
        extractor = extractor.Extractor({"UID","DTSTAMP","LOCATION"})
        extractor.extractFromFile(file)
        
        print("Successfuly extracted file")
        extrData = extractor.getClassList()


    time.sleep(1)
    print("\n\t---- Formatting ----" )
    files = open("config/userData.json")
    errorStr = ""
    extrctDummy = False
    print("Starting to format raw data")
    
    if(len(extrData) == 0):
        print("No data to format. Looks like you have a free week.")
        errorStr = " (even thought it's nothing)."
        extrData = extractor.getDummyList()
        extrctDummy = True
    
    formater = formater.Formater(extrData, files)

    if(extrctDummy):
        formater.createDummySchedual()
    else:
        formater.createSchedual()

    schedual = formater.getSchedual()

    time.sleep(1)
    print("\n\t---- Writting to file ----" )
    print("Writing formated data into file" + errorStr)
    
    with open("data/urnik.txt", "w") as file:
        file.seek(0)
        file.truncate()
        for i in schedual:
            file.write(i + "\n")
    
    print("\n\t---- Finished ----" )
