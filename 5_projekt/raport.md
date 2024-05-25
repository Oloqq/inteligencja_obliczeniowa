# Ingeligencja obliczeniowa

## Projekt 5: Przestrzenie Ciągłe

Olgierd Piofczyk, Kaja Dzielnicka

## Środowisko: Pendulum-v1

W ramach projektu zastosowaliśmy środowisko `Pendulum-v1` z biblioteki `gym`. Jest to klasyczny problemem sterowania, w którym zadaniem agenta jest balansowanie wahadła w pionie, startując z dowolnej pozycji. Agent otrzymuje negatywne nagrody za odchylenia od pionu oraz za dużą prędkość kątową.

## Algorytm: SAC

SAC jest algorytmem wzmacniającego uczenia, który łączy metody aktora-krytyka z maksymalizacją entropii. Celem jest nie tylko maksymalizacja nagrody, ale także eksploracja różnych działań.
