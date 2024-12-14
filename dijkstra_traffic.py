
#import math
#from datetime import datetime
#from converter_traffic import csv_to_adjacency_list

#print("-----------", (datetime.now().strftime("%Y-%m-%d %H:%M:%S")) ,"-----------")
#x=datetime.now()
def check_connected_nodes(graph, node, path_weight, previous_node, visited):
    for buur, weight, x, n, t in graph[node]:  
        if path_weight[node] + t < path_weight[buur]:  
            path_weight[buur] = path_weight[node] + t  
            previous_node[buur] = node  
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

def walking_time(weight, speed):
        time = round((weight * (1.34/speed)),2)
        return time

def run_algorithm(graph, startnode, endnode, speed):
    visited = [False] * len(graph)
    path_weight = [float('inf')] * len(graph)  
    path_weight[startnode] = 0
    previous_node = [None] * len(graph)
    while not visited[endnode]:
        check_connected_nodes(graph, closest_unvisited_node(path_weight, visited), path_weight, previous_node, visited)
    return (find_route(startnode, endnode, previous_node), walking_time(path_weight[endnode], speed))

#print(run_algorithm(csv_to_adjacency_list('trafficgraph.csv'), 14, 4, 1.34))
#y=datetime.now()
#print('time to run is: ', y-x)
