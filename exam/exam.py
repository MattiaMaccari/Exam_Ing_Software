import numpy as np
import math
import matplotlib.pyplot as plt
import copy
import seaborn as sns

def generate_tsp_instance(n=5, max_coordinate=100, max_opening_time=10, 
seed_coordinates=None, seed_opening_times=None):

    #Seme per la generazione delle coordiante
    if seed_coordinates is not None:
        np.random.seed(seed_coordinates)
    coordinates = [(np.random.randint(0,max_coordinate), np.random.randint(0,max_coordinate)) for _ in range(n)]

    #Seme per la generazione dei tempi di apertura
    if seed_opening_times is not None:
        np.random.seed(seed_opening_times)
    opening_times = [0] + [np.random.randint(1, max_opening_time) for _ in range(n-1)]

    #La matrice viene inizializzata a tutti zero
    #Non calcolo elmenti della diagonale --> 0
    #Calcolo solo la metà dei valori --> la matrice è simmetrica
    distance_matrix = np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[j]
            dist = math.ceil(np.sqrt((x2 - x1)**2 + (y2 - y1)**2))
            distance_matrix[i][j] = dist
            distance_matrix[j][i] = dist

    #Nodo: id, tempo di apertura, coordinate, 
    # vettore di distanza per tutti i punti (0 distanza da se stesso)
    nodes = []
    for i in range(n):
        node = {
            'id': i,
            'opening_time': opening_times[i],
            'coordinates': coordinates[i],
            'distance_vector': distance_matrix[i]
        }
        nodes.append(node)

    return nodes

def print_istance(nodes):
    for node in nodes:
        print(f"ID: {node['id']}\tOpening Time: {node['opening_time']} \tCoordinates: {node['coordinates']}\tDistance Vector: {node['distance_vector']}")

def main():
    print("Tutto aggiornato")
    # GENERAZIONE DELLE ISTANZE
    instance_1 = generate_tsp_instance(n=5, seed_coordinates=1, seed_opening_times=2)
    instance_2 = generate_tsp_instance(n=20, max_coordinate=200, seed_coordinates=3, seed_opening_times=4)

    # CALCOLO DELLE SOLUZIONI DELLE GREEDY

    # LE RIGHE SEGUENTI STAMPANO DIRETTAMENTE LE SOLUZIONI DELLE GREEDY E LA LORO COMPARAZIONE
    # IN UN UNICO SUBPLOT SENZA DOVER INVOCARE ESPLICITAMENTE LA FUNZIONE plot_tsp_node_link
    #call_greedy(20, 100, 80, 44, 2,'greedy_minimum_opening_time')
    #compare_greedy(20,100,80,44,2)

    #LE SEGUENTI RIGHE APPLICANO LE GREEDY SU UN'ISTANZA ALLA VOLTA
    #Sol1 = greedy_minimum_opening_time(instance_1)
    #Sol1B = greedy_minimum_opening_time(instance_2)

    #Sol2 = greedy_minimum_distance_from_zero(instance_1)
    #Sol2B = greedy_minimum_distance_from_zero(instance_2)

    #Sol3 = nn_greedy(instance_1)
    #Sol3B = nn_greedy(instance_2)

    ## STAMPA DELLE ISTANZE GENERATE
    #print("Istanza 1:")
    #print_istance(instance_1)
    #print("\nIstanza 2:")
    #print_istance(instance_2)

    #print("\n")
    #plot_tsp_nodes(instance_1)
    #plot_tsp_nodes(instance_2)

    # STAMPA DELLE ISTANZE CON FRECCE DI COLLEGAMENTO
    #plot_tsp_nodes_link(instance_1)
    #plot_tsp_nodes_link(instance_2)

    # STAMPA DELLE SOLUZIONI DELLE GREEDY
    #plot_tsp_nodes_link(Sol1)
    #plot_tsp_nodes_link(Sol1B)

    #plot_tsp_nodes_link(Sol2)
    #plot_tsp_nodes_link(Sol2B)

    #plot_tsp_nodes_link(Sol3)
    #plot_tsp_nodes_link(Sol3B)


    # STAMPO DELLE METRICHE INERENTI ALLE LOCAL SEARCH

    call_LocalSearch(20, 100, 80, 44, 2, 'greedy_minimum_opening_time','LS_swap_adjacent')
    call_LocalSearch(20, 100, 80, 44, 2, 'greedy_minimum_distance_from_zero','LS_swap_adjacent')
    call_LocalSearch(20, 100, 80, 44, 2, 'nn_greedy','LS_swap_adjacent')

    call_LocalSearch(20, 100, 80, 44, 2, 'greedy_minimum_opening_time','LSH_city_insert')
    call_LocalSearch(20, 100, 80, 44, 2, 'greedy_minimum_distance_from_zero','LSH_city_insert')
    call_LocalSearch(20, 100, 80, 44, 2, 'nn_greedy','LSH_city_insert')
    
    call_LocalSearch(20, 100, 80, 44, 2, 'greedy_minimum_opening_time','LSH_city_insertT')
    call_LocalSearch(20, 100, 80, 44, 2, 'greedy_minimum_distance_from_zero','LSH_city_insertT')
    call_LocalSearch(20, 100, 80, 44, 2, 'nn_greedy','LSH_city_insertT')



    plt.show()


if __name__ == "__main__":
    main()

# *****************************************************************
# STAMPA DELLE ISTANZE CON SOLAMENTE I NODI VISUALIZZATI NEL PIANO
# *****************************************************************

def plot_tsp_nodes(nodes):
    plt.figure(figsize=(6, 6))

    for node in nodes:
        x, y = node['coordinates']
        if node['id'] == 0:
            plt.scatter(x, y, color='red', s=50, zorder=3)
        else:
            plt.scatter(x, y, color='blue', s=50, zorder=3)
            plt.text(x + 1, y + 1, f"{node['id']}", fontsize=9, color='black')

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("TSP Nodes Visualization")
    plt.grid(True)
    #plt.show()


# ****************************************************
# STAMPA DELLE ISTANZE CON I NODI COLLEGATI DA FRECCE
# ****************************************************

def plot_tsp_nodes_link(nodes, title = "TSP Nodes Visualization", value = "",show="YES"):
    plt.figure(figsize=(6, 6))

    #Disegna i nodi
    for node in nodes:
        x, y = node['coordinates']
        if node['id'] == 0:
            plt.scatter(x, y, color='red', s=50, zorder=3)
        else:
            plt.scatter(x, y, color='blue', s=50, zorder=3)
            plt.text(x + 1, y + 1, f"{node['id']}", fontsize=9, color='black', zorder=3)

    #Disegna le frecce tra i nodi
    for i in range(len(nodes) - 1):
        x1, y1 = nodes[i]['coordinates']
        x2, y2 = nodes[i + 1]['coordinates']
        plt.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle='->', color='orange', lw=2), zorder=2)

    # Se ci sono almeno 3 nodi collego l'ultimo nodo con il primo
    if len(nodes) > 2:
        x1, y1 = nodes[-1]['coordinates']
        x2, y2 = nodes[0]['coordinates']
        plt.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle='->', color='orange', lw=2), zorder=2)

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title(title + ("  FO: " + value if value else ""))
    plt.grid(True)
    #if show is not None:
     # plt.show()


# ********************************************
# FUNZIONE PER FARE DEI SUBPLOT DI PIU FIGURE
# ********************************************
def plot_tsp_nodes_link_nofigure(nodes, title="TSP Nodes Visualization", value=""):
    # NON creiamo una nuova figura qui, usiamo il subplot corrente

    # Disegna i nodi
    for node in nodes:
        x, y = node['coordinates']
        if node['id'] == 0:
            plt.scatter(x, y, color='red', s=50, zorder=3)
        else:
            plt.scatter(x, y, color='blue', s=50, zorder=3)
        plt.text(x + 1, y + 1, f"{node['id']}", fontsize=9, color='black', zorder=3)

    # Disegna le frecce tra i nodi
    for i in range(len(nodes) - 1):
        x1, y1 = nodes[i]['coordinates']
        x2, y2 = nodes[i + 1]['coordinates']
        plt.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle='->', color='orange', lw=2), zorder=2)

    # Se ci sono almeno 3 nodi collego l'ultimo nodo con il primo
    if len(nodes) > 2:
        x1, y1 = nodes[-1]['coordinates']
        x2, y2 = nodes[0]['coordinates']
        plt.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle='->', color='orange', lw=2), zorder=2)

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title(title + ("  FO: " + value if value else ""))
    plt.grid(True)

# *********************************************
# CALCOLO DEL VALORE DELLA FUNZIONE OBBIETTIVO
# *********************************************
def calculate_objective(route, istance, info=None):


    #Se in route non ci sono tutti i nodi --> Soluzione non valida
    if len(route) != len(istance):
        print("Soluzione non valida: la soluzione non include tutti i nodi !")
        return None

    #Se il primo elemento non è la base --> Soluzione non valida
    if route[0]['id'] != 0:
        print("Soluzione non valida: Il primo nodo deve essere la base !")
        return None

    #Se non sono presenti tutti gli elementi di istance in route --> Soluzione non valida
    for node in istance:
        if not (any(r['id'] == node['id'] for r in route)):
            print(f"Soluzione non valida: Il nodo con ID: {node['id']} non è presente nella soluzione!")
            return None

    #Calcolo il valore della soluzione
    #Genero il vettore delle distanze
    distance = []
    for i in range(len(route) - 1):
        id_next_node = route[i+1]['id']
        d = route[i]['distance_vector'][id_next_node]
        distance.append(d)
    distance.append(route[-1]['distance_vector'][0])

    #Genero valore di tarniess per la route
    time = 0
    tardiness = []
    for i, node in enumerate(route[1:], start=0):
        time += distance[i]
        if time < node['opening_time']:
            idle_time = node['opening_time'] - time
            time = time + idle_time
        else:
            idle_time = 0

        tardiness_node = max(0, time - node['opening_time'])
        tardiness.append(tardiness_node)

        if info is not None:
            print(f"Nodo: {node['id']}, apertura {node['opening_time']} --> arrivo: {time-idle_time}, idle: {idle_time}, tardiness: {tardiness_node}")

    #Calcolo valore della soluzione
    tot_distance = sum(distance)
    tot_tardiness = sum(tardiness)
    value_solution = tot_distance + tot_tardiness

    if info is not None:
        print(f"\tValore soluzione --> {value_solution}")
        print(f"\t - Totale distanza percorsa: {tot_distance}")
        print(f"\t - Totale tempo di tardiness {tot_tardiness}")


    return value_solution


# *******************************************
# PRIMA GREEDY = GREEDY MINIMUM OPENING TIME
# *******************************************
def greedy_minimum_opening_time(nodes):
    sorted_items = sorted(nodes, key=lambda x: x['opening_time'])

    # Inizializzo la soluzione di partenza
    route = []
    current_time = 0

    route.append(sorted_items[0])
    route[-1]['idle_tardiness'] = (0,0)

    for item in sorted_items[1:]:
        current_time += route[-1]['distance_vector'][item['id']]

        idle = max(0, item['opening_time'] - current_time)
        current_time += idle
        tardiness = max(0,current_time - item['opening_time'])

        route.append(item)
        route[-1]['idle_tardiness'] = (idle,tardiness)

    return route


# ***************************************************
# SECONDA GREEDY = GREEDY MINIMUM DISTANCE FROM ZERO
# ***************************************************
def greedy_minimum_distance_from_zero(nodes):
    sorted_items = sorted(nodes, key=lambda x: x['distance_vector'][0])

    #Inizializzo la soluzione di partenza
    route = []
    current_time = 0

    route.append(sorted_items[0])
    route[-1]['idle_tardiness'] = (0,0)

    for item in sorted_items[1:]:
        current_time += route[-1]['distance_vector'][item['id']]

        idle = max(0, item['opening_time'] - current_time)
        current_time += idle
        tardiness = max(0,current_time - item['opening_time'])

        route.append(item)
        route[-1]['idle_tardiness'] = (idle,tardiness)

    return route


# ***********************************
# TERZA GREEDY = GREEDY NEAREST NODE
# ***********************************
def nn_greedy(istance):

    #Parto dalla soluzione vuota
    nn_route = []
    current_time = 0

    #Il nodo 0 (base) viene aggiunto alla route. La route deve partire sempre dal nodo 0.
    nn_route.append(istance[0])
    nn_route[-1]['idle_tardiness'] = (0,0)

    for _ in istance[1:]:
        #L'istanza viene ordinata in base alla distanza di ciascun nodo dall'ultimo nodo aggiunto alla soluzione
        id_last_node = nn_route[-1]['id']
        #A-->B è equivalente ad B-->A
        nn_sequence = sorted(istance, key= lambda x : x['distance_vector'][id_last_node])

        for node_to_insert in nn_sequence:
            #Test di ammissibilità
            if node_to_insert not in nn_route:
                distance = nn_route[-1]['distance_vector'][node_to_insert['id']]
                current_time += distance

                idle = max(0, node_to_insert['opening_time'] - current_time)
                current_time += idle
                tardiness = max(0,current_time - node_to_insert['opening_time'])

                nn_route.append(node_to_insert)
                nn_route[-1]['idle_tardiness'] = (idle,tardiness)
                break

    return nn_route


# ***********************************
# PRIMA LOCAL SEARCH = SWAP ADJIACENT
# ***********************************
def LS_swap_adjacent(route, obj_val, istance):

    current_route = copy.deepcopy(route)
    current_obj_val  = obj_val
    n_nodes = len(current_route)
    improved = True
    moves_counter = 0
    info_extra = []

    while improved:
        improved = False
        current_route_sorted = sorted(current_route[1:], key=lambda x: (-x["idle_tardiness"][0], -x["idle_tardiness"][1] if x["idle_tardiness"][0] == 0 else 0))

        for node in current_route_sorted:
            new_route = copy.deepcopy(current_route)
            #index_node = current_route.index(node)
            index_node = next(i for i, n in enumerate(current_route) if n['id'] == node['id'])
            if index_node != len(new_route) - 1:
                  new_route[index_node], new_route[index_node+1] = new_route[index_node+1], new_route[index_node]
                  new_obj_val = calculate_objective(new_route,istance)

                  if new_obj_val < current_obj_val:
                      current_route = new_route
                      current_obj_val = new_obj_val
                      moves_counter += 1
                      improved = True
                      info_extra.append({'fo':current_obj_val, 'move':moves_counter})

                      current_time = 0
                      for i in range (1, len(current_route)):
                            current_time += current_route[i-1]['distance_vector'][i]
                            idle = max(0, current_route[i]['opening_time'] - current_time)
                            current_time += idle
                            tardiness = max(0,current_time -  current_route[i]['opening_time'])
                            current_route[i]['idle_tardiness'] = (idle, tardiness)

                            break   
    return current_route, current_obj_val, moves_counter, info_extra

# ***********************************
# SECONDA LOCAL SEARCH = CITY INSERT
# ***********************************
def LSH_city_insert(route, obj_val, istance, H):

  #Inizializzo la soluzione corrente
  current_route = copy.deepcopy(route)
  current_obj_val  = obj_val

  #Inizializzazione variabili
  n_nodes = len(current_route)
  improved = True
  moves_counter = 0

  info_extra = []

  #Eseguo la ricerca nell'intorno fino a quando non ci sono piu' mosse vantaggiose
  while improved:
    improved = False

    #Cerco h soluzioni migliori di quella corrente
    h_route_set = []
    for h in range(0, H):
        h_improved = False
        for i in range(n_nodes-1,0,-1):
            tmp_route = copy.deepcopy(current_route)
            node_to_move = tmp_route.pop(i)
            for p in range(1,len(tmp_route)+1):
                  #FILTRO
                  if i != p and (tmp_route[p-1]['distance_vector'][i] < tmp_route[p-1]['distance_vector'][p] or \
                     tmp_route[0]['distance_vector'][i] < tmp_route[0]['distance_vector'][p]):
                        h_route = copy.deepcopy(tmp_route)
                        h_route.insert(p,node_to_move)
                        #Controllo che la h_route non sia già in h_route_set
                        if h_route not in h_route_set:
                              h_obj_val = calculate_objective(h_route,istance)
                              if h_obj_val < current_obj_val:
                                  h_route_set.append({'h':h_route, 'obj_val':h_obj_val})
                                  h_improved = True
                                  break
            if h_improved:
                break
    if len(h_route_set) != 0:
          best_h = min(h_route_set,key = lambda x : x['obj_val'])
          current_route = best_h['h']
          current_obj_val = best_h['obj_val']
          moves_counter += 1
          improved = True
          info_extra.append({'fo':current_obj_val, 'move':moves_counter})

  return current_route, current_obj_val, moves_counter,info_extra


# ***********************************
# SECONDA LOCAL SEARCH = CITY INSERT TAIL
# ***********************************
def LSH_city_insertT(route, obj_val, istance, H):

  #Inizializzo la soluzione corrente
  current_route = copy.deepcopy(route)
  current_obj_val  = obj_val

  #Inizializzazione variabili
  n_nodes = len(current_route)
  improved = True
  moves_counter = 0

  info_extra = []

  #Eseguo la ricerca nell'intorno fino a quando non ci sono piu' mosse vantaggiose
  while improved:
    improved = False

    #Cerco h soluzioni migliori di quella corrente
    h_route_set = []
    for h in range(0, H):
        h_improved = False
        for i in range(n_nodes-1,0,-1):
            tmp_route = copy.deepcopy(current_route)
            node_to_move = tmp_route.pop(i)
            for p in range(len(tmp_route),0,-1):
                  #FILTRO
                  if i != p and (tmp_route[p-1]['distance_vector'][i] < tmp_route[p-1]['distance_vector'][p] or \
                     tmp_route[0]['distance_vector'][i] < tmp_route[0]['distance_vector'][p]):
                        h_route = copy.deepcopy(tmp_route)
                        h_route.insert(p,node_to_move)
                        #Controllo che la h_route non sia già in h_route_set
                        if h_route not in h_route_set:
                              h_obj_val = calculate_objective(h_route,istance)
                              if h_obj_val < current_obj_val:
                                  h_route_set.append({'h':h_route, 'obj_val':h_obj_val})
                                  h_improved = True
                                  break
            if h_improved:
                break
    if len(h_route_set) != 0:
          best_h = min(h_route_set,key = lambda x : x['obj_val'])
          current_route = best_h['h']
          current_obj_val = best_h['obj_val']
          moves_counter += 1
          improved = True
          info_extra.append({'fo':current_obj_val, 'move':moves_counter})

  return current_route, current_obj_val, moves_counter,info_extra


# ********************************
# FUNZIONI DI STAMPA DELLE GREEDY
# ********************************
def call_greedy(n=5, max_coordinate=100, max_opening_time=10, seed_coordinates=None, 
                seed_opening_times=None, greedy = 'greedy_minimum_opening_time',plot="YES"):
          function = {'greedy_minimum_opening_time' : greedy_minimum_opening_time,
                      'greedy_minimum_distance_from_zero' : greedy_minimum_distance_from_zero,
                      'nn_greedy' : nn_greedy
          }

          if greedy in function:
                instance =  generate_tsp_instance(n,max_coordinate,max_opening_time,seed_coordinates,seed_opening_times)
                sol_greedy = function[greedy](instance)
                sol_greedy_val = calculate_objective(sol_greedy,instance)

                if plot is not None:
                    plot_tsp_nodes_link(sol_greedy,greedy,str(sol_greedy_val))
                else:
                    return sol_greedy, sol_greedy_val

def compare_greedy(n=5, max_coordinate=100, max_opening_time=10, seed_coordinates=None, seed_opening_times=None,plot ="YES"):

    sol_Gmot, val_Gmot = call_greedy(n,max_coordinate,max_opening_time,seed_coordinates,seed_opening_times,'greedy_minimum_opening_time',None)
    sol_Gmdfz, val_Gmdfz = call_greedy(n,max_coordinate,max_opening_time,seed_coordinates,seed_opening_times,'greedy_minimum_distance_from_zero',None)
    sol_Gnn, val_Gnn = call_greedy(n,max_coordinate,max_opening_time,seed_coordinates,seed_opening_times,'nn_greedy',None)
    if plot is not None:
        plt.figure(figsize=(18, 6))
        plt.subplot(1, 3, 1)
        plot_tsp_nodes_link_nofigure(sol_Gmot,'greedy_minimum_opening_time',str(val_Gmot))
        plt.subplot(1, 3, 2)
        plot_tsp_nodes_link_nofigure(sol_Gmdfz,'greedy_minimum_distance_from_zero',str(val_Gmdfz))
        plt.subplot(1, 3, 3)
        plot_tsp_nodes_link_nofigure(sol_Gnn,'nn_greedy',str(val_Gnn))
        plt.tight_layout()
        plt.show()

    else:
        return val_Gmot, val_Gmdfz, val_Gnn
    


# *************************************
# FUNZIONI DI STAMPA DELLE LOCAL SEARCH
# *************************************

def call_LocalSearch(n=5, max_coordinate=100, max_opening_time=10, seed_coordinates=None, seed_opening_times=None, greedy = 'greedy_minimum_opening_time', local_search= 'LSH_city_insert', H=1, plot="YES"):
      function = {
          'greedy_minimum_opening_time' : greedy_minimum_opening_time,
          'greedy_minimum_distance_from_zero' : greedy_minimum_distance_from_zero,
          'nn_greedy' : nn_greedy,
          'LS_swap_adjacent' : LS_swap_adjacent,
          'LS_swap_adjacent' : LS_swap_adjacent,
          'LSH_city_insert' : LSH_city_insert,
          'LSH_city_insertT' : LSH_city_insertT
      }

      if greedy in function and local_search in function:
            instance =  generate_tsp_instance(n,max_coordinate,max_opening_time,seed_coordinates,seed_opening_times)
            sol_greedy = function[greedy](instance)
            sol_greedy_val = calculate_objective(sol_greedy,instance)
            if local_search == "LSH_city_insert" or local_search == "LSH_city_insertT":
                  LS_route, LS_value, LS_moves, LS_extra_info = function[local_search](sol_greedy,sol_greedy_val,instance,H)
            else:
                  LS_route, LS_value, LS_moves, LS_extra_info = function[local_search](sol_greedy,sol_greedy_val,instance)

            if plot is not None:
                  plt.figure(figsize=(18, 6))

                  plt.subplot(1, 3, 1)
                  plot_tsp_nodes_link_nofigure(sol_greedy,greedy,str(sol_greedy_val))

                  plt.subplot(1, 3, 2)
                  plot_tsp_nodes_link_nofigure(LS_route,local_search,str(LS_value))

                  plt.subplot(1, 3, 3)
                  moves = [d['move'] for d in LS_extra_info]
                  fo_s = [d['fo'] for d in LS_extra_info]

                  plt.scatter(0, sol_greedy_val, color='red', label="Greedy value")
                  sns.lineplot(x=moves, y=fo_s, marker='o', linestyle='-', color='b',label="FO Value")
                  plt.plot([0, moves[0]], [sol_greedy_val, fo_s[0]], color='b', linestyle='-')

                  plt.title(f"Trend FO - Moves {LS_extra_info[-1]['move']}")
                  plt.xlabel("Moves")
                  plt.ylabel("FO Val")

                  plt.legend()
                  plt.grid(True)
                  plt.tight_layout()
                  plt.show()
            else:
              return local_search, LS_extra_info