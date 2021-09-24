import json
import sys
import control_variables
import pandas as pd
from datetime import datetime as Formatter


# Kaizen_Names= ["RMH","CO2","CMD","WMD","RAD_MOD","RMT_SP","BLIND_POS_AV","LIGHT_AVG_LUX_LEVEL_AV","VAV_system_SCH_BV","MD_OCC_BV","VAV_OAT_XFER_AV","RMT_CO","VAV_RAT","LIGHT_kW_AV","LIGHT_AMP","RMT","LIGHT_ON","LIGHT_OFF","VAV_FLOW_AV",
# "VAV_FLOW_SP","PERIM_HTG_DELTA_T_AV","WINDOW_CONTACT_BV","VAV_CTRL_MODE_MV","PERIM_HTG_DELTA_T_CO","MPC","sMPC","VAV_SAT_SP","VAV_SAT","VAV_DP_CO","SAT_CO","LIGHT_DIM","VAV_system_UNIT_MODE_BV","LIGHT_OUTPUT_AV","LIGHT_LAST_VALUE_AV""DC","TEMP_PERM_BV","GENERAL_PERM_BV",
# "VAV_system_UNIT_MODE_BV","LUX1","LUX2","LUX3","LIGHT_kWh_AT","VAV_RHC_MOD","VAV_DMP_MOD","VAV_DP_SP","VAV_FBK","VAV_DP"]

df = pd.read_csv("Data_Continous.csv")

with open(control_variables.json_path + "\\test-devices.json") as jsonFile:
    devices = json.load(jsonFile)
    jsonFile.close()

with open(control_variables.json_path + "\\test-device-models.json") as jsonFile:
    devices_models = json.load(jsonFile)
    jsonFile.close()
# for each device type inside devices.json

#Find columns with no data in it and remove them
dropset = set()
for column in df.columns:
    if df[column].isnull().values.any():
        dropset.add(column)
ndf = df.drop(columns=list(dropset))
#Change Timestamp to time and then reformat the time strings
df = ndf.rename(columns={"Var1":"time"})
for count, value in enumerate(df["time"]):
    text = Formatter.isoformat(Formatter.strptime(value,"%m/%d/%Y %H:%M")) + "Z"
    df.at[count,"time"] = text
    
for i in devices:
    print(i["deviceModelId"] + " model type")
    # get the property id headers for the device type
    propList = []
    for model in devices_models:
        if model["deviceModelId"] == i["deviceModelId"]:
            for property in model["deviceProperties"]:
                propList.append(property["propertyName"])
    print(propList)
    # now for each device get the header names
    for device in i["deviceInfo"]:
        headerList = propList.copy()
        headerList = ['{1}_{0}'.format(header,device["name"]) for header in headerList]
        headerList.insert(0,"time")
        print(headerList)
        ndf = df.filter(headerList)
        ndf.to_csv( device["id"] + ".csv",index=False)

