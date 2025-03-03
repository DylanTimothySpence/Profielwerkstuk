def check_connected_nodes(graph, node, path_weight, previous_node, visited):
    for connected_node, weight in graph[node]:  
        if path_weight[node] + weight < path_weight[connected_node]:  
            path_weight[connected_node] = path_weight[node] + weight  
            previous_node[connected_node] = node  
    visited[node] = True
             
def closest_unvisited_node(path_weight, visited):
    unvisited_distances = []
    for index, weight in enumerate(path_weight): 
        if visited[index] == False :
            unvisited_distances.append((weight, index))
    if unvisited_distances:  
        return min(unvisited_distances, key=lambda x: x[0])[1]  
    
def find_route(startnode, endnode, previous_node):
    route = []
    current_node = endnode
    while current_node != startnode:
        route.append(current_node)
        current_node = previous_node[current_node]
    route.append(current_node)
    route.reverse()
    return route

def walking_time(tsys, speed, fastest_path):
    dtgem = 0.95
    tcor = tsys - float((len(fastest_path)-2)*dtgem)
    tgkz = round((tcor * (1.34/speed)),2)
    return tgkz

def run_algorithm(graph, startnode, endnode, speed):
    visited = [False] * len(graph)
    path_weight = [float('inf')] * len(graph)  
    path_weight[startnode] = 0
    previous_node = [None] * len(graph)
    while not visited[endnode]:
        check_connected_nodes(graph, closest_unvisited_node(path_weight, visited), path_weight, previous_node, visited)
    fastest_path = find_route(startnode, endnode, previous_node)
    return fastest_path, walking_time(path_weight[endnode], speed, fastest_path)

'''#promt om een snelste pad te vinden, zet hier respectievelijk                   beginpunt, eindpunt en snelheid
#__________________________________________________________________________________________V_____V____V
from converter import csv_to_adjacency_list
route, time = run_algorithm(csv_to_adjacency_list('./Werking systeem/weighted_graph.csv'), 3, 133, 1.34)
print(f"Route: {route}, Time: {time}")'''