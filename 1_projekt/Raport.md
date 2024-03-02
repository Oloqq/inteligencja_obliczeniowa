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
TODO: Porównaj kilka (co najmniej Negamax z i bez odcięcia alfa-beta, z dwoma różnymi ustawienia maksymalnej głębokości) algorytmy dla gier deterministycznych na deterministycznych i probabilistycznych wariantach twojej gry.

TODO: Napisz kod, który mierzy średni czas spędzony na wybieraniu akcji przez każdy wariant AI. Dodaj zmierzone czasy do raportu