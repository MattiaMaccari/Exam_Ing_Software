# Progetto TSP
<details>
<summary> Apri per vedere la spiegazione </summary>

## TSP con finestre temporali (TS-TW):
* A partire dalla base (nodo 0) un tecnico deve rifornire n vending machines poste in n siti diversi, e rientrare alla base.
* Ogni sito i apre al tempo 𝑡_𝑖:
* Se si arriva prima occorre attendere fino all’apertura;
* Se si arriva al tempo 𝑡_𝑗>𝑡_𝑖 si paga una penale di (𝑡_𝑗−𝑡_𝑖).
* Noti i tempi di percorrenza da sito a sito e alla base, si determini il tour di costo minimo (durata + penalità) che visita tutti i siti e la base, partendo al tempo 𝑡_0.
</details>

## Travelling Salesman Problem (TSP)

Il problema del commesso viaggiatore (TSP – Traveling Salesman Problem) è un problema combinatorio classico noto per essere NP-hard, ovvero non esiste alcun algoritmo noto in grado di risolverlo in tempo polinomiale in tutti i casi. L’obiettivo del TSP consiste nel trovare il ciclo hamiltoniano di costo minimo che visiti ciascun nodo esattamente una volta.

<img src="./Images/tsp.png" alt="TSP" width="300">

<br>
Nel problema del commesso viaggiatore con tempi di apertura, ogni nodo 𝑖 i può essere visitato solo a partire da un determinato istante di apertura 𝑡_𝑖.

Questo vincolo temporale aggiuntivo complica ulteriormente il problema:
**La presenza di tempi di apertura riduce lo spazio delle soluzioni ammissibili, escludendo molti percorsi che sarebbero validi nel TSP classico.**

Se un nodo viene raggiunto prima del suo tempo di apertura, il commesso deve attendere, introducendo periodi di inattività (**idle time**) che incidono sull’efficienza complessiva del tour.

Dal punto di vista della teoria della complessità, il TSP con tempi di apertura rimane NP-hard come il TSP classico, ma nella pratica risulta più difficile da risolvere per via dei vincoli temporali.

## Struttura del progetto

Questo progetto implementa e confronta diverse strategie di risoluzione del **Travelling Salesman Problem (TSP)**.
Il seguente codice è organizzato in moduli che permettono di:
- Generare istanze del problema
- Applicare algoritmi greedy
- Applicare tecniche di local search
- Applicare varianti di tabu search
- Applicare una iterated local search
- Visualizzare graficamente le soluzioni

## Algoritmi implementati

Nel progetto vengono illustrate le seguenti procedure:

#### Greedy (3 procedure)
1. `greedy_minimum_opening_time`  
2. `greedy_minimum_distance_from_zero`  
3. `nn_greedy`  

#### Local Search (3 procedure)
1. `LS_swap_adjacent`  
2. `LSH_city_insert`
3. `LSH_city_insertT`

#### Tabu Search (2 procedure)
1. `information_guided_tabu_searchAR`  
2. `tabu_search_city_insertAR`  

#### Iterated Local Search (1 procedura)
1. `iterated_local_search`  



## Spiegazione dei vari moduli/algoritmi

- **Generazione istanze TSP**  <br>

  La funzione generate_tsp_instance, genera un’istanza e ha i seguenti parametri:
  * n : numero di nodi
  * max_coordinate : Valore coordinate massimo
  * max_opening_time : valore massimo apertura nodo
  * seed_coordinates : seme per generazione casuale e ripetibile delle coordinate
  * seed_opening_times : seme per generazione casuale e ripetibile dei tempi di apertura dei nodi
---
- **Visualizzazione**  <br>

  Funzioni per stampare le istanze e rappresentarle graficamente:
  - `plot_tsp_nodes`: visualizza solo i nodi
  - `plot_tsp_nodes_link`: visualizza nodi e collegamenti con frecce
---
- **Algoritmi Greedy**<br>

  1. **greedy_minumum_opening_time**costruisce una soluzione eseguendo le seguenti operazioni:
      * Ordina i nodi dell'istanza, in ordine non decrescente, in base all'opening_time di ciascun nodo.
      * Seleziona un nodo alla volta dal vettore dei nodi ordinati e lo collega con il successivo.

  2. **greedy_minimum_distance_from_zero**
  costruisce una soluzione eseguendo le seguenti operazioni:
      * Ordina i nodi dell'istanza in base alla distanza crescent dalla base (nodo 0).
      * Seleziona un nodo alla volta dal vettore dei nodi ordinati e lo collega con il successivo.
  
  3. **greedy Nearest Node** costruisce una soluzione eseguendo le seguenti operazioni:
      * Seleziona, per ciascun nodo, il nodo adiacente più vicino.
      * Ad ogni passo, vengono identificati i nodi adiacenti e si sceglie quello con il costo minimo, aggiornando progressivamente la soluzione con decisioni localmente ottimali.

  <br>
---
- **Local Search**
  1. **Swap Adjacent**  
  * Strategia: **First Improvement**, cerca di migliorare iterativamente una route scambiando due nodi adiacenti, privilegiando quelli con maggiore idle o tardiness <br>

    <img src="./Images/LS1.png" alt="TSP" width="350">

  <br>

  2. **City Insert**
  * Strategia: **h Improvement** (la migliore delle h soluzioni che migliorano l'ottimo corrente).
  * La ricerca nell'intorno procede fino a determinare h miglioramenti.
  * Intorno ottenuto dalla cancellazione di 1 nodo nella route e dal suo reinserimento in un altro punto (partendo dall’inizio).
  * I nodi vengono cancellati a partire dalla fine della route.
  * Il nodo i viene reinserito nella posizione p solo se la sua distanza dal nodo precedente (p-1) o dal nodo iniziale è inferiore a quella del nodo attualmente presente in p.
  
    <img src="./Images/LS2.png" alt="TSP" width="350">

  <br>

  3. **City Insert Tail**
  * Strategia: **h Improvement** (la migliore delle h soluzioni che migliorano l'ottimo corrente).
  * La ricerca nell'intorno procede fino a determinare h miglioramenti.
  * Intorno ottenuto dalla cancellazione di 1 nodo nella route e dal suo reinserimento in un altro punto (partendo dalla fine).
  * I nodi vengono cancellati a partire dalla fine della route.
  * Il nodo i viene reinserito nella posizione p solo se la sua distanza dal nodo precedente (p-1) o dal nodo iniziale è inferiore a quella del nodo attualmente presente in p.

    <img src="./Images/LS3.png" alt="TSP" width="350">
  
  <BR>

---
- **Tabu Search**  
  Implementazioni delle due varianti di tabu search per esplorare lo spazio delle soluzioni evitando cicli.

- **Iterated Local Search**  
  Una procedura iterativa che applica ripetutamente local search con perturbazioni per uscire da minimi locali.

