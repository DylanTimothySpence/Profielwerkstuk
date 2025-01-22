from traffic_casus.dijkstra_casus import run_algorithm
from traffic_casus.converter_casus import csv_to_adjacency_list
import csv

#conciërge = 0
#trappenhuis = 0

def latencyfunction(x, w, n):
    kjam = 5.4
    vf = 1.34
    e = 2.718281828
    L = w / (1 - (e ** (-1.913 * (((x * w * vf) / n) - (1 / kjam)))))
    return L

graph = csv_to_adjacency_list('./traffic_casus/trafficgraph.csv')

output_file = './traffic_casus/output.csv'
with open(output_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['n', 'teller trappenhuis', 'teller conciërge'])  

    def flow(s, t, m):
        global trappenhuis
        global conciërge
        for n in range(1, (m+1)):
            shortest_path = run_algorithm(graph, s, t, 1.34)
            path = shortest_path[0]
            length = shortest_path[1]
            '''
            tijd_trappenhuis = round(((run_algorithm(graph, s, 7, 1.34))[1] + (run_algorithm(graph, 7, t, 1.34))[1]), 2)
            tijd_conciërge = round(((run_algorithm(graph, s, 2, 1.34))[1] + (run_algorithm(graph, 2, t, 1.34))[1]), 2)
            if 7 in path:
                trappenhuis +=1
            if 2 in path:
                conciërge +=1
            csv_writer.writerow([n, trappenhuis, conciërge])
            csv_writer.writerow([n, tijd_trappenhuis, tijd_conciërge])
            '''
            for i, node in enumerate(path):
                prev_node = path[i - 1] if i > 0 else None
                next_node = path[i + 1] if i < len(path) - 1 else None
                for connection in graph[node]:
                    if connection[0] == prev_node or connection[0] == next_node:
                        a = connection[4] / length
                        connection[3] += a
                        Le = latencyfunction(connection[2], connection[1], connection[3])
                        if Le < 0:
                            Le = float('inf')
                        connection[4] = Le

    #flow(5, 13, 200)
