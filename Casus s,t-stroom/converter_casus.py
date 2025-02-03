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
    return dict(graph)

'''#promt om de casus graaf als adjacency list te printen in de terminal
graph = csv_to_adjacency_list('./Casus s,t-stroom/double_weighted_graph_casus.csv')
print("graph = {")
for node, edges in sorted(graph.items()):
    print(f"    {node}: {edges},")
print("}")'''