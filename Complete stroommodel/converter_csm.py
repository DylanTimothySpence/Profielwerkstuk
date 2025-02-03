import csv
from collections import defaultdict

def csv_to_adjacency_list(file_path):
    graph = defaultdict(list)
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            source = int(row[0])
            if row[1] and row[2] and row[3]:
                graph[source].append([int(row[1]), float(row[2]), float(row[3]), 0, float(row[2])])
            if row[4] and row[5] and row[6]:
                graph[source].append([int(row[4]), float(row[5]), float(row[6]), 0, float(row[5])])
            if row[7] and row[8] and row[9]:
                graph[source].append([int(row[7]), float(row[8]), float(row[9]), 0, float(row[8])])
            if row[10] and row[11] and row[12]:
                graph[source].append([int(row[10]), float(row[11]), float(row[12]), 0, float(row[11])])
    return dict(graph)

'''#promt om de graaf als adjacency list te printen in de terminal
graph = csv_to_adjacency_list('./Complete stroommodel/double_weighted_graph_csm.csv')
print("graph = {")
for node, edges in sorted(graph.items()):
    print(f"    {node}: {edges},")
print("}")'''