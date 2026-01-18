# projekt2_informatyka_2025_26
Taras Heraimovych, s206481, ARiSS sem.3 gr.2a
2 etap zaliczenia przedmiotu (Python)
V1: stworzenie szkieletu ukladu, wstepnie brak jakichkolwiek funkcji
V2: optymalizacja wizualizacji, dodanie nowych elementow drugorzednych dla przyszlych funkcji
V3: wprowadzenie pierwszych funkcji: dzialajacy piec, dodana mechanika zmiany poziomu plynu w 1 pojemniku + mechanika wyparowywania cieczy
V4: dodano prymitywna mechanike filtra z opcja jego wymiany podczas zatkania
V5: interfejs uzytkownika zostal optymalizowany, przyciski sa opisane dokladniej, dodana mechanika przegrzania chlodnicy i wymiana wody (P.S. Podczas zatkania/przegrzania proces destylacji sie hamuje). Z para wystapil bug, z powodu ktorego sie nie wyswietla.
V6: dodana animacja wymiany filtra oraz wody w chlodnicy. Problem z animacja pary rozwiazac sie nie udalo
Glowne mechaniki sterowania ukladem:
    - zero-jedynkowe sterowanie ciecza robocza w pojemniku T1 (posrednie wartosci nie maja sensu w tym ukladzie)
    - Wlaczenie/wylaczenie pieca oraz regulacja jego temperatury, od ktorej zalezy intensywnosc parowania
    - wymiana filtra oraz chlodnicy