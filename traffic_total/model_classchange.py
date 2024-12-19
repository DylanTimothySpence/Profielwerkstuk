from trafficflow import oppad
from trafficflow import flow
from converter_traffic import csv_to_adjacency_list
import random

graph = csv_to_adjacency_list('./traffic_total/trafficgraph.csv')
capacity = {
    28 : 0 ,
    29 : 0 ,
    30 : 0 ,
    32 : 0 ,

    39 : 0 ,
    40 : 0 ,
    45 : 0 ,
    47 : 0 ,
    48 : 0 ,
    52 : 0 ,
    67 : 0 ,
    68 : 0 ,

    92 : 0 ,
    89 : 0 ,
    88 : 0 ,
    87 : 0 ,
    78 : 0 ,
    79 : 0 ,
    75 : 0 ,
    74 : 0 ,

    96 : 0 ,
    100 : 0 ,
    103 : 0 ,
    104 : 0 ,
    112 : 0 ,
    113 : 0 ,
    115 : 0 ,
    116 : 0 ,

    133 : 0 ,
    134 : 0 ,
    135 : 0 ,
    136 : 0 ,
    146 : 0 ,
    147 : 0 ,
}

def fill_classes():
    rooms = list(capacity.keys())
    total_students = 860
    while total_students > 0:
        room = random.choice(rooms)        
        if capacity[room] < 32:
            capacity[room] += 1  
            total_students -= 1  

fill_classes()
print(capacity)