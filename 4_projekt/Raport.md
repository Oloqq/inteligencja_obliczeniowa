1.  Napisz własne dowolne środowisko Gymnasium.
2.  Napisz program rozwiązujący problem w utworzonym środowisku.
3.  Agentowi udaje się ukończyć grę / rozwiązać problem.
4.  Napisz sprawozdanie (około 2-3 strony A4), w którym opiszesz swoją implementację
środowiska i problemu, wykorzystany algorytm oraz przeprowadzone eksperymenty
z AI

# Środowisko
W naszym środowisku dzielny Ślązak musi unikać spadających mu na głowę goroli.

![](2024-05-05-20-04-31.png)

![](2024-05-05-20-04-43.png)

Po instalacji modułu grę uruchamia się komendą:
- `minecraft -m human` dla ręcznej kontroli
- `minecraft -m random` dla uruchomienia agenta wykonującego losowe ruchy

Implementując nasze środowisko wzorowaliśmy się na repozytorium `https://github.com/Talendar/flappy-bird-gym`.




# Agent