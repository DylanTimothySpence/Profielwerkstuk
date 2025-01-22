import asyncio
from dijkstra_traffic import run_algorithm
from asyncio import Lock

latency_lock = Lock()

def latency_function(x, w, n):
    if n > 0:
        kjam = 5.4
        vf = 1.34
        e = 2.718281828
        gamma = 1.913
        L = w / (1 - (e ** (-(gamma) * (((x * w * vf) / n) - (1 / kjam)))))
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

async def outward_flow(source_node, target_nodes, graph, tleave, deltatime):
    tasks = []
    for location in target_nodes:
        path = run_algorithm(graph, source_node, location, 1.34)[0]
        task = asyncio.create_task(walk_route(path, graph, deltatime)) 
        tasks.append(task)
        await asyncio.sleep(tleave*deltatime)
    await asyncio.gather(*tasks)