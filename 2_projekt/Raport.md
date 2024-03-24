# Ingeligencja obliczeniowa
## Projekt 2: STRIPS
Olgierd Piofczyk, Kaja Dzielnicka

# Na 3.0
## Wybór dziedziny STRIPS i definicja problemów

Wybrana dziedzina STRIPS dotyczy układania klocków na stole, co jest klasycznym problemem w dziedzinie planowania i sztucznej inteligencji. Zadanie polega na przenoszeniu klocków tak, aby osiągnąć określony układ końcowy, zaczynając od danego układu początkowego. Problemy przez nas zdefiniowane to trzy różne scenariusze układania klocków:
1.  ```
            D    A
            B -> E C
        E A C    B D
2.  ```
        A
        B
        C -> A
        D    E D
        E    C B

3.   ```
                 A
        E   D    C B
        B A C -> D E
        ```

## Rozwiązanie problemu metodą forward planning

Rozwiązanie problemów polega na zastosowaniu metody forward planning, która systematycznie przeszukuje przestrzeń stanów od stanu początkowego do stanu końcowego, rozważając wszystkie możliwe akcje. Dla każdego z zdefiniowanych problemów algorytm forward planning jest użyty do znalezienia sekwencji ruchów, które transformują układ początkowy w układ końcowy. Oto rozwiązania dla każdego z problemów:
1. Problem 1
   - move_d_from_b_to_table
   - move_b_from_c_to_table
   - move_e_from_table_to_b
   - move_a_from_table_to_e
   - move_c_from_table_to_d
2. Problem 2
   - move_a_from_b_to_table
   - move_b_from_c_to_table
   - move_c_from_d_to_table
   - move_d_from_e_to_b
   - move_e_from_table_to_c
   - move_a_from_table_to_e
3. Problem 3
   - move_e_from_b_to_table
   - move_b_from_table_to_e
   - move_d_from_c_to_table
   - move_c_from_table_to_d
   - move_a_from_table_to_b

## Propozycja heurystyki do problemu

Prezentowana heurystyka `count_mismatches` służy do oceny obecnego stanu względem stanu koncowego poprzez zliczanie liczby błędów (niedopasowań). Błąd jest zliczany, gdy pozycja klocka w obecnym stanie nie odpowiada jego pozycji w stanie docelowym. Kod heurystyki:
``` python
def count_mismatches(state, goal):
    error = 0
    for key, val in goal.items():
        assert key in state
        error += val == state[key]

    return -error
```
W wyniku eksperymentów porównano czasy działania algorytmu z heurystyką (heuristic) oraz bez niej (naive). Czas dla każdego przypadku został zmierzony 100 razy żeby zredukować wpływ losowych czynników na czas wykonania. Prezentowane wartości to średnie.
```
{'case_1_heuristic': 1857514.0,
 'case_1_naive':     174237136.0,
 'case_2_heuristic': 946137.0,
 'case_2_naive':     121888077.0,
 'case_3_heuristic': 1375991.0,
 'case_3_naive':     185659843.0}
```
Otrzymane wyniki pokazują, że zastosowanie heurystyki pozwala znacząco zredukować czas potrzebny na znalezienie rozwiązania, nawet o kilka rzędów wielkości, co demonstruje skuteczność heurystyki w poprawie wydajności algorytmu planowania.

# Na 4.0
## Zdefiniowanie podceli dla problemów

Dla każdego z problemów zdefiniowano specyficzne etapy pośrednie, które przybliżały układ początkowy do układu końcowego. Oto zdefiniowane podcele dla każdego z problemów:
1.  ```
                C
                E
           D -> A ->   A -> A
           B    D    C B    E C
       E A C    B    E D    B D
2.  ```
        A    E
        B    D
        C -> C -> A   -> A
        D    B    E C    E D
        E    A    D B    C B
3.   ```
                 D
                 C
              -> B -> C   ->   A
        E   D    A    D E    C B
        B A C    E    B A    D E
        ```

## Rozwiązanie ponownie problemów z podcelami z heurystyką i bez

1. Problem 1
   1. ```
                C
                E
           D -> A
           B    D
       E A C    B
       ```
        - move_d_from_b_to_table
        - move_b_from_c_to_table
        - move_d_from_table_to_b
        - move_a_from_table_to_d
        - move_e_from_table_to_a
        - move_c_from_table_to_e
   2. ```
       C
       E
       A ->   A
       D    C B
       B    E D
       ```
        - move_c_from_e_to_table
        - move_e_from_a_to_table
        - move_c_from_table_to_e
        - move_a_from_d_to_c
        - move_d_from_b_to_table
        - move_b_from_table_to_d
        - move_a_from_c_to_b
   3. ```
         A    A
       C B -> E C
       E D    B D
       ```
        - move_b_from_d_to_table
        - move_a_from_c_to_table
        - move_c_from_e_to_d
        - move_a_from_table_to_e
2. Problem 2
   1. ```
        A    E
        B    D
        C -> C
        D    B
        E    A
        ```
        - move_a_from_b_to_table
        - move_b_from_c_to_a
        - move_c_from_d_to_b
        - move_d_from_e_to_c
        - move_e_from_table_to_d
   2. ```
        E
        D
        C -> A
        B    E C
        A    D B
        ```
        - move_e_from_d_to_table
        - move_d_from_c_to_table
        - move_c_from_b_to_table
        - move_b_from_a_to_table
        - move_e_from_table_to_d
        - move_a_from_table_to_e
        - move_c_from_table_to_b
   3. ```
        A      A
        E C -> E D
        D B    C B
        ```
        - move_c_from_b_to_table
        - move_a_from_e_to_b
        - move_e_from_d_to_c
        - move_a_from_b_to_e
        - move_d_from_table_to_b
3. Problem 3
   1. ```
                 D
                 C
              -> B
        E   D    A
        B A C    E
        ```
        - move_e_from_b_to_table
        - move_d_from_c_to_table
        - move_b_from_table_to_e
        - move_c_from_table_to_d
        - move_a_from_table_to_b
   2. ```
        D
        C
        B -> C
        A    D E
        E    B A
        ```
        - move_d_from_c_to_table
        - move_c_from_b_to_table
        - move_b_from_a_to_table
        - move_d_from_table_to_b
        - move_c_from_table_to_d
        - move_a_from_e_to_table
        - move_e_from_table_to_a
   3. ```
        C        A
        D E -> C B
        B A    D E
        ```
        - move_c_from_d_to_table
        - move_d_from_b_to_table
        - move_e_from_a_to_table
        - move_b_from_table_to_e
        - move_a_from_table_to_b
        - move_c_from_table_to_d

Tak jak poprzednio, porównano czasy działania algorytmu z heurystyką (heuristic) oraz bez niej (naive).
```
{'case_1_with_sub-goals_heuristic': 14951297.0,
 'case_1_with_sub-goals_naive':     976458129.0,
 'case_2_with_sub-goals_heuristic': 8175869.0,
 'case_2_with_sub-goals_naive':     790803520.0,
 'case_3_with_sub-goals_heuristic': 15927340.0,
 'case_3_with_sub-goals_naive':     1368617626.0}
```
Wyniki potwierdzają, że zastosowanie heurystyki pozwala znacząco zredukować czas potrzebny na znalezienie rozwiązania, nawet o kilka rzędów wielkości, co demonstruje skuteczność heurystyki w poprawie wydajności algorytmu planowania.