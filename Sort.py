from collections import defaultdict
import re
import pandas as pd
import json

reference = pd.read_excel("HSB.xlsx")
typeToRoom = defaultdict(lambda: [])
for index, row in reference.iterrows():
    x = re.search('([a-zA-Z0-9]+_[a-zA-Z0-9]+)_(\w+)',row[0])
    typeToRoom[x.group(2)].append(x.group(1))

with open('HSBdata.json', 'w') as fp:
    json.dump(typeToRoom, fp,  indent=4)