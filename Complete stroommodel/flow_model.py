from outward_flow_csm import outward_flow
from converter_csm import csv_to_adjacency_list
import random
import asyncio
import csv
from asyncio import Lock
from scipy.stats import beta
import os
import pandas
import copy
from asyncio import Lock

'''#functie voor het overzichtelijk printen van een graaf
def print_graph(graph):
    print('graph = {')
    for node, edges in graph.items():
        print(f'    {node}', end=' :  [    ')
        for edge in edges:
            print(f'[{edge[0]}, {edge[1]}]', end=',    ')
        print('],')
    print('}')'''

def divide(m, period, starting_rooms, ending_rooms):
    capacity_starting_rooms = [[room, max_capacity, 0] for room, max_capacity in starting_rooms]
    capacity_ending_rooms = [[room, max_capacity, 0] for room, max_capacity in ending_rooms]
    students = 0
    division = {room : [0,[]] for room, max_capacity in starting_rooms}
    while students < m:
        index_starting_room = random.randint(0, len(capacity_starting_rooms)-1) 
        index_ending_room = random.randint(0, len(capacity_ending_rooms)-1) 
        if capacity_starting_rooms[index_starting_room][2] < capacity_starting_rooms[index_starting_room][1] :
            if capacity_ending_rooms[index_ending_room][2] < capacity_ending_rooms[index_ending_room][1]:
                capacity_starting_rooms[index_starting_room][2] += 1  
                capacity_ending_rooms[index_ending_room][2] += 1  
                students += 1  
                division[capacity_starting_rooms[index_starting_room][0]][1].append(capacity_ending_rooms[index_ending_room][0])
            else: capacity_ending_rooms.pop(index_ending_room)
        else: capacity_starting_rooms.pop(index_starting_room)
    for room in division:
        division[room][0] = float(round((beta.rvs(2,2))*period, 2))
    return division

'''#prompt ter inzage van de willekeurige verdeling personen en vertrektijden
division = divide(859, 180, starting_rooms, ending_rooms)
for room, div in division.items():
    print('lokaal : [wachttijd deur openen, [lijst bestemmingen]]')
    print(f'{room} : {div}')
    print()'''

async def run_model(graph_lock, graph, m, tleave, deltatime, period, starting_rooms, ending_rooms, timeframe, model_nr):
    tasks = []  
    division = divide(m, period, starting_rooms, ending_rooms)
    for room, div in division.items():
        task = asyncio.create_task(outward_flow(graph_lock, div[0], room, div[1], graph, tleave, deltatime)) 
        tasks.append(task)  
    output_file = './Complete stroommodel/output.csv'
    if not os.path.exists(output_file):
        with open(output_file, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['t'])
            for i in range(1, timeframe + 1):
                csv_writer.writerow([i])
    editable_output_file = pandas.read_csv(output_file)
    busiest_graph = await indicator(graph_lock, graph, deltatime, model_nr, timeframe, editable_output_file)
    for task in tasks:
        task.cancel() 
    editable_output_file.to_csv(output_file, index=False)
    print(f'model nr. {model_nr} is done running')
    return busiest_graph

async def indicator(graph_lock, graph, deltatime, model_nr, timeframe, editable_output_file):
    current_highest_total_people = 0
    async with graph_lock:
        busiest_graph = copy.deepcopy(graph)
    t = 0
    column = []
    while t < timeframe:
        t+=1
        print(t, end=',')
        total_people = 0
        async with graph_lock:
            for room, connections in graph.items():
                for connection in connections:
                    total_people += connection[3]
        total_people /= 2
        if(total_people > current_highest_total_people):
            current_highest_total_people = total_people
            async with graph_lock:
                busiest_graph = copy.deepcopy(graph)
        column.append(total_people)
        await asyncio.sleep(deltatime)  
    editable_output_file[model_nr] = column
    return busiest_graph

async def monte_carlo(graph_file, m, tleave, deltatime, period, starting_rooms, ending_rooms, timeframe, sample_amount):
    graph_lock = Lock()
    sample_graphs = []
    for model_nr in range(1, sample_amount + 1):
        graph = csv_to_adjacency_list(graph_file)
        sample_graph = await run_model(graph_lock, graph, m, tleave, deltatime, period, starting_rooms, ending_rooms, timeframe, model_nr)
        sample_graphs.append(sample_graph)
    monte_carlo_graph = {}
    for node, edges in sample_graphs[0].items():
        mc_edges = []
        for index, edge in enumerate(edges):
            sum_weight = sum(sampled_graph[node][index][4] for sampled_graph in sample_graphs)
            mc_weight = round(sum_weight / len(sample_graphs), 2)
            mc_edges.append([edge[0], mc_weight])
        monte_carlo_graph[node] = mc_edges
    return monte_carlo_graph

'''#van klas naar klas
starting_rooms = [(28, 32), (29, 32), (30, 32), (32, 32), (39, 32), (40, 32), (45, 32), (47, 32), (48, 32), 
(52, 32), (67, 32), (68, 32), (92, 32), (89, 32), (88, 32), (87, 32), (78, 32), (79, 32), (75, 32), (74, 32), 
(96, 32), (100, 32), (103, 32), (104, 32), (112, 32), (113, 32), (115, 32), (116, 32), (133, 32), (134, 32), 
(135, 32), (136, 32), (146, 32), (147, 32)]
ending_rooms = starting_rooms
period = 180
m = 859
tleave = 1
deltatime = 2
graph_file = './Complete stroommodel/double_weighted_graph_csm.csv'
timeframe = 300
sample_amount = 10
resulting_graph = asyncio.run(monte_carlo(graph_file, m, tleave, deltatime, period, starting_rooms, ending_rooms, timeframe, sample_amount))
print_graph(resulting_graph)'''

'''#van start dag naar klas 
ending_rooms = [(28, 32), (29, 32), (30, 32), (32, 32), (39, 32), (40, 32), (45, 32), (47, 32), (48, 32), 
(52, 32), (67, 32), (68, 32), (92, 32), (89, 32), (88, 32), (87, 32), (78, 32), (79, 32), (75, 32), (74, 32), 
(96, 32), (100, 32), (103, 32), (104, 32), (112, 32), (113, 32), (115, 32), (116, 32), (133, 32), (134, 32), 
(135, 32), (136, 32), (146, 32), (147, 32)]
starting_rooms = [(3, 400), (11, 130), (21, 70)]
period = 240
m = 600
tleave = .3
deltatime = 2
graph_file = './Complete stroommodel/double_weighted_graph_csm.csv'
timeframe = 400
sample_amount = 10
resulting_graph = asyncio.run(monte_carlo(graph_file, m, tleave, deltatime, period, starting_rooms, ending_rooms, timeframe, sample_amount))
print_graph(resulting_graph)'''

'''#van klas naar pauze
starting_rooms = [(28, 32), (29, 32), (30, 32), (32, 32), (39, 32), (40, 32), (45, 32), (47, 32), (48, 32), 
(52, 32), (67, 32), (68, 32), (92, 32), (89, 32), (88, 32), (87, 32), (78, 32), (79, 32), (75, 32), (74, 32), 
(96, 32), (100, 32), (103, 32), (104, 32), (112, 32), (113, 32), (115, 32), (116, 32), (133, 32), (134, 32), 
(135, 32), (136, 32), (146, 32), (147, 32)]
ending_rooms = [(19, 46), (22, 46), (24, 46), (8, 46), (9, 46), (2, 46), (60, 46), (62, 46), (66, 46), (69, 46), 
(43, 46), (85, 46), (127, 46), (76, 46), (138, 46), (147, 46), (1, 46), (58, 46), (125, 46)]
period = 180
m = 859
tleave = 1
deltatime = 2
graph_file = './Complete stroommodel/double_weighted_graph_csm.csv'
timeframe = 300
sample_amount = 10
resulting_graph = asyncio.run(monte_carlo(graph_file, m, tleave, deltatime, period, starting_rooms, ending_rooms, timeframe, sample_amount))
print_graph(resulting_graph)'''