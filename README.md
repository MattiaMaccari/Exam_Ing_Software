# Progetto TSP - Algoritmi Greedy, Local Search e Tabu Search

Questo progetto implementa e confronta diverse strategie di risoluzione del **Travelling Salesman Problem (TSP)**.  
Il codice è organizzato in moduli che permettono di:
- Generare istanze del problema
- Applicare algoritmi greedy
- Applicare tecniche di local search
- Applicare varianti di tabu search
- Applicare una iterated local search
- Visualizzare graficamente le soluzioni

---

## Algoritmi implementati

Nel progetto vengono illustrate le seguenti procedure:

### Greedy (3 procedure)
1. `greedy_minimum_opening_time`  
2. `greedy_minimum_distance_from_zero`  
3. `nn_greedy`  

### Local Search (2 procedure)
1. `LS_swap_adjacent`  
2. `LSH_city_insert`
3. `LSH_city_insertT`

### Tabu Search (2 procedure)
1. `information_guided_tabu_searchAR`  
2. `tabu_search_city_insertAR`  

### Iterated Local Search (1 procedura)
1. `iterated_local_search`  

---

## Struttura del progetto

- **Generazione istanze TSP**  
  Funzioni per creare nodi con coordinate casuali, tempi di apertura e matrice delle distanze.

- **Visualizzazione**  
  Funzioni per stampare le istanze e rappresentarle graficamente:
  - `plot_tsp_nodes`: visualizza solo i nodi
  - `plot_tsp_nodes_link`: visualizza nodi e collegamenti con frecce

- **Algoritmi Greedy**  
  Implementazioni delle tre procedure greedy per costruire soluzioni iniziali.

- **Local Search**  
  Implementazioni delle due varianti di ricerca locale per migliorare le soluzioni greedy.

- **Tabu Search**  
  Implementazioni delle due varianti di tabu search per esplorare lo spazio delle soluzioni evitando cicli.

- **Iterated Local Search**  
  Una procedura iterativa che applica ripetutamente local search con perturbazioni per uscire da minimi locali.
