# import networkx as nx
# import matplotlib.pyplot as plt
# G = nx.DiGraph()
# graph = {
#         "A":[("B",5),("C",6)],
#         "B":[("D",10),("E",1)],
#         "C":[("E",5),("F",12)],
#         "D":[("B",20),("G",9)],
#         "E":[("B",4),("C",8)],
#         "F":[("C",28),("G",15)],
#         "G":[("D",3),("F",7)]
#     }

# for vertex, edges in graph.items():
#     G.add_node("%s" % vertex)
#     for edge,weight in edges:
#         G.add_node("%s" % edge)
#         G.add_edge("%s" % vertex, "%s" % edge, weight = weight)
#         print("'%s' it connects with '%s'" % (vertex,edge))
# # ---- END OF UNCHANGED CODE ----

# # Create positions of all nodes and save them
# pos = nx.spring_layout(G)

# # Draw the graph according to node positions
# nx.draw(G, pos, with_labels=True, node_color = 'white')

# # Create edge labels
# labels = {e: str(e) for e in G.edges}
# labels = nx.get_edge_attributes(G,'weight')

# # Draw edge labels according to node positions
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
# nx.draw_networkx_edges(G,pos,edgelist = G.edges,edge_color = 'black' , arrows= True,
#     arrowsize=20)

# #hightlight start
# highlighted_node_name = 'F'
# nx.draw_networkx(G.subgraph(highlighted_node_name), pos=pos, node_color='red')

# # hightlight path
# path = ['A','B','C']
# nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange')

# plt.show()
import copy

list1 = [1,2,3,4]

ref_copy = list1
shallow_copy = copy.copy(list1)
deep_copy = copy.deepcopy(list1)

ref_copy[1] = 'refed'
shallow_copy[1] = 'shallowed'
deep_copy[1] = 'deeped'
print(list1,ref_copy,list1,shallow_copy,list1,deep_copy)