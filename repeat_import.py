import urllib.request
import json
import control_variables
import re
import pandas as pd
from datetime import datetime as date, timedelta
import time


def get_data(tl, start, end, interimFrame, header):
    '''
    Function is responsible for getting the data from Kaizen and write it to
    the interim frame
    Inputs:
    tl (str) = trend log address used in api
    start (str) = formatted datestring for start of timeperiod of data
    end (str) = formatted datestring for end of timeperiod of data
    intertimFrame (dataframe) =  dataframe for holding new sensor data before adding to device csv
    header (str) = property that is being fetched
    '''
    startTime = time.time()
    #request to get data
    url = 'https://kaizen.coppertreeanalytics.com/public_api/api/get_tl_data_start_end?&api_key=1351f2dddfc940e2&start='+ start + '&end=' + end + '&data=raw&tl=' + tl

    web = urllib.request.urlopen(url)
    
    print(url)
    getTime = time.time()-startTime
    print("Get time is ")
    print(getTime)
    # load the request data into json file
    Data = json.load(web)
    loadTime = time.time()-startTime-getTime
    print("Load time is ")
    print(loadTime)
    # load the json into dataframe, and then add it to the interim frame
    df = pd.json_normalize(Data)
    frameTime = time.time()-startTime-loadTime-getTime
    print("Frame time is ")
    print(frameTime)
    if df.empty:
        print("No data is found in range " + start + " to " + end)
        return
    interimFrame[['time',header]] = df[['ts','v']]

def update_devices():
    '''
    This script will loop thorugh devices.json and update/create the csv
    file for each device
    '''
    # get current time for upper bound of fetching data
    now = date.now()
    nowString = now.strftime("%Y-%m-%dT%H:%M:%S")
    # open json files used by server/gateways
    with open(control_variables.json_path + "\\devices.json") as jsonFile:
        devices = json.load(jsonFile)
        jsonFile.close()

    with open(control_variables.json_path + "\\device-models.json") as jsonFile:
        devices_models = json.load(jsonFile)
        jsonFile.close()
    # open excell sheet with headers used
    TLsheet_dict = {"CB_": pd.read_excel("CB.xlsx"),"HS_":pd.read_excel("HSB.xlsx")}
    # get data on a device by device basis
    for i in devices:
        # get the property id headers for the device type
        propList = []
        for model in devices_models:
            if model["deviceModelId"] == i["deviceModelId"]:
                for property in model["deviceProperties"]:
                    propList.append(property["propertyId"])

        # now for each device get the header names
        for device in i["deviceInfo"]:
            headerDict = {}
            for prop in propList:
                headerDict[prop] = '{1}{0}'.format(prop,re.search('\w+\d_',device["id"]).group())
            print(headerDict)
            # use 
            TLsheet = TLsheet_dict[device["id"][0:3]]
            # if csv already exists get last used time from csv else use current time -1 year
            try:
                excel_data = pd.read_csv(control_variables.hyperion_path + device["id"] + ".csv")
                endTime = excel_data.tail(1).iloc[0]["time"][:-1]
                print(endTime)
            except FileNotFoundError:
                print("File not Found")
                excel_data = pd.DataFrame()
                endTime = (now - timedelta(days = 730)).strftime("%Y-%m-%dT%H:%M:%S")
            #Interim dataframe used to hold data before being added to excel_data frame
            to_add = pd.DataFrame()
            for header in headerDict:
                #get the addresss of the item to read
                print("Getting data")
                print(headerDict[header])
                test = TLsheet.loc[TLsheet['Name'] == headerDict[header]]
                print(test)
                # if there is a header, get data from Kaizen and add to interim frame
                if not test.empty:
                    get_data(test.iloc[0]["Object Reference"],endTime,nowString,to_add, header)
            # if interim frame has data to add, add data and then resave csv file
            if not to_add.empty:
                for count, value in enumerate(to_add["time"]):
                    to_add.at[count,"time"] = value + "Z"
                excel_data = pd.concat([excel_data,to_add[1:]], ignore_index=True)
                excel_data.to_csv(control_variables.hyperion_path + device["id"] + ".csv",index=False)

def updateLoop ():
    while True:
        print("updating")
        update_devices()
        print("update Finished")
        time.sleep(20)

if __name__ == "__main__":
    updateLoop()