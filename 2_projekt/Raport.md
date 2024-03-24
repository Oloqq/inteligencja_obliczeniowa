# Ingeligencja obliczeniowa
## Projekt 2: STRIPS
Olgierd Piofczyk, Kaja Dzielnicka

# Na 3.0
1. dziedzina ukladanie klocow na stole 
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
2.

3. zlicza poprawnosc obecnego stanu wzgledem stanu koncowego 
``` python
def count_mismatches(state, goal):
    fuckup = 0
    for key, val in goal.items():
        assert key in state
        fuckup += val == state[key]

    return -fuckup
```
wyniki dla ebfyhsebf:
-
-
-
Czas spadł o nawet 2 rzedy wielkosci

# Na 4.0

