from graph import Graph, graph_from_file
import itertools
import time

def truck_choice(route, trucks):
    """
    Cette fonction permet de trouver le camion le moins cher pouvant passer par cette route.
    La liste trucks doit être triée par ordre décroissant.
    """
    power = g.min_power(route[0], route[1])[0]
    if trucks[0][0]<power:      # On vérifie que le camion le plus puissant peut passer par cette route.
        return None
    i=0
    while i<len(trucks) and trucks[i][0]>=power:
        i+=1
    if i==len(trucks):
        return trucks[-1]
    return trucks[i]

def brut_force(file_routes,file_trucks,contrainte):
    # Initialisation
    routes=open(file_routes,"r")
    lines = routes.readlines() # attention c'est des string + split
    nb_routes=lines.pop(0)
    routes_lines=[]
    for l in lines:
        data=l.split(" ")
        routes_lines.append([int(data[0]),int(data[1]),int(data[2].rstrip("\n"))]) 
    trucks=open(file_trucks,"r")
    lines = trucks.readlines() # attention c'est des string + split
    i=0
    lines.pop(0)
    trucks_lines=[]
    for l in lines:
        i+=1
        data=l.split(" ")
        trucks_lines.append([int(data[0]),int(data[1].rstrip("\n")),i])
    trucks_lines = sorted(trucks_lines, key=lambda x:x[1],reverse=True) # trie les camions en fonction de leur coût ordre croissant
    # On crée l'ensemble des parties de routes_lines
    ens_comb_routes = []
    ens_comb_routes_1=[]
    for i in range(1,1+len(routes_lines)):  
        for j in itertools.combinations(routes_lines, i):
            ens_comb_routes_1.append(list(j))
    for list_routes in ens_comb_routes_1:
        profit=0
        for route in list_routes:
            profit+=route[2]
        ens_comb_routes.append([list_routes, profit])
    ens_comb_routes = sorted(ens_comb_routes, key=lambda x:x[1], reverse = True)    # On trie l'ensemble des comb de route en fonction du profit ordre décroissant
    i=0     # variable de comptage sur ens_comb_routes
    # Pour chaque combinaison de routes, on crée la liste de camion associé.
    # On vérifie si le coût est inférieure à la contrainte et si c'est le cas on arrête la fonction
    # et on renvoie la liste associée.
    # Comme les combinaisons de routes sont triées par ordre de profit décroissant, on renvoie automatiquement
    # la meilleure combinaison de route.
    for comb_routes in ens_comb_routes:
        choosen_trucks=[]
        cost=0
        comb_routes_1=comb_routes[0]
        for route in comb_routes_1:
            truck=truck_choice([route[0],route[1]],trucks_lines)
            if truck !=None:
                cost+=truck[0]
                choosen_trucks.append(truck)
            else:
                cost=contrainte+1
        if cost<=contrainte:
            return comb_routes, choosen_trucks, cost


file_routes="/home/onyxia/projet_ENSAE_1A/input/routes.0.in"
file_trucks="/home/onyxia/projet_ENSAE_1A/output/trucks.0.min.in"
g=graph_from_file("/home/onyxia/projet_ENSAE_1A/input/network.1.in")
contrainte=25*(10**9)

t1=time.time()
routes,trucks,cost=brut_force(file_routes, file_trucks,contrainte)
print(len(routes), trucks)
t2=time.time()
print(t2-t1)
