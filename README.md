# Forge - Kaizen Data Integration Scripts

These scripts and files are designed to help pull data from Coopertree Analytics Kaizen service and format it into data that can be read by Autodesk Forges' Hyperion Reference App

## List of files

- **HSB.xlsx** and **CB.xlsx** These files are used to define the relation between building sensor properties and their trendlog address
- **CBdata.json** and **HSBdata.json**: These files contain a dictionary of different sensor properties and list which rooms have data regarding that property
- **CBjson.txt** A json string that contains a list of rooms in a given model, and the position of those rooms
- **RsData.csv** A csv file containing descriptions of device properties used when creating a new device model
- **repeat_import.py** script that will update the individual device csv files based on
- **control_variables.py** file has paths to the users
- **position extraction notes.txt** contains notes on how to get list of room positions from Reference app
- **TL_Listing.py** in progress work on downloading list of trendlogs from Kaizen

## Prerequisites
The python package "pandas", needed to perform the manipulation of the 

## Setup
To install download folder into the same directory as the reference app



