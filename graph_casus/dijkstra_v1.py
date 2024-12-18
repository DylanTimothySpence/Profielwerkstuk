import math
from datetime import datetime


"""
class Node:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        
class Edge:
    def __init__(self, leftId: Node, rightId: Node, weight) -> None:
        self.leftId = leftId
        self.rightId = rightId
        self.weight = weight
        
"""
time_now = datetime.now()
print("-------------------------------------------- ", time_now," --------------------------------------------")
nodes = [0, 1, 2, 3, 4, 5]
edges = [
    #From node, To node, with weight
    (0, 1, 5),
    (0, 2, 1),
    (2, 1, 2),
    (1, 3, 3),
    (1, 4, 4),
    (2, 4, 7),   
    (4, 3, 1),
    (3, 5, 3),
    (4, 5, 5),
]
closest_node = 0
visited = [False, False, False, False, False, False]
path_weight = [0, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'),]

def check_buur(node):
    for edge in edges: #deze for telt niet op telt niet op?????
        source_node = edge[0]
        target_node = edge[1]
        weight = edge[2]
        potential_path_weight = weight + path_weight[source_node]
        
        if ( source_node == node ) and (potential_path_weight < path_weight[target_node]):    
            path_weight[target_node] = potential_path_weight
    visited[node] = True
    

            
            
#now find the shortest unvisited node
def shortest_unvis():
    global closest_node
    unvis_values = []
    for x in nodes:
        if visited[x] == False :
            unvis_values.append(path_weight[x])
    closest_node = path_weight.index(min(unvis_values)) #mogelijk een loop

    

check_buur(closest_node)
shortest_unvis()
while not all(visited):
    shortest_unvis() 
    check_buur(closest_node)
print("final shortest path values:",path_weight)


print("shortest path is", path_weight[-1])