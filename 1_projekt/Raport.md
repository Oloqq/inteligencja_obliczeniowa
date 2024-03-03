# Ingeligencja obliczeniowa
## Projekt 1: probabilistyczne warianty gier
Olgierd Piofczyk, Kaja Dzielnicka

# Na 3.0
## Opis gry
Zaimplementowano grę Nimby, będącą wariantem gry Nim, ale z dodatkowym 10% prawdopodobieństwem, że gracz wykonujący ruch weźmie o jeden element mniej z wybranego stosu, niż zamierzał. Gra zaczyna się z 4 stosami, każdy z 5 elementami. Gracze na przemian usuwają dowolną liczbę elementów z jednego stosu. Gracz, który zabierze ostatni element, przegrywa grę.

## Porównanie deterministycznego i probabilistycznego wariantu
Przeprowadzono testy na dwóch graczach, z których każdy korzystał z algorytmu Negamax z różnymi maksymalnymi głębokościami przeszukiwania drzewa gry. Testy odbyły się na deterministycznym i probabilistycznym wariancie gry.

Stworzono dwóch graczy o głębokościach 3 i 5 ruchów, którzy na przemian dostawali możliwość rozpoczynania gry. W każdym przypadku przeprowadzono 100 gier, zapisując wyniki.

### Statystyki po uruchomieniu gier 100 razy
W wariancie deterministycznym, za każdym razem wygrywa gracz o większej głębokości.

W wariancie probabilistycznym, gracz o mniejszej głębokości wygrał 53 ze 100 gier

```
depth 3
{'deterministic': {'wins': 0, 'losses': 100}, 'probabilistic': {'wins': 53, 'losses': 47}}

depth 5
{'deterministic': {'wins': 100, 'losses': 0}, 'probabilistic': {'wins': 47, 'losses': 53}}
```

# Na 4.0
Deafultowa wersja algorytmu Negamax w module easyAI zawiera prunig, który pozwala na przyspieszenie obliczeń. Sprawdzono jak prunig wpływa na ich czas. Aby to zrobić, zmodyfikowano plik modułu easyAI `easyAI\AI\NonRecursiveNegamax.py`, konkretnie podmieniono linię 142
```
prune_time = states[depth].alpha >= states[depth].beta
```
na
```
prune_time = False
```
Użyto NonRecursiveNegamax (ze względu na prostotę modyfikacji) i zauważono, że wersja nierurkurencyjna z prunigiem działa około 10 razy szybciej niż wersja rekurencyjna z prunigiem.

Aby obliczyć czas wykonania ruchu, zmodyfikowano klasę PlayerReport, która przechowuje wyniki gracza. Zmodyfikowano metodę ask_move, która zwraca ruch wybrany przez algorytm. Dodano pomiar czasu wykonania ruchu. 'time' w wynikach oznacza średni czas na ruch.

## Wyniki wersji rekurencyjnej, z pruningiem:
```json
depth 3
{
    "deterministic": {
        "wins": 0,
        "losses": 100,
        "time": 0.0002854002846611871,
        "moves": 1854
    },
    "probabilistic": {
        "wins": 59,
        "losses": 41,
        "time": 0.006065457039713793,
        "moves": 1783
    }
}

depth 5
{
    "deterministic": {
        "wins": 100,
        "losses": 0,
        "time": 0.0027831299019477128,
        "moves": 1854
    },
    "probabilistic": {
        "wins": 41,
        "losses": 59,
        "time": 0.062839291166604,
        "moves": 1783
    }
}
```

## Wyniki wersji nierekurencyjnej:
```json
depth 3
{
    "deterministic": {
        "wins": 0,
        "losses": 100,
        "time": 0.0005652362943146924,
        "moves": 1849
    },
    "probabilistic": {
        "wins": 61,
        "losses": 39,
        "time": 0.000653052490029559,
        "moves": 1788
    }
}

depth 5
{
    "deterministic": {
        "wins": 100,
        "losses": 0,
        "time": 0.005321090965415414,
        "moves": 1849
    },
    "probabilistic": {
        "wins": 39,
        "losses": 61,
        "time": 0.006640563475205594,
        "moves": 1788
    }
}
```

## Wyniki wersji nierekurencyjnej bez pruningu:
```json
depth 3
{
    "deterministic": {
        "wins": 0,
        "losses": 100,
        "time": 0.0033423580475349197,
        "moves": 1847
    },
    "probabilistic": {
        "wins": 69,
        "losses": 31,
        "time": 0.0038709631491428316,
        "moves": 1852
    }
}

depth 5
{
    "deterministic": {
        "wins": 100,
        "losses": 0,
        "time": 0.25229950459763756,
        "moves": 1847
    },
    "probabilistic": {
        "wins": 31,
        "losses": 69,
        "time": 0.3141499229950215,
        "moves": 1852
    }
}
```
Czas obliczania pojedynczego ruchu zwiększył o rząd wielkości dla głębokości 3, i 3 rzędy wielkości dla głębokości 5. Widać, że prunig znacząco przyspiesza obliczenia. 