import asyncio
from dijkstra_traffic import run_algorithm
from asyncio import Lock

latency_lock = Lock()

def latencyfunction(x, w, n):
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

async def oppad(path, g, graph):
    for i, node in enumerate(path):
        if i < len(path) - 1:
            next_node = path[i + 1]
            async with latency_lock:
                for index_connection, connection in enumerate(graph[node]): 
                    if connection[0] == next_node:
                        connection[3] += g
                        w = connection[1] 
                        x = connection[2]
                        Le = latencyfunction(x, w, connection[3])
                        connection[4] = Le
                        store_index_connection = index_connection 
                        break
                for index_connection, connection in enumerate(graph[next_node]): 
                    if connection[0] == node:
                        connection[3] += g
                        connection[4] = latencyfunction(x, w, connection[3])
                        store_index_reverse_connection = index_connection 
                        break
            await asyncio.sleep(Le)
            async with latency_lock:
                graph[node][store_index_connection][3] -=g 
                graph[node][store_index_connection][4] = latencyfunction(x, w, graph[node][store_index_connection][3])
                graph[next_node][store_index_reverse_connection][3] -=g 
                graph[next_node][store_index_reverse_connection][4] = latencyfunction(x, w, graph[node][store_index_reverse_connection][3])

async def flow(s, t, m, g, graph):
    tasks = []
    for n in range(1, m + 1, g):
        path = run_algorithm(graph, s, t, 1.34)[0] 
        task = asyncio.create_task(oppad(path, g, graph)) 
        tasks.append(task)
        tleave = 1
        await asyncio.sleep(tleave*g)
    await asyncio.gather(*tasks)
