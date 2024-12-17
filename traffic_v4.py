print("klaar voor de start...")
print("AF!!!")

import asyncio
import csv
from dijkstra_traffic import run_algorithm
from converter_traffic import csv_to_adjacency_list
from asyncio import Lock

run_indicator = True
latency_lock = Lock()

graph = csv_to_adjacency_list('./traffic_casus/trafficgraph.csv') # input

# een connectie in de graaf s: (t, w, x, n, L) = source node: (target node, gewicht(eerste graaf), breedte, aantal mensen, resulterende looptijd)

def latencyfunction(x, w, n):
    if n > 0:
        kjam = 5.4
        vf = 1.34
        e = 2.718281828
        L = w / (1 - (e ** (-1.913 * (((x * w * vf) / n) - (1 / kjam)))))
        if L < 0: # als de dichtheid groter is dan kjam dan wordt L negatief in de formule, terwijl deze oneindig moet zijn.
            L = float('inf')
    else: # als n=0 tript de functie (delen door 0) maar dan zou de resulterende looptijd gelijk moeten zijn aan het gewicht vd eerste graaf
        L = w
    return L

async def oppad(path, n):
    print(f"{n} op weg")
    for i, node in enumerate(path):
        next_node = path[i + 1] if i < len(path) - 1 else None

        if next_node:
            async with latency_lock:
                for index_connection, connection in enumerate(graph[node]): # zoeken naar de juiste connectie
                    if connection[0] == next_node:
                        connection[3] += 1
                        w = connection[1] # opslaan zodat dit niet heel vaak opnieuw opgehaald hoeft te worden en omdat ze constant blijven
                        x = connection[2]
                        Le = latencyfunction(x, w, connection[3])
                        connection[4] = Le
                        store_index_connection = index_connection # opslaan zodat er later niet gezocht hoeft te worden
                        break
                for index_connection, connection in enumerate(graph[next_node]): # zoeken naar de juiste reverse connectie
                    if connection[0] == node:
                        connection[3] += 1
                        connection[4] = latencyfunction(x, w, connection[3])
                        store_index_reverse_connection = index_connection # opslaan zodat er later niet gezocht hoeft te worden
                        break
            # persoon loopt over de zijde
            await asyncio.sleep(Le)
            # persoon is over de zijde gelopen, er wordt een aan aanwezigheid weggehaald en de resulterende looptijd opnieuw berekend
            async with latency_lock:
                graph[node][store_index_connection][3] -=1 
                graph[node][store_index_connection][4] = latencyfunction(x, w, graph[node][store_index_connection][3])
                graph[next_node][store_index_reverse_connection][3] -=1 # idem voor de reverse connectie
                graph[next_node][store_index_reverse_connection][4] = latencyfunction(x, w, graph[node][store_index_reverse_connection][3])

    print(f"{n} aangekomen")

async def flow(s, t, m):
    tasks = []
    for n in range(1, m + 1):
        path = run_algorithm(graph, s, t, 1.34)[0] # bereken het kortste pad s --> t
        task = asyncio.create_task(oppad(path, n)) # stuurt een persoon op dit pad
        tasks.append(task)
        await asyncio.sleep(0.5)  # elke seconde gaat een nieuw persoon de deur uit
    # wachten tot elke persoon is aangekomen
    await asyncio.gather(*tasks)
    global run_indicator
    run_indicator = False # indicator wordt uitgezet

async def indicator(s, t): # de indicator heeft geen invloed op het proces, het is een visualisatie van het proces
    with open('./traffic_casus/output.csv', 'w', newline='') as csvfile: # output file wordt gemaakt (handig voor een grafiekje ed.)
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['n', 'teller trappenhuis', 'teller conciërge'])
        d = 0
        while run_indicator: # hierbinnen kun je van alles schrijven om te visualiseren
            '''tijd_trappenhuis = round(((run_algorithm(graph, s, 7, 1.34))[1] + (run_algorithm(graph, 7, t, 1.34))[1]), 2)
            #tijd_conciërge = round(((run_algorithm(graph, s, 2, 1.34))[1] + (run_algorithm(graph, 2, t, 1.34))[1]), 2)
            #csv_writer.writerow([0, tijd_trappenhuis, tijd_conciërge])  '''
            csv_writer.writerow([d, graph[5][0][4], graph[6][1][4]])

            await asyncio.sleep(1) 
            d +=1

async def main():
    # start flow en indicator gelijktijdig
    await asyncio.gather(
        flow(5, 13, 200), # input
        indicator(5, 13)
    )

asyncio.run(main())

print ("iedereen heeft de finish gehaald!")