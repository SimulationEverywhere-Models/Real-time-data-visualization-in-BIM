# Forge - Kaizen Data Integration Scripts

These scripts and files are designed to help pull data from Coopertree Analytics Kaizen service and format it into data that can be read by Autodesk Forges' Hyperion Reference App

## List of files
**Script files**

- **HSB.xlsx** and **CB.xlsx** These files are used to define the relation between building sensor properties and their trendlog address
- **CBdata.json** and **HSBdata.json**: These files contain a dictionary of different sensor properties and list which rooms have data regarding that property
- **CBjson.txt** A json string that contains a list of rooms in a given model, and the position of those rooms
- **RsData.csv** A csv file containing descriptions of device properties used when creating a new device model
- **repeat_import.py** script that will update the individual device csv files based on
- **control_variables.py** file has paths to the users

- **TL_Listing.py** in progress work on downloading list of trendlogs from Kaizen
- **MassAdd.py**  script that allows you to create device-models and devices in the respsective jsons
- **Sort.py**  Sorts through HSB.xlsxl and CB.xlsx to generate the sorted lists in CBdata.json and HSBdata.json

**Notes Files**
- **presentationSlides.pptx** Slides outlining basic operation of the HRA using CSV adapter and out the updating csv files work
- **Notes.docx** Compilation of notes about edits made to the HRA itself and some quirks of the scripts
- **position extraction notes.txt** contains notes on how to get list of room positions from Reference app

## Prerequisites
Requires at least python3.9.6
The python package "pandas", needed to perform the manipulation of the API data and reading/writing to  the csv/excel files, use "pip install pandas" to install

## Setup
To install download folder into the same directory as the reference app, if reference app is in different location, adjust path variables in control_variable.py to compensate

## Running the scripts

### Adding new devices and creating new device models
**Operating steps**
1. Make sure that the data.json and xlsx files are up todate regarding sensor data
   1. If files are not up to date, first update the xlsx file with the data from Kaizen
   2. Then update the data.json by running Sort.py
2. If model has been changed or updated, make sure to update json string with the new positional data
3. Navigate into the top git folder
4. run MassAdd.py, you should receive a prompt asking for a device property
5. When prompted indicate which property's sensor you want to update
6. Let the script run, it should automatically generate a device model and accompanying devices

### Updating/Creating Device CSV files
1. Make sure that the devices.json and the device_models.json are up to date with the devices you want
   1. If the jsons are not updated refer to Adding new devices and creating new device models
2. Run repeat_import.py
3. When System displays "update finished" you can stop update loop with control C 




