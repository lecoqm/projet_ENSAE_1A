import numpy as np

class Graph:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """

        if node1 not in self.nodes:
            self.nodes.append(node1)
            self.graph[node1] = [[node2, power_min, dist]]
        else:
            self.graph[node1].append([node2,power_min,dist])
        if node2 not in self.nodes:
            self.nodes.append(node2)
            self.graph[node2]=[[node1,power_min,dist]]
        else:
            self.graph[node2].append([node1,power_min,dist])

        #raise NotImplementedError
    

    def get_path_with_power(self, src, dest, power):
        nodesPassed=[]
        dist=[np.inf]*len(self.nodes)
        dist[src-1]=0
        test=True
        predecessor={}
        distprime=dist.copy()
        while test and len(nodesPassed)<len(self.nodes):
            for i in self.nodes:
                if i in nodesPassed:
                    distprime[i-1]=np.inf
                else:
                    distprime[i-1]=dist[i-1]
            node=1+distprime.index(min(distprime))
            nodesPassed.append(node)
            neighbors=[]
            for i in range(len(self.graph[node])):
                if self.graph[node][i][0] not in nodesPassed and self.graph[node][i][1]<=power:
                    neighbors.append(self.graph[node][i])
            for node_neighbor in neighbors:
                if dist[node_neighbor[0]-1]>dist[node-1]+node_neighbor[2]:
                    dist[node_neighbor[0]-1]=dist[node-1]+node_neighbor[2]
                    predecessor[node_neighbor[0]]=node
            test=False
            for i in range (1,1+len(dist)):
                if i not in nodesPassed and dist[i-1]!=np.inf:
                    test=True
        if dest in nodesPassed:
            path=[dest]
            node=dest
            while node != src:
                node=predecessor[node]
                path.append(node)
            path.reverse()
            return path
        else:
            return None
            raise NotImplementedError
    
    def one_connected_components(self, node, nodes_known):
        connected_component=[node]
        neighbors=[self.graph[node][i][0] for i in range(len(self.graph[node]))]
        for node_neighbor in neighbors:
            if node_neighbor not in nodes_known:
                nodes_known.add(node_neighbor)
                connected_component_1,nodes_known=self.one_connected_components(node_neighbor,nodes_known)
                connected_component+=connected_component_1
        return connected_component, nodes_known

    def connected_components(self):
        self.connected_components=[]
        nodes_known=set()
        for node in self.nodes:
            if node not in nodes_known:
                nodes_known.add(node)
                connected_componentes, nodes_known=self.one_connected_components(node, nodes_known)
                self.connected_components.append(connected_componentes)
        return self.connected_components
        raise NotImplementedError
    

    def connected_components_set(self):
        """  
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """    
        return set(map(frozenset, self.connected_components()))
    
    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        # vérification composante connexe
        power=2
        while self.get_path_with_power(src, dest, power)==None:
            power=power*2
        inf=power//2
        sup=power
        mid=(sup+inf)//2
        while sup-inf>1:
            if self.get_path_with_power(src, dest, mid)==None:
                inf=mid
                mid=(sup+inf)//2
            else:
                sup=mid
                mid=(sup+inf)//2
        if self.get_path_with_power(src, dest, inf)==None:
            return sup, self.get_path_with_power(src, dest, sup)
        else:
            return inf, self.get_path_with_power(src, dest, inf)

        raise NotImplementedError


def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    G: Graph
        An object of the class Graph with the graph from file_name.
    """

    G=Graph(nodes=[])
    f=open(filename,"r")
    lines=f.readlines()
    for i in lines:
        data=i.split(" ")
        if len(data)==3:
            node1,node2,power_min=int(data[0]),int(data[1]),int(data[2])
            G.add_edge(node1,node2,power_min)
        if len(data)==4:
            node1,node2,power_min,dist=int(data[0]),int(data[1]),int(data[2]),int(data[3])
            G.add_edge(node1,node2,power_min,dist)
        if len(data)==2:
            G.nb_nodes=int(data[0])
            G.nb_edges=int(data[1])
    return G

    
    raise NotImplementedError
