from traffic_casus.dijkstra_casus import run_algorithm
from traffic_casus.converter_casus import csv_to_adjacency_list
import threading
import time
from datetime import datetime
import csv

graph = csv_to_adjacency_list('./traffic_casus/trafficgraph.csv')
# Globale teller voor actieve threads
active_threads = 0
active_threads_lock = threading.Lock()  # Lock om toegang tot de teller te synchroniseren

def latencyfunction(x, w, n):
    if n > 0:
        kjam = 5.4
        vf = 1.34
        e = 2.718281828
        L = w / (1 - (e ** (-1.913 * (((x * w * vf) / n) - (1 / kjam)))))
        if L < 0 :
            L = float('inf')
    else: 
        L = w
    return L
    

def oppad(path, n):
    global active_threads
    global next_node, Le, con1, con2
    print('                          ',n, 'op weg - ', datetime.now())

    for i, node in enumerate(path):
        if i < len(path) - 1:
            next_node = path[i + 1] 
            for index1, connection in enumerate(graph[node]):
                if connection[0] == next_node:
                    connection[3] = int(connection[3]) + 1
                    Le = latencyfunction(connection[2], connection[1], connection[3])
                    connection[4] = Le
                    con1 = index1
            for index2, connection in enumerate(graph[next_node]):
                if connection[0] == node:
                    connection[3] = int(connection[3]) + 1
                    connection[4] = Le
                    con2 = index2

            time.sleep(Le)
            #print (Le)

            # Verminder de verkeerdruk
            graph[node][con1][3] -= 1
            Le = latencyfunction(graph[node][con1][2], graph[node][con1][1], graph[node][con1][3])
            graph[node][con1][4] = Le
            graph[next_node][con2][3] -= 1
            graph[next_node][con2][4] = Le
        else: #de persoon is aangekomen
            print('                                                                    ',n, 'aangekomen - ', datetime.now())
            with active_threads_lock:
                active_threads -= 1

def flow(s, t, m):
    global active_threads
    with active_threads_lock:
        active_threads += 1
    for n in range(1, (m + 1)):
        path = run_algorithm(graph, s, t, 1.34)[0]
        # Start een thread en verhoog de teller
        with active_threads_lock:
            active_threads += 1
        threading.Thread(target=oppad, args=(path, n)).start()

        time.sleep(0.5)
    with active_threads_lock:
        active_threads -= 1

def arbitrair():
    threading.Thread(target=flow, args=(5,13,200)).start()
    for n in range (1, 300):
        print(datetime.now())
        time.sleep(1)

'''
def indicator(s, t):
    global active_threads
    d=0

    with open('./traffic_casus/output.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['n', 'teller trappenhuis', 'teller conciërge'])

        while True: #not active_threads==0
            tijd_trappenhuis = round(((run_algorithm(graph, s, 7, 1.34))[1] + (run_algorithm(graph, 7, t, 1.34))[1]), 2)
            tijd_conciërge = round(((run_algorithm(graph, s, 2, 1.34))[1] + (run_algorithm(graph, 2, t, 1.34))[1]), 2)
            csv_writer.writerow([d, tijd_trappenhuis, tijd_conciërge])

            # Controleer of alle threads klaar zijn
            with active_threads_lock:
                if active_threads <= 0:
                    break
            print(d, ' s')
            time.sleep(1)
            d +=1
'''
'''
flow_thread = threading.Thread(target=flow, args=(5, 13, 200))
indicator_thread = threading.Thread(target=indicator, args=(5, 13))

flow_thread.start()
indicator_thread.start()

# Wacht tot beide threads klaar zijn
flow_thread.join()
indicator_thread.join()'''
arbitrair()