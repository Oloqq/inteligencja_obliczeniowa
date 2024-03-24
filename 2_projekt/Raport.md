# Ingeligencja obliczeniowa
## Projekt 2: STRIPS
Olgierd Piofczyk, Kaja Dzielnicka

# Na 3.0
1. **Wybór dziedziny STRIPS i definicja problemów**

Wybrana dziedzina STRIPS dotyczy układania klocków na stole, co jest klasycznym problemem w dziedzinie planowania i sztucznej inteligencji. Zadanie polega na przenoszeniu klocków tak, aby osiągnąć określony układ końcowy, zaczynając od danego układu początkowego. Problemy przez nas zdefiniowane to trzy różne scenariusze układania klocków:
-   ```
        D    A
        B -> E C
    E A C    B D
    ```

-   ```
    A
    B
    C -> A
    D    E D
    E    C B
    ```

-   ```
               A
    E   D    C B
    B A C -> D E
    ```
2. **Rozwiązanie problemu metodą forward planning**

Rozwiązanie problemów polega na zastosowaniu metody forward planning, która systematycznie przeszukuje przestrzeń stanów od stanu początkowego do stanu końcowego, rozważając wszystkie możliwe akcje. Dla każdego z zdefiniowanych problemów algorytm forward planning jest użyty do znalezienia sekwencji ruchów, które transformują układ początkowy w układ końcowy. Oto rozwiązania dla każdego z problemów:
-   ```
    rozwiazanie dla problemu 1
    ```
-   ```
    rozwiazanie dla problemu 2
    ```
-   ```
    rozwiazanie dla problemu 3
    ```

3. **Propozycja heurystyki do problemu**

Prezentowana heurystyka `count_mismatches` służy do oceny obecnego stanu względem stanu koncowego poprzez zliczanie liczby błędów (niedopasowań). Błąd jest zliczany, gdy pozycja klocka w obecnym stanie nie odpowiada jego pozycji w stanie docelowym. Kod heurystyki: 
``` python
def count_mismatches(state, goal):
    fuckup = 0
    for key, val in goal.items():
        assert key in state
        fuckup += val == state[key]

    return -fuckup
``` 
W wyniku eksperymentów porównano czasy działania algorytmu z heurystyką oraz bez niej (metoda naiwna).
```
{'case_1_heuristic': 1857514.0,
 'case_1_naive':     174237136.0,
 'case_2_heuristic': 946137.0,
 'case_2_naive':     121888077.0,
 'case_3_heuristic': 1375991.0,
 'case_3_naive':     185659843.0}
```
Otrzymane wyniki pokazują, że zastosowanie heurystyki pozwala znacząco zredukować czas potrzebny na znalezienie rozwiązania, nawet o dwa rzędy wielkości, co demonstruje skuteczność heurystyki w poprawie wydajności algorytmu planowania.

# Na 4.0
TO DO
