# bachelor

Bachelorprojekt 2023 - Algorithmic collusion

Link til overleaf: 

https://www.overleaf.com/read/cbmqdzydzpfd

Link til bachelor møde - noter mm.:

https://docs.google.com/document/d/1hbMO4Pj0ytmTZ8uR4CliwYQ-r6hG3K3lX3s7iI5WB74/edit

## Status og spørgsmål:
### Q-learner learning module og forventningen til modstanderens pris
Jeg er usikker på om Q-funktionens learning module er implementeret korrekt. Lige nu "gætter" firm 0 på modstanderens pris ved at kalde set_price() og vice versa. Der står dog i Klein (2021), at den value-function condition (4), der skal holde for at være på ligevægtsstien, er parallel med Q-learning-algoritmens learning module (5). Under value-function condition (4), tager vi ikke modstanderens pris, $p_{j,t+1}$, direkte, men vi tager forventingen til den baseret på fordelingen af modstanderens reaktionsfunktion, $R_j(p)$. Dvs. vi tager $E_{p_{j,t+1}}$. Det vigtige her er, at vi ikke bare må gætte tilfældigt på en pris, men er nødt til at beregne en forventingsværdi på baggrund af en statistisk fordeling af en bestemt funktion $R_j(p)$, som jeg tror på en eller anden måde baserer sig på $Q_j(p)$. Jeg har derfor et par spørgsmål:

1. Hvordan skal ligheden mellem value-function condition (4) og det rekursive Q-learning forhold (5) forstås? Er andet led i sidste ligning i (5), $\delta \pi (p_{it}, s_{t+1})$ nødt til at tage forventingen, $E_{p_{j,t+1}}$, som argument, dvs. $s_{t+1}=E_{p_{j,t+1}}$?

2. Såfremt dette er tilfældet, hvordan kan vi approksimere denne forventningsværdi? Tager vi gennemsnittet af prishistorikken? Der står eksplicit i Klein(2021) (side 553), at algoritmen under Markov-antagelsen ikke må betinge vores priser på historikken af tidligere priser, der ikke længere er relevante for den nuværende profit. 

3. Hvad er fordelingen af reaktionsfunktionen $R_j(p)$? Kender vi den overhovedet?

### Undercutter
Klein (2021) siger også i afsnittet om teoretiske begrænsninger (side 546), at Q-learnere er garanterede til at konvergere mod optimale strategier, hvis modstanderen spiller en fixed strategi, f.eks. undercutting. Hvis ikke vi får samme resultat, kan det være, vi har gjort noget galt. Vores Q-learner får totalt bank af undercutteren, hvilket er lidt pudsigt.

### Optimalitet
Vi mangler at indføre målet for optimalitet, $\Gamma_i$. Dette er ret vigtigt, da det kan hjælpe os med at afgøre, om udfaldet er en Nash-ligevægt eller ej. Klein(2021) fandt, at $\Gamma_i \approx 1$. Det er ret vigtigt at kunne replikere dette resultat. At beregne optimaliteten kræver dog, at vi finder $max_p Q_{i}^{\*}(p, p_j)$, men algoritmen observerer ikke $Q_{i}^{\*}$. Den skal beregnes ved at loope over alle action-state par indtil ligning (5) konvergerer, men jeg er lidt i tvivl om, hvordan dette skal gøres. Hvordan ved vi, at (5) er konvergeret? Vi kan evt. sige at hvis differenserne er små nok, er den konvergeret. 

## TO DO (in priority):
0. DONE Ret 2 spiller implementationen sådan at q-funktionen trækker en pris for modstanderen ligesom vi gør i 3 spiller implementationen

1. Udbyg opgavestrukturen med f.eks. grafer, 2 og 3 spillere implementation,      complicity, annualiseret discountrate: Find den optimale discountrate $\delta$. Og begynd at skrive på opgaven. De to nedenstående grafer skal laves:
  1.1. Lav visualiersinger af graden af stationaritet, vha. varians fordeling

  1.2. Lav en graf hvor x-aksen er er antallet af priser (undersøg om finheden af prisgrid ændrer resultater) og y aksen er hvor meget de colluder

2. Udbyg de resultat plots der er lavet med sandynlighed skriv runs istedet frequency, skriv at delta beregnes som per run og at det viser fordelingen. 

3. Find ud af at lave en anualiseret discountrate da det ikke er "fair" at anvende 0.95 når der kommer flere spillere

4. Implementer undercutter (sanity check)

5. Implementer grim trigger (n periode) og



Contents <br />
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
