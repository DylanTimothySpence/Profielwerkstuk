from trafficflow import oppad
from trafficflow import flow
from converter_traffic import csv_to_adjacency_list
import random
import asyncio
from asyncio import Lock

graph = csv_to_adjacency_list('./traffic_total/trafficgraph.csv')
deltatime = 1

starting_rooms = [(28, 32), (29, 32), (30, 32), (32, 32), (39, 32), (40, 32), (45, 32), (47, 32), (48, 32), 
(52, 32), (67, 32), (68, 32), (92, 32), (89, 32), (88, 32), (87, 32), (78, 32), (79, 32), (75, 32), (74, 32), 
(96, 32), (100, 32), (103, 32), (104, 32), (112, 32), (113, 32), (115, 32), (116, 32), (133, 32), (134, 32), 
(135, 32), (136, 32), (146, 32), (147, 32)]

ending_rooms = starting_rooms

room_info = {
    # lokaal : [begincapaciteit, eindcapaciteit, tijd voor deur open, [(nr van ll, waar naartoe)]]
    28 : [0,0,0,[]],
    29 : [0,0,0,[]] ,
    30 : [0,0,0,[]] ,
    32 : [0,0,0,[]] ,

    39 : [0,0,0,[]] ,
    40 : [0,0,0,[]] ,
    45 : [0,0,0,[]] ,
    47 : [0,0,0,[]] ,
    48 : [0,0,0,[]] ,
    52 : [0,0,0,[]] ,
    67 : [0,0,0,[]] ,
    68 : [0,0,0,[]] ,

    92 : [0,0,0,[]] ,
    89 : [0,0,0,[]] ,
    88 : [0,0,0,[]] ,
    87 : [0,0,0,[]] ,
    78 : [0,0,0,[]] ,
    79 : [0,0,0,[]] ,
    75 : [0,0,0,[]] ,
    74 : [0,0,0,[]] ,

    96 : [0,0,0,[]] ,
    100 : [0,0,0,[]] ,
    103 : [0,0,0,[]] ,
    104 : [0,0,0,[]] ,
    112 : [0,0,0,[]] ,
    113 : [0,0,0,[]] ,
    115 : [0,0,0,[]] ,
    116 : [0,0,0,[]] ,

    133 : [0,0,0,[]] ,
    134 : [0,0,0,[]] ,
    135 : [0,0,0,[]] ,
    136 : [0,0,0,[]] ,
    146 : [0,0,0,[]] ,
    147 : [0,0,0,[]]
}

def divide(period, starting_rooms, ending_rooms):
    capacity_starting_rooms = [[room, max_capacity, 0] for room, max_capacity in starting_rooms]
    capacity_ending_rooms = [[room, max_capacity, 0] for room, max_capacity in ending_rooms]

    students = 0
    division = {room : [0,[]] for room, max_capacity in starting_rooms}
    while students < 860:
        index_starting_room = random.randint(0, len(capacity_starting_rooms)-1) 
        index_ending_room = random.randint(0, len(capacity_ending_rooms)-1) 

        if capacity_starting_rooms[index_starting_room][2] < capacity_starting_rooms[index_starting_room][1] :
            if capacity_ending_rooms[index_ending_room][2] < capacity_ending_rooms[index_ending_room][1]:
                capacity_starting_rooms[index_starting_room][2] += 1  
                capacity_ending_rooms[index_ending_room][2] += 1  
                students += 1  
                print(students)
                division[capacity_starting_rooms[index_starting_room][0]][1].append(capacity_ending_rooms[index_ending_room][0])
            else: capacity_ending_rooms.pop(index_ending_room)
        else: capacity_starting_rooms.pop(index_starting_room)
    for room in division:
        division[room][0] = random.randint(0, period)
    return division

'''
division = divide(120,starting_rooms,ending_rooms)
for room, div in division.items():
    print(f'{room} : {div}')
    print()'''

async def put_on_hold(waittime, s, target_nodes, graph, tleave, deltatime):
    await asyncio.sleep(waittime*deltatime)
    await flow(s, target_nodes, graph, tleave, deltatime)

async def run_model(graph, tleave, deltatime, period, starting_rooms, ending_rooms):
    division = divide(period, starting_rooms, ending_rooms)
    tasks = []
    for room, div in division.items():
        task = asyncio.create_task(put_on_hold(div[0], room, div[1], graph, tleave, deltatime)) 
        tasks.append(task)
    await asyncio.gather(*tasks)
    


