from traffic_casus.dijkstra_casus import run_algorithm
from traffic_casus.converter_casus import csv_to_adjacency_list
import threading
import time
import csv


#conciërge = 0
#trappenhuis = 0

graph = csv_to_adjacency_list('./traffic_casus/trafficgraph.csv')


def latencyfunction(x, w, n):
    kjam = 5.4
    vf = 1.34
    e = 2.718281828
    L = w / (1 - (e ** (-1.913 * (((x * w * vf) / n) - (1 / kjam)))))
    return L

def oppad (node, connection_index, a, length):
    time.sleep(length)
    graph[node][connection_index][3] -= a
    Le = latencyfunction(graph[node][connection_index][2], graph[node][connection_index][1], graph[node][connection_index][3])
    if Le < 0:
        Le = float('inf')
    graph[node][connection_index][4] = Le


output_file = './traffic_casus/output.csv'
#lock = threading.Lock()

def flow(s, t, m):
    global trappenhuis
    global conciërge
    
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['n', 'teller trappenhuis', 'teller conciërge'])  

        for n in range(1, (m+1)):
            shortest_path = run_algorithm(graph, s, t, 1.34)
            path = shortest_path[0]
            length = shortest_path[1]
            
            tijd_trappenhuis = round(((run_algorithm(graph, s, 7, 1.34))[1] + (run_algorithm(graph, 7, t, 1.34))[1]), 2)
            tijd_conciërge = round(((run_algorithm(graph, s, 2, 1.34))[1] + (run_algorithm(graph, 2, t, 1.34))[1]), 2)
            
            
            #with lock:
            csv_writer.writerow([n, tijd_trappenhuis, tijd_conciërge])
            print (n)
            
            for i, node in enumerate(path):
                prev_node = path[i - 1] if i > 0 else None
                next_node = path[i + 1] if i < len(path) - 1 else None
                for connection_index, connection in enumerate(graph[node]):
                    if connection[0] == prev_node or connection[0] == next_node:
                        a = connection[4] / length
                        connection[3] += a
                        Le = latencyfunction(connection[2], connection[1], connection[3])
                        if Le < 0:
                            Le = float('inf')
                        connection[4] = Le
                        threading.Thread(target=oppad, args=(node, connection_index, a, length)).start()  # Verplaats argumenten naar 'args'
            time.sleep(1)


flow(5, 13, 200)
