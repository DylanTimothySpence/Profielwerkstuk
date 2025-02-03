from converter_csm import csv_to_adjacency_list
graph = csv_to_adjacency_list('./Complete stroommodel/double_weighted_graph_csm.csv')
for node, edges in graph.items():
    print(f'{node} : {edges}')
    print('')
def symmetry_check(graph):
    is_symmetric = True  
    for node, edges in graph.items():
        for connected_node, weight, x, n, t in edges:
            reverse_found = False
            for reverse_neighbor, reverse_weight, reverse_x, reverse_n, reverse_t in graph.get(connected_node, []):
                if reverse_neighbor == node:
                    reverse_found = True
                    if reverse_weight != weight:
                        print(f"Asymmetry found: ({node}, {connected_node}) has weight {weight}, "
                              f"but ({connected_node}, {node}) has weight {reverse_weight}")
                    if reverse_x != x:
                        print(f"Asymmetry found: ({node}, {connected_node}) has x {x}, "
                              f"but ({connected_node}, {node}) has x {reverse_x}")
                    if reverse_n != n:
                        print(f"Asymmetry found: ({node}, {connected_node}) has n {n}, "
                              f"but ({connected_node}, {node}) has n {reverse_n}")
                    if reverse_t != t:
                        print(f"Asymmetry found: ({node}, {connected_node}) has t {t}, "
                              f"but ({connected_node}, {node}) has t {reverse_t}")
                    break
            if not reverse_found:
                print(f"Warning: No reverse connection from {connected_node} to {node}.")
                is_symmetric = False  
    return is_symmetric  

symmetry_check(graph)
    