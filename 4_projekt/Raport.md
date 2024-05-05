# Ingeligencja obliczeniowa
## Projekt 4: TS 1 - Podstawy Gymnasium
Olgierd Piofczyk, Kaja Dzielnicka

## Środowisko
W ramach projektu zastosowaliśmy popularną postać z gry Minecraft, Steve'a, który znajduje się w jaskini. Jego zadaniem jest unikanie spadających na niego creeperów, które są znanymi przeciwnikami w świecie Minecrafta. Środowisko to zostało zainspirowane mechanikami i estetyką tej gry, a realizacja projektu odbyła się przy użyciu biblioteki `gymnasium`, co umożliwia łatwe testowanie różnych strategii unikania.

![](2024-05-05-20-04-31.png)

![](2024-05-05-20-04-43.png)

## Instalacja i uruchamianie gry
Gra wymaga instalacji odpowiednich modułów Pythona, po których zainstalowaniu można ją uruchomić z poziomu terminala:

- minecraft -m human – uruchamia grę w trybie ręcznym, gdzie użytkownik steruje Steve'em.
- minecraft -m random – uruchamia grę w trybie, gdzie ruchy Steve'a są generowane losowo przez algorytm.

Te opcje pozwalają na ocenę i dostosowanie mechaniki gry przed wdrożeniem zaawansowanych metod sterowania.

## Struktura i działanie środowiska

Środowisko zostało zaimplementowane na wzór repozytorium [https://github.com/Talendar/flappy-bird-gym](https://github.com/Talendar/flappy-bird-gym), z użyciem pliku `minecraft/envs/minecraft_env.py`. Środowisko to jest typu dyskretnego i oferuje trzy możliwe akcje, które Steve może wykonać, zdefiniowane w klasie `Actions`:
- pozostanie w miejscu,
- ruch w lewo,
- ruch w prawo.

Zadaniem Steve'a jest unikanie kontaktu z spadającymi creeperami. Za każdego unikniętego creepera gracz zdobywa punkty. Kontakt z creeperem oznacza utratę punktów. Rozgrywka kończy się, gdy Steve nie uniknie określonej liczby creeperów lub po wykonaniu określonej liczby ruchów, co pozwala na przeprowadzenie wielu krótkich sesji testowych.

## Program rozwiązujący problem w utworzonym środowisku

Nasz agent, działający w środowisku gry jest wyposażony w system decyzyjny, który zapewnia optymalną strategię unikania nadchodzących przeciwników. Wykorzystując algorytmy przetwarzania obserwacji, agent dynamicznie analizuje zmieniające się warunki na planszy i podejmuje decyzje, które maksymalizują jego wynik.