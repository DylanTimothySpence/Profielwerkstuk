from trafficflow import outward_flow
from converter_traffic import csv_to_adjacency_list
import random
import asyncio
import csv
from asyncio import Lock
from scipy.stats import beta

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
division = divide(859, 120, starting_rooms, ending_rooms)
for room, div in division.items():
    print('lokaal : [wachttijd deur openen, [lijst bestemmingen]]')
    print(f'{room} : {div}')
    print()'''

async def wait_for_open(waittime, source_node, target_nodes, graph, tleave, deltatime):
    await asyncio.sleep(waittime*deltatime)
    await outward_flow(source_node, target_nodes, graph, tleave, deltatime)

async def run_model(graph, m, tleave, deltatime, period, starting_rooms, ending_rooms):
    global running
    running = True
    division = divide(m, period, starting_rooms, ending_rooms)
    tasks = []
    asyncio.create_task(indicator(deltatime)) 
    for room, div in division.items():
        task = asyncio.create_task(wait_for_open(div[0], room, div[1], graph, tleave, deltatime)) 
        tasks.append(task)
    await asyncio.gather(*tasks)
    print('model done running')
    running = False

#de indicator geeft de mogelijkheid om op gekozen tijden de graaf te printen, of iets anders
#voor gebruik van de functie moeten alle #'s worden weggehaald
async def indicator(deltatime):
    t = 0
    with open('./traffic_total/outputpt.csv', 'w', newline='') as csvfile: 
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['t','Le','n'])
        while running and t<250:
            '''if t == take_graph:
                async with Lock():
                    for room, connections in graph.items():
                        print(room, end=" : [")
                        for i, connection in enumerate(connections):
                            latency = connection[4] 
                            connected_node = connection[0]
                            print(f'[{connected_node}, {latency}]', end=", ")
                        print("],")'''
            csv_writer.writerow([t, round(graph[38][3][4], 2), graph[38][3][3]])

            await asyncio.sleep(deltatime)
            t +=1
            print(t)

#van klas naar klas
starting_rooms = [(28, 32), (29, 32), (30, 32), (32, 32), (39, 32), (40, 32), (45, 32), (47, 32), (48, 32), 
(52, 32), (67, 32), (68, 32), (92, 32), (89, 32), (88, 32), (87, 32), (78, 32), (79, 32), (75, 32), (74, 32), 
(96, 32), (100, 32), (103, 32), (104, 32), (112, 32), (113, 32), (115, 32), (116, 32), (133, 32), (134, 32), 
(135, 32), (136, 32), (146, 32), (147, 32)]
ending_rooms = starting_rooms
period = 120
m = 859
take_graph = 120
graph = csv_to_adjacency_list('./traffic_total/hlgraph_traffic.csv')
asyncio.run(run_model(graph, m, 1, 3, period, starting_rooms, ending_rooms))
'''#van start dag naar klas (omgekeerd gemodelleerd)
#VERWIJDER DE ZIJDE VAN DE GLIJBAAN IN DE GRAAF: 85,84,2.73,4.79,86,4.21,4.79,7,13.04,0.85,,, --> 85,84,2.73,4.79,86,4.21,4.79,,,,,,
starting_rooms = [(28, 32), (29, 32), (30, 32), (32, 32), (39, 32), (40, 32), (45, 32), (47, 32), (48, 32), 
(52, 32), (67, 32), (68, 32), (92, 32), (89, 32), (88, 32), (87, 32), (78, 32), (79, 32), (75, 32), (74, 32), 
(96, 32), (100, 32), (103, 32), (104, 32), (112, 32), (113, 32), (115, 32), (116, 32), (133, 32), (134, 32), 
(135, 32), (136, 32), (146, 32), (147, 32)]
ending_rooms = [(3, 400), (11, 130), (21, 70)]
period = 240
m = 600
take_graph = 180
asyncio.run(run_model(graph, m, 1, 5, period, starting_rooms, ending_rooms))'''
'''#van klas naar pauze
starting_rooms = [(28, 32), (29, 32), (30, 32), (32, 32), (39, 32), (40, 32), (45, 32), (47, 32), (48, 32), 
(52, 32), (67, 32), (68, 32), (92, 32), (89, 32), (88, 32), (87, 32), (78, 32), (79, 32), (75, 32), (74, 32), 
(96, 32), (100, 32), (103, 32), (104, 32), (112, 32), (113, 32), (115, 32), (116, 32), (133, 32), (134, 32), 
(135, 32), (136, 32), (146, 32), (147, 32)]
ending_rooms = [(19, 46), (22, 46), (24, 46), (8, 46), (9, 46), (2, 46), (60, 46), (62, 46), (66, 46), (69, 46), 
(43, 46), (85, 46), (127, 46), (76, 46), (138, 46), (147, 46), (1, 46), (58, 46), (125, 46)]
period = 180
m = 859
take_graph = 150
asyncio.run(run_model(graph, m, 1, 5, period, starting_rooms, ending_rooms))'''