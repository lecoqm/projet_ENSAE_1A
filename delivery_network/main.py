from graph import Graph, graph_from_file
from kruskal import kruskal, union, find
import time
import copy
import sys


data_path = "/home/onyxia/projet_ENSAE_1A/input/"
file_name = "network.3.in"

routes="/home/onyxia/projet_ENSAE_1A/input/routes.3.in"

g = graph_from_file(data_path + file_name)
sys.setrecursionlimit(g.nb_edges)
g_mst=kruskal(g)
g_mst.Depth_First_Search_init()

f=open(routes,"r")
lines=f.readlines()
lines.pop(0)

f_out=open("/home/onyxia/projet_ENSAE_1A/output/network.3.out","a")

for l in lines:
    data=l.split(" ")
    src,dest=int(data[0]),int(data[1])
    a,b=g_mst.kpath(int(data[0]), int(data[1]))
    f_out.write(str(b)+"\n")
    
