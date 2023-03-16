import numpy as np
import copy

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

        if node1 not in self.nodes: # si le noeud 1 n'est jamais apparu
            self.nodes.append(node1) # On l'ajoute dans l'ensemble des noeuds
            # On l'ajoute dans le dictionnaire, avec pour premier voisisn le noeud 2
            self.graph[node1] = [[node2, power_min, dist]] 
        else:
            # Sinon, on rajoute le noeud 2 à la liste des voisins du noeud 1
            self.graph[node1].append([node2,power_min,dist])
            # De même pour le noeud 2
        if node2 not in self.nodes:
            self.nodes.append(node2)
            self.graph[node2]=[[node1,power_min,dist]]
        else:
            self.graph[node2].append([node1,power_min,dist])

        #raise NotImplementedError
    

    def get_path_with_power(self, src, dest, power):
        """Ce graphe permet d'obtenir le plus court chemin entre 2 points, avec une 
        contrainte de puissance. Pour cela on associe un poid dist à chaque noeud, initialisé à l'infini
        pour chaque noeud, sauf pour le noeud initial qui est à 0. 
        A la première itération, on modifie la dist des voisins du noeud initiale pour qu'elle
        soit égale à la distance entre le noeud initiale et son voisin, puis on note que le prédécesseur
        de ces noeuds voisins est le noeud initial.
        Pour les itérations suivantes, on choisit le noeud par lequel on n'est pas déjà passé avec la 
        plus petite dist, on modifie la dist de ses voisinpar lesquels on n'est pas déjà passé
        tel quelle soit égale à la dist du noeud choisit, plus la distance entre ce noeud et le 
        voisin, et on note que le prédécesseur de ces noeuds voisins est le noeud choisit.
        Puis on itère jusqu'à trouver le noeud dest ou que tout les noeuds par lesquels on n'est 
        pas passé soient à une distance infini (dans ce cas, cela veut dire qu'il n'y a pas de
        chemin entre src et dest)."""
        # On initialise la liste contenant les noeuds passés et la distance
        nodesPassed=[]  
        dist=[np.inf]*len(self.nodes)
        dist[src-1]=0
        test=True  # Permet de vérifier si le noeud dest est atteint et si il y a encore des chemins
        predecessor={}
        # distprime vaut la même valeur que dist, sauf si on est déjà passé par ce noeud,
        # et vaut alors inf. Ce qui permet d'éviter de sélectionner 2 fois un même noeud
        distprime=dist.copy()
        while test and len(nodesPassed)<len(self.nodes):
            # On modifie distprime
            for i in self.nodes:
                if i in nodesPassed:
                    distprime[i-1]=np.inf
                else:
                    distprime[i-1]=dist[i-1]
            # On choisit notre nouveau noeud
            node=1+distprime.index(min(distprime))
            nodesPassed.append(node)
            # On détermine ses voisins
            neighbors=[]
            for i in range(len(self.graph[node])):
                if self.graph[node][i][0] not in nodesPassed and self.graph[node][i][1]<=power:
                    neighbors.append(self.graph[node][i])
            # On modifie la dist de ses voisins
            for node_neighbor in neighbors:
                if dist[node_neighbor[0]-1]>dist[node-1]+node_neighbor[2]:
                    dist[node_neighbor[0]-1]=dist[node-1]+node_neighbor[2]
                    predecessor[node_neighbor[0]]=node
            # On vérifie si on a atteint la dest et si il y a encore des chemins
            test=False
            for i in range (1,1+len(dist)):
                if i not in nodesPassed and dist[i-1]!=np.inf:
                    test=True
        # Si on a atteint dest, on remonte les prédécesseurs en partant de dest jusqu'à src
        # pour avoir le chemin
        if dest in nodesPassed:
            path=[dest]
            node=dest
            while node != src:
                node=predecessor[node]
                path.append(node)
            path.reverse()
            return path
        else: # Si on n'a pas atteint dest, on renvoie None
            return None
            raise NotImplementedError
    
    def one_connected_components(self, node, nodes_known):
        # On parcours l'ensemble des noeuds sur la composante connexe avec un parcours en profondeur
        # Par récursivité
        connected_component=[node]
        neighbors=[self.graph[node][i][0] for i in range(len(self.graph[node]))]
        for node_neighbor in neighbors:
            if nodes_known[node_neighbor]:
                nodes_known[node_neighbor]=False # On ajoute d'abord les voisins de notre noeud initiale
                #Puis on itère la fonction pour avoir les voisins des voisins,...
                connected_component_1,nodes_known=self.one_connected_components(node_neighbor,nodes_known)
                connected_component+=connected_component_1
        return connected_component, nodes_known

    def connected_components(self):
        self.connect_components=[]
        nodes_known={node:True for node in self.nodes}  # Permet de savoir si un noeud est déjà parcouru
        for node in self.nodes:   # On parcours tous les noeuds du graphe
            if nodes_known[node]:   # Si ils ont déjà été parcouru, on ne les prend pas une seuconde fois
                nodes_known[node]=False
                # On regarde sa composante connexe
                connect_componentes, nodes_known=self.one_connected_components(node, nodes_known)
                self.connect_components.append(connect_componentes)
        return self.connect_components
        raise NotImplementedError
    

    def connected_components_set(self):
        """  
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """    
        return set(map(frozenset, self.connected_components()))
    
    def kpath(self,src,dest):
        # On vérifie src et dest sont dans la même composante connexe
        """
        connected_components=self.connected_components()
        for connected in connected_components:
            if src in connected:
                if dest not in connected:
                    return None,None"""
        # On vérifie que src!=dest
        if src==dest:
            return None,None
        depth_src=self.depth[src]
        depth_dest=self.depth[dest]
        path_src=[]  # pour la route partant de src
        path_dest=[]   # pour la route partant de dest
        # Pour le noeud avec la plus grande profoncdeur, on remonte l'arbre jusqu'à avoir la même profondeur
        while depth_src<depth_dest:
            depth_dest-=1
            path_dest.append([dest,self.parents[dest][1]])
            dest=self.parents[dest][0]
        while depth_src>depth_dest:
            depth_src-=1
            path_src.append([src,self.parents[src][1]])
            src=self.parents[src][0]
        # Puis on remonte les ancêtres juasqu'à tomber sur le même noeud
        while src!=dest:
            path_dest.append([dest,self.parents[dest][1]])
            path_src.append([src,self.parents[src][1]])
            src=self.parents[src][0]
            dest=self.parents[dest][0]
        # Les deux if suivant permettent d'éviter un bug dans le cas où, lorsque l'on remonte la profondeur d'un noeud, on tombe directement
        # sur l'autre noeud comme  noeud commun.
        if path_dest==[]:
            path_src.append([src,self.parents[src][1]])
            power=max([path_src[i][1] for i in range(len(path_src))])
            path=[path_src[i][0] for i in range(len(path_src))]
            return path,power
        if path_src==[]:
            path_dest.append([src,self.parents[dest][1]])
            power=max([path_dest[i][1] for i in range(len(path_dest))])
            path=[path_dest[i][0] for i in range(len(path_dest))]
            path.reverse()
            return path,power
        # sinon on colle les routes path_dest et path_src l'un à l'autre et on renvoie le trajet crée.
        if path_dest[-1][1]<path_src[-1][1]:
            path_dest.pop()
        else:
            path_src.pop()
        path_dest.reverse()
        path_1=path_src+path_dest
        power=max([path_1[i][1] for i in range(len(path_1))])
        path=[path_1[i][0] for i in range(len(path_1))]
        return path,power

    def Depth_First_Search_init(self):
        """
        Le but de cette fonction est de faire un parcours en profondeur de tout à partir d'une racine.
        Pour chaque noeud, on va associé son parent, ainsi qu'une profondeur, qui correspond au nombre
        d'arête entre ce noeud et le noeud racine.
        """
        self.parents={}   # dictionnaire des parents
        self.depth={}      # dictionnaire de la profondeur
        # dictionnaire pour savoir si les noeuds ont déjà étés parcourus
        nodes_known={node:True for node in self.nodes} 
        for node in self.nodes:   # On parcours tous les noeuds du graphe
            if nodes_known[node]:   # Si ils ont déjà été parcouru, on ne les prend pas une seuconde fois
                nodes_known[node]=False
                self.depth[node]=0 # initialise la profondeur, il s'agit de notre racine par cette composante connexe.
                self.parents[node]=[0,0]
                # On regarde sa composante connexe
                self.Depth_First_Search(node,nodes_known,0)
    
    def Depth_First_Search(self,node,nodes_known,depth):
        # On fait un parcours en profondeur en relevant les parents et la profondeur de chaque noeud
        for node_neighbor in self.graph[node]:
            if nodes_known[node_neighbor[0]]:
                nodes_known[node_neighbor[0]]=False
                self.parents[node_neighbor[0]]=[node,node_neighbor[1]]
                self.depth[node_neighbor[0]]=depth+1
                self.Depth_First_Search(node_neighbor[0],nodes_known,depth+1)


    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        # On vérifie que src et dest sont dans la même composante connexe.
        connected_components=self.connected_components_set()
        for connected in connected_components:
            if src in connected:
                if dest not in connected:
                    return None,None
        # On vérifie que la source et la destination sont différents
        if src==dest:
            return None,None
        # On regarde la plus petite puissance de 2 pour laquelle il y a un chemin
        power=2
        while self.get_path_with_power(src, dest, power)==None:
            power=power*2
        # Puis on fait une dichotomie entre cette puissance de 2 et celle inférieure
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

    G=Graph(nodes=[])   # On crée le graphe initialement vide
    f=open(filename,"r")
    lines=f.readlines()    # On lit ligne par ligne
    for i in lines:
        data=i.split(" ")
        if len(data)==3:    # Si trois éléments, alors il n'y a pas la distance
            node1,node2,power_min=int(data[0]),int(data[1]),int(data[2])
            G.add_edge(node1,node2,power_min)
        if len(data)==4: # Si quatre éléments, alors il y a la distance
            node1,node2,power_min,dist=int(data[0]),int(data[1]),int(data[2]),int(data[3])
            G.add_edge(node1,node2,power_min,dist)
        if len(data)==2:    # Si deux éléments, alors il s'agit de la ligne d'entête
            G.nb_nodes=int(data[0])
            G.nb_edges=int(data[1])
    return G

    
    raise NotImplementedError
