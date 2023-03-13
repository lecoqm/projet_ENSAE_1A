from graph import Graph, graph_from_file
from kruskal import kruskal, union, find

data_path = "/home/onyxia/projet_ENSAE_1A/input/"
file_name = "network.04.in"

g = graph_from_file(data_path + file_name)
#print(g)

a=kruskal(g)
b=a.kpath(2,4)
print(b)
