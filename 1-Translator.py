import pandas as pd

time = "time"

val = "val"

Meetings = {"1": {time: ["08:10", "13:50"], val: 10}, "2": {time: ["09:50", "10:50"], val: 15}, 
            "3": {time: ["13:15", "14:50"], val: 12},  "4": {time: ["13:15", "16:50"], val: 19}, 
            "5": {time: ["08:10", "14:50"], val: 25}}

## We first create a list of time (bus stops in the original network)

Time = []
for key in Meetings:
    Time.append(Meetings[key][time][0])
    Time.append(Meetings[key][time][1])

## Refine list Time
Time.sort()

Time = list(dict.fromkeys(Time))
        
print(Time)

Bot_vertices = dict.fromkeys(Time)
Top_vertices = dict.fromkeys(Meetings.keys())

Nodes = pd.DataFrame()
Arcs = pd.DataFrame()

## Initialize Nodes:
for t in Time:
    new_row = pd.DataFrame({"Name": [t], "Imbalance": [0]})
    Nodes = pd.concat([Nodes, new_row], ignore_index=True)

## Add to Arcs and Nodes
first = Time[0]
last = Time[-1]
for i in range(len(Time)):
    if Time[i] != last:
        new_row = pd.DataFrame({"Start": Time[i], "End":Time[i + 1], "UpperBound":[1], "Lowerbound":[0], "Value":[0]})
        Arcs = pd.concat([Arcs, new_row], ignore_index=True)

for meet in Meetings:
    ## For Nodes
    new_row = pd.DataFrame({"Name": [meet], "Imbalance": [1]})
    Nodes = pd.concat([Nodes, new_row], ignore_index=True)
    start = Meetings[meet][time][0]
    end = Meetings[meet][time][1]
    Nodes.loc[Nodes['Name'] == end, "Imbalance"] -= 1
    
    value = -1 * Meetings[meet][val]
    ## For Arcs
    new_row = pd.DataFrame({"Start": meet, "End": start, "UpperBound":[1], "Lowerbound":[0], "Value":[value]})
    Arcs = pd.concat([Arcs, new_row], ignore_index=True)
    new_row = pd.DataFrame({"Start": meet, "End": end, "UpperBound":[1], "Lowerbound":[0], "Value":[0]})
    Arcs = pd.concat([Arcs, new_row], ignore_index=True)
    
Nodes.to_csv("Nodes.csv")
Arcs.to_csv("Arcs.csv")
    




