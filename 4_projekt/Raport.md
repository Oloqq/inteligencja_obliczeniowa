# Środowisko
W naszym środowisku dzielny Ślązak musi unikać spadających mu na głowę goroli.

![](2024-05-05-20-04-31.png)

![](2024-05-05-20-04-43.png)

Po instalacji modułu grę uruchamia się komendą:
- `minecraft -m human` dla ręcznej kontroli
- `minecraft -m random` dla uruchomienia agenta wykonującego losowe ruchy

Implementując nasze środowisko wzorowaliśmy się na repozytorium `https://github.com/Talendar/flappy-bird-gym`. Środowisko zdefiniowane jest w `minecraft/envs/minecraft_env.py`, jest to środowisko dyskretne gdzie agent może w każdym ruchu wykonać jedną z 3 akcji (`class Actions`): 
- pozostanie w spoczynku
- ruch w lewo
- ruch w prawo

Gracz zdobywa punkt za każdego przeciwnika który rozbije się o podłogę, oraz traci punkty za każdego który go trafi. Gra kończy się po określonej z góry ilości ruchów.

# Program rozwiązujący problem w utworzonym środowisku

