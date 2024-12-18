
import math
from datetime import datetime

print("-----------", (datetime.now().strftime("%Y-%m-%d %H:%M:%S")) ,"-----------")

graph = {
    0: [(1, 5), (2, 1)],
    1: [(0, 5), (2, 2), (3, 3), (4, 4)],
    2: [(0, 1), (1, 2), (4, 7)],
    3: [(1, 3), (4, 1), (5, 3)],
    4: [(1, 4), (2, 7), (3, 1), (5, 5)],
    5: [(3, 3), (4, 5)]
}




endnode = 5 #input
startnode = 0 #input
visited = [False] * len(graph)
path_weight = [float('inf')] * len(graph)  
path_weight[startnode] = 0
previous_node = [None] * len(graph)

#------------de algoritmes

def check_connected_nodes(node):
    for buur, weight in graph[node]:  
        if path_weight[node] + weight < path_weight[buur]:  
            path_weight[buur] = path_weight[node] + weight  
            previous_node[buur] = node  
    visited[node] = True  
             
def closest_unvisited_node():
    unvisited_distances = []
    for index, weight in enumerate(path_weight): 
        if visited[index] == False :
            unvisited_distances.append((weight, index))
    if unvisited_distances:  
        return min(unvisited_distances, key=lambda x: x[0])[1]  
    
def find_route():
    route = []
    current_node = endnode
    while current_node != startnode:
        route.append(current_node)
        current_node = previous_node[current_node]
    route.append(current_node)
    route.reverse()
    return route

#----------- uitvoer programma

while not visited[endnode]:
    check_connected_nodes(closest_unvisited_node())
print("-----------", (datetime.now().strftime("%Y-%m-%d %H:%M:%S")) ,"-----------")


#---------- print alles
    
print("the shortest route is:", find_route())
print("with length:", path_weight[endnode])
print("path_weight = ", path_weight)
