# bachelor

Bachelorprojekt 2023 - Algorithmic collusion

Link til overleaf: 

https://www.overleaf.com/read/cbmqdzydzpfd

Link til bachelor møde - noter mm.:

https://docs.google.com/document/d/1hbMO4Pj0ytmTZ8uR4CliwYQ-r6hG3K3lX3s7iI5WB74/edit

## TO DO (in priority):
0. DONE Ret 2 spiller implementationen sådan at q-funktionen trækker en pris for modstanderen ligesom vi gør i 3 spiller implementationen

1. Udbyg opgavestrukturen med f.eks. grafer, 2 og 3 spillere implementation,      complicity, anualiseret rate og begynd at skrive på opgaven. De to nedenstående grafer skal laves:
  1.1. Lav visualiersinger af graden af stationaritet, vha. varians fordeling

  1.2. Lav en graf hvor x-aksen er er antallet af priser (undersøg om finheden af prisgrid ændrer resultater) og y aksen er hvor meget de colluder

2. Udbyg de resultat plots der er lavet med sandynlighed skriv runs istedet frequency, skriv at delta beregnes som per run og at det viser fordelingen. 

3. Find ud af at lave en anualiseret discountrate da det ikke er "fair" at anvende 0.95 når der kommer flere spillere

4. Implementer undercutter (sanity check)

5. Implementer grim trigger (n periode) og



Contents
0 Abstract….. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 0%/0.5side <br />
1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .0%/1.5side <br />
2 Theory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .0%/0.5side <br />
2.1 Dynamic competition . . . . . . . . . . . . . . . . . . . . . . . . . . 0%/0.5side <br />
2.1.1 Sequential games . . . . . . . . . . . . . . . . . . . . . . . . . . .0%/1side <br />
2.1.1.1 Perioder. . . . . . . . . . . . . . . . . . . . . . . . . ... . . . <br /> 
2.1.1.2 Timing. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . <br />
2.1.2 Bertrand two and n players . . . . . . . . . . . . . . . . ... . . .. 0%/1side <br />
2.1.3 Collusion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 0%/2sider <br />
2.2 Q-learning . . . . . . . ……. . . . . . . . . . . . . . . . . . . . . ...0%/0.5side <br />
2.2.1 Reinforcement learning and Q-learning introduction . .. . . . . . ..  80%/3sider <br />
2.2.2 Q-learning with more players . . . . . . . . . . . . . . . . . . . ...0%/1side <br />
2.2.3 Q-learning pricing algorithm Setup . . . . . . . . . . . . . . . . 0%/1side <br />
3 Results . . . . . . . ……. . . . . . . . . . . . . . . . . . . . . . . . ……….0%/0.5side <br />
3.1 Performance metrics . . . . . . . ……. . . . . . . . . . . . . . . .….0%/0.5side <br />
3.1.1 Complicity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .……..0%/1side <br />
3.1.2 Profitability . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ………0%/1side <br />
3.2 Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . …..0%/2sider <br />
3.3 Grim trigger . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ….0%/1side <br />
4 Implementation and Optimization . . . . . . . ……. . . . . . .. .. . . . . .……….0%/0.5side <br />
4.1 Optimization. . . . . . . ……. . . . . . . . . . . . . . . . . . . . . . . ...0%/0.5side <br />
4.1.1 Numba speedup . . . . . . . . . . . . . . . . . . . . . . . . . . . …...0%/1side <br />
4.1.1.1 Scaling of running time and parrelization…………….. <br />
4.1.2 Using C . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ……….0%/1side <br />
4.2 Implementation . . . . . . . ……. . . . . . . . . . . . . . . . . . . .….0%/0.5side <br />
4.2.1 Object oriented approach . . . . . . . . . . . . . . . . . . . . . . ..0%/1side <br />
5 Discussion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ………...0%/1side <br />
6 Conclusion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ………..0%/1side <br />
7 Bibliography <br />
I alt 25 sider.
