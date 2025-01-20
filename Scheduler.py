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

Bot_vertices = dict.fromkeys(Time)
Top_vertices = dict.fromkeys(Meetings.keys())

network = {"nodes":{}, "edges":{}}

Nodes = pd.DataFrame()
Arcs = pd.DataFrame()

## Initialize Nodes:
for t in Time:
    new_row = pd.DataFrame({"Name": [t], "Imbalance": [0]})
    Nodes = pd.concat([Nodes, new_row], ignore_index=True)
    network["nodes"][t] = {"b":0}

## Add to Arcs and Nodes
first = Time[0]
last = Time[-1]
for i in range(len(Time)):
    if Time[i] != last:
        new_row = pd.DataFrame({"Start": Time[i], "End":Time[i + 1], "UpperBound":[1], "Lowerbound":[0], "Value":[0]})
        Arcs = pd.concat([Arcs, new_row], ignore_index=True)
        network["edges"][(Time[i], Time[i + 1])] = {"u":1, "c":0}

for meet in Meetings:
    ## For Nodes
    new_row = pd.DataFrame({"Name": [meet], "Imbalance": [1]})
    Nodes = pd.concat([Nodes, new_row], ignore_index=True)
    network["nodes"][meet] = {"b":1}
    start = Meetings[meet][time][0]
    end = Meetings[meet][time][1]
    Nodes.loc[Nodes['Name'] == end, "Imbalance"] -= 1
    network["nodes"][end]["b"] -= 1
    
    value = -1 * Meetings[meet][val]
    ## For Arcs
    new_row = pd.DataFrame({"Start": meet, "End": start, "UpperBound":[1], "Lowerbound":[0], "Value":[value]})
    Arcs = pd.concat([Arcs, new_row], ignore_index=True)
    network["edges"][(meet, start)] = {"u": 1, "c": value}
    new_row = pd.DataFrame({"Start": meet, "End": end, "UpperBound":[1], "Lowerbound":[0], "Value":[0]})
    Arcs = pd.concat([Arcs, new_row], ignore_index=True)
    network["edges"][(meet, end)] = {"u": 1, "c": 0}
    
Nodes.to_csv("Nodes.csv", index=False)
Arcs.to_csv("Arcs.csv", index=False)


## Modified from https://mobook.github.io/MO-book/notebooks/04/02-mincost-flow.html

## pip install pyomo
## pip install highspy

solver = 'appsi_highs'

from pyomo.environ import *
import pyomo.environ as pyo
SOLVER = pyo.SolverFactory(solver)

def mincostflow(network):
    model = pyo.ConcreteModel("Minimum cost flow")

    model.x = pyo.Var(network["edges"], domain=pyo.NonNegativeReals)

    @model.Objective(sense=pyo.minimize)
    def objective(m):
        return sum(data["c"] * m.x[e] for e, data in network["edges"].items())

    @model.Expression(network["nodes"])
    def incoming_flow(m, j):
        return sum(m.x[i, j] for i in network["nodes"] if (i, j) in network["edges"])

    @model.Expression(network["nodes"])
    def outgoing_flow(m, j):
        return sum(m.x[j, i] for i in network["nodes"] if (j, i) in network["edges"])

    @model.Constraint(network["nodes"])
    def flow_conservation(m, j):
        return m.outgoing_flow[j] - m.incoming_flow[j] == network["nodes"][j]["b"]

    @model.Constraint(network["edges"])
    def flow_upper_bound(m, *e):
        return m.x[e] <= network["edges"][e]["u"]

    return model


model = mincostflow(network)
SOLVER.solve(model)
######################################## End ############################################

## Output the result as a whole
if __name__ == "__main__":
    model.pprint()


Tup = []
for meet in Meetings:
    tup = (meet, Meetings[meet][time][0])
    Tup.append(tup)


print("In our model, we suggest to attempt to the following meetings:")
if __name__ == "__main__":
    print("__OUTPUT FOR TESTING PURPOSES__")
Attend_to = []
for var in model.component_objects(Var, active=True):
    for index in var:
        if value(var[index]) == 1 and index in Tup:
            ## Test about the correctness of the meeting selection
            if __name__ == "__main__":
                print(f'{index} = {value(var[index])}')
            Attend_to.append(index[0])

Returned_list = [["Name", "Start", "End", "Value"]]
for meet in Attend_to:
    row = [meet, Meetings[meet][time][0], Meetings[meet][time][1], Meetings[meet][val]]
    Returned_list.append(row)

print(Attend_to)

import csv
with open('Out.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(Returned_list)    
