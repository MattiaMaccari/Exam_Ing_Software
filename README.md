# Progetto TSP

## TSP con finestre temporali (TS-TW):
* A partire dalla base (nodo 0) un tecnico deve rifornire n vending machines poste in n siti diversi, e rientrare alla base.
* Ogni sito i apre al tempo 𝑡_𝑖:
* Se si arriva prima occorre attendere fino all’apertura;
* Se si arriva al tempo 𝑡_𝑗>𝑡_𝑖 si paga una penale di (𝑡_𝑗−𝑡_𝑖).
* Noti i tempi di percorrenza da sito a sito e alla base, si determini il tour di costo minimo (durata + penalità) che visita tutti i siti e la base, partendo al tempo 𝑡_0.

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

  1. **greedy_minumum_opening_time** costruisce una soluzione eseguendo le seguenti operazioni:
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

    <img src="./Images/LS1.png" alt="TSP" width="400">

  <br>

  2. **City Insert**
  * Strategia: **h Improvement** (la migliore delle h soluzioni che migliorano l'ottimo corrente).
  * La ricerca nell'intorno procede fino a determinare h miglioramenti.
  * Intorno ottenuto dalla cancellazione di 1 nodo nella route e dal suo reinserimento in un altro punto (partendo dall’inizio).
  * I nodi vengono cancellati a partire dalla fine della route.
  * Il nodo i viene reinserito nella posizione p solo se la sua distanza dal nodo precedente (p-1) o dal nodo iniziale è inferiore a quella del nodo attualmente presente in p.
  
    <img src="./Images/LS2.png" alt="TSP" width="400">

  <br>

  3. **City Insert Tail**
  * Strategia: **h Improvement** (la migliore delle h soluzioni che migliorano l'ottimo corrente).
  * La ricerca nell'intorno procede fino a determinare h miglioramenti.
  * Intorno ottenuto dalla cancellazione di 1 nodo nella route e dal suo reinserimento in un altro punto (partendo dalla fine).
  * I nodi vengono cancellati a partire dalla fine della route.
  * Il nodo i viene reinserito nella posizione p solo se la sua distanza dal nodo precedente (p-1) o dal nodo iniziale è inferiore a quella del nodo attualmente presente in p.

    <img src="./Images/LS3.png" alt="TSP" width="400">
  
  <BR>

---
- **Tabu Search**
  1. **Information Guided**  
  * La funzione information_guided_tabu_searchA implementa una variante della Tabu Search per ottimizzare un percorso, spostando iterativamente i nodi in base a una priorità calcolata su idle_tardiness.
  * Tiene traccia delle soluzioni migliori evitando cicli grazie a una lista Tabu, ma consente eccezioni se si trova un miglioramento (criterio di aspirazione). 
  * Il processo termina dopo un numero definito di iterazioni senza miglioramenti. 
  * Restituisce il miglior percorso trovato e informazioni sull’evoluzione della ricerca.
  
  <br>

  2. **City Insert**
  * La funzione tabu_search_city_insertA applica la Tabu Search rimuovendo e reinserendo nodi del percorso per esplorare soluzioni vicine.
  * Se una mossa è Tabu, può comunque essere accettata se migliora la soluzione ottima (criterio di aspirazione).
  * Il processo continua finché non si verificano troppi passi senza miglioramenti.
  * Restituisce il miglior percorso trovato e informazioni sull’evoluzione della ricerca.
  
<br>

---
- **Iterated Local Search**  

  Questa funzione implementa un algoritmo iterativo di ricerca locale guidata per ottimizzare una soluzione su una data istanza di problema.
  * Inizia generando una soluzione greedy e migliorandola tramite una procedura di LS (LS_swap_adjacent). 
  * Successivamente entra in un ciclo iterativo in cui perturba la soluzione corrente con una mossa di diversificazione e la migliora ulteriormente con la ricerca locale.  
  * La funzione tiene traccia dell’evoluzione della funzione obiettivo ad ogni iterazione e restituisce la migliore soluzione e il suo valore.

  <br>

  **MOSSA DI DIVERSIFICAZIONE:**

    <img src="./Images/MOVE1.png" alt="TSP" width="400">

    <br>

    Come evidenziato nell'immagine la mossa di diversificazione della procedura **Iterated local search** si compone, di fatto, di altre due sotto mosse che vengono applicate con probabilità randomica.

    In particolare la funzione **"modify_sequence"**, che si occupa di attuare la mossa, esegue i seguenti passi:

    * Fa una copia della route in ingresso per poterci lavorare in sicurezza.
    * Calcola un numero di iterazioni casuale da 1 a 3.
    * Per il numero di iterazioni calcolato, calcola un indice **i** casuale che può andare da 1 alla lunghezza della lista meno i due elementi finali.
    Calcola, poi, un indice **j** casuale che va da **i+1** alla lunghezza della lista escluso l'elemento finale.
    * Una volta fatti questi calcoli l'indice **j** sarà sicuramente più grande di **i** ed il primo e l'ultimo elemento della lista rimarranno invariati.
    * A questo punto viene estratto un numero casuale compreso tra zero e uno.
    * Se il numero appena estratto è più piccolo di 0.5 allora gli elementi della lista in posizione **i** e in posizione **j** vengono scambiati.
    * Se il numero estratto è maggiore o uguale di 0.5 allora la sotto sequenza che va da **i** a **j** viene invertita.
  ---
  **VISUALIZZAZIONE GRAFICA DELLA MOSSA**
     
    Scambio degli elementi in posizione **i** e posizione **j**:
    <img src="./Images/MOVE2.png" alt="TSP" width="400">

    Inversione della sotto sequenza identificata dagli indici **i** e **j**:
    <img src="./Images/MOVE3.png" alt="TSP" width="400">
<br>

---

## SEZIONE DI TEST - INTEGRATION E UNIT TEST

  - **INTEGRATION TEST**

    - 

