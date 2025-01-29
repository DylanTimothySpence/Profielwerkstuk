import asyncio
import csv
from traffic_casus.dijkstra_casus import run_algorithm
from traffic_casus.converter_casus import csv_to_adjacency_list
from asyncio import Lock

latency_lock = Lock()

def latency_function(x, w, n):
    if n > 0:
        kjam = 5.4
        vf = 1.34
        e = 2.718281828
        gamma = -1.913
        L = w / (1 - (e ** (gamma * (((x * w * vf) / n) - (1 / kjam)))))
        if L < 0: 
            L = float('inf')
    else:
        L = w
    return L

async def walk_route(path, graph, deltatime):
    for i, node in enumerate(path):
        if i < len(path) - 1:
            next_node = path[i + 1]
            async with latency_lock:
                for index_connection, connection in enumerate(graph[node]): 
                    if connection[0] == next_node:
                        connection[3] += 1
                        w = connection[1] 
                        x = connection[2]
                        Le = latency_function(x, w, connection[3])
                        connection[4] = Le
                        store_index_connection = index_connection 
                        break
                undirected = False
                for index_connection, connection in enumerate(graph[next_node]): 
                    if connection[0] == node: 
                        connection[3] += 1
                        connection[4] = latency_function(x, w, connection[3])
                        store_index_reverse_connection = index_connection 
                        undirected = True
                        break
            await asyncio.sleep(Le*deltatime)
            async with latency_lock:
                graph[node][store_index_connection][3] -=1 
                Le_after = latency_function(x, w, graph[node][store_index_connection][3])
                graph[node][store_index_connection][4] =  Le_after
                if undirected: 
                    graph[next_node][store_index_reverse_connection][3] -=1 
                    graph[next_node][store_index_reverse_connection][4] = Le_after

async def flow(s, t, m, deltatime, tleave, graph):
    tasks = []
    for n in range(1, m + 1):
        path = run_algorithm(graph, s, t, 1.34)[0]
        task = asyncio.create_task(walk_route(path, graph, deltatime)) 
        tasks.append(task)
        await asyncio.sleep(tleave * deltatime)  
    await asyncio.gather(*tasks)
    global run_indicator
    run_indicator = False 


#de indicator kan gebruikt worden om gegevens te verzamelen over de stroom
run_indicator = True #zet deze variabele op false als je de indicator niet wilt gebruiken
async def indicator(s, t, deltatime, graph): 
    with open('./traffic_casus/outputpt.csv', 'w', newline='') as csvfile: 
        csv_writer = csv.writer(csvfile)
        count = 0
        #header rows:
        #csv_writer.writerow(['t', (4,5), (5,6), (6,10),(10,7),(7,9),(9,8),(8,15),(15,13),(5,3),(3,1),(1,2),(2,0),(0,11),(11,12),(12,13),(13,14)])
        #csv_writer.writerow(['t', 'tijd trappenhuis', 'tijd conciërge'])
        while run_indicator: 
            '''#verzamelen totale tijden van beide paden 
            tijd_trappenhuis = round(((run_algorithm(graph, s, 7, 1.34))[1] + (run_algorithm(graph, 7, t, 1.34))[1]), 2)
            tijd_conciërge = round(((run_algorithm(graph, s, 2, 1.34))[1] + (run_algorithm(graph, 2, t, 1.34))[1]), 2)
            csv_writer.writerow([count, tijd_trappenhuis, tijd_conciërge])'''

            '''#verzamelen extra tijd op alle individuele zijden
            L1 = [round(graph[4][0][4],2), round(graph[5][1][4],2), round(graph[6][1][4],2), round(graph[10][1][4],2), round(graph[7][0][4],2), round(graph[9][1][4],2), round(graph[8][1][4],2), round(graph[15][0][4],2), round(graph[5][0][4],2), round(graph[3][0][4],2), round(graph[1][0][4],2), round(graph[2][1][4],2), round(graph[0][0][4],2), round(graph[11][1][4],2), round(graph[12][1][4],2),round(graph[14][0][4],2)]
            L2 = [graph[4][0][1], graph[5][1][1], graph[6][1][1], graph[10][1][1], graph[7][0][1], graph[9][1][1], graph[8][1][1], graph[15][0][1], graph[5][0][1], graph[3][0][1], graph[1][0][1], graph[2][1][1], graph[0][0][1], graph[11][1][1], graph[12][1][1],graph[14][0][1]]
            L3 = [round(a - b, 2) for a, b in zip(L1, L2)]
            csv_writer.writerow([count, *L3])'''

            '''#verzamelen aantal personen op alle individuele zijden
            L3 = [graph[4][0][3], graph[5][1][3], graph[6][1][3], graph[10][1][3], graph[7][0][3], graph[9][1][3], graph[8][1][3], graph[15][0][3], graph[5][0][3], graph[3][0][3], graph[1][0][3], graph[2][1][3], graph[0][0][3], graph[11][1][3], graph[12][1][3], graph[14][0][3]]
            csv_writer.writerow([count, *L3])'''

            await asyncio.sleep(deltatime) 
            print(count)
            count +=1
    if run_indicator: print('klaar')

async def main(s, t, m, deltatime, tleave, graph):
    await asyncio.gather(
        flow(s, t, m, deltatime, tleave, graph),
        indicator(s, t, deltatime, graph)
    )

'''#promt voor runnen van code, vul in: (beginpunt, eindpunt, aantal mensen, deltatime, tijd deur uit te gaan, graaf)
asyncio.run(main(5, 13, 100, 5, 1, csv_to_adjacency_list('./traffic_casus/casus_graph.csv'))) '''
