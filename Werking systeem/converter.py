import csv
from collections import defaultdict

def csv_to_adjacency_list(file_path):
    graph = defaultdict(list)
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            source = int(row[0])
            if row[1] and row[2]:
                graph[source].append([int(row[1]), float(row[2])])
            if row[3] and row[4]:
                graph[source].append([int(row[3]), float(row[4])])
            if row[5] and row[6]:
                graph[source].append([int(row[5]), float(row[6])])
            if row[7] and row[8]:
                graph[source].append([int(row[7]), float(row[8])])
    return dict(graph)
    
'''#promt om de graaf als adjacency list te printen in de terminal
graph = csv_to_adjacency_list('./Werking systeem/weighted_graph.csv')
print("graph = {")
for node, edges in sorted(graph.items()):
    print(f"    {node}: {edges},")
print("}")'''
