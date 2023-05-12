# bachelor

Bachelorprojekt 2023 - Algorithmic collusion

Link til overleaf: 

https://www.overleaf.com/read/cbmqdzydzpfd

Link til bachelor møde - noter mm.:

https://docs.google.com/document/d/1hbMO4Pj0ytmTZ8uR4CliwYQ-r6hG3K3lX3s7iI5WB74/edit

## Status og spørgsmål:
### Grim Trigger graf
Det ses at Q-learneren hurtigt falder i hvor god den er til at spille en kooperativ mængde (kooperativ pris)
### Discount rate
Vi kan ikke finde nogen måde at udregne den optimale discount rate for flere spillere. Skal vi bare simulere en masse spil med forskellige discount rates og tage den discount rate som giver bedste complicity/profitability?
### Flere priser graf
Når vi har flere priser i spil ses det hvordan Q_learneren hurtigt stopper med at spille kooperative mængder (kooperativ priser) når der kommer for mange priser. Skal dette resultat med i opgaven evt. 
### Fordelingen af complicity i historgram graf
Fordelingen af complicity ser stadig ret sjov ud, hvad kan mon dette betyder?
### Hvor stort et problem er numba fejlen
### Q-learner learning module og forventningen til modstanderens pris
Jeg er usikker på om Q-funktionens learning module er implementeret korrekt. Lige nu "gætter" firm 0 på modstanderens pris ved at kalde set_price() og vice versa. Der står dog i Klein (2021), at den value-function condition (4), der skal holde for at være på ligevægtsstien, er parallel med Q-learning-algoritmens learning module (5). Under value-function condition (4), tager vi ikke modstanderens pris, $p_{j,t+1}$, direkte, men vi tager forventingen til den baseret på fordelingen af modstanderens reaktionsfunktion, $R_j(p)$. Dvs. vi tager $E_{p_{j,t+1}}$. Det vigtige her er, at vi ikke bare må gætte tilfældigt på en pris, men er nødt til at beregne en forventingsværdi på baggrund af en statistisk fordeling af en bestemt funktion $R_j(p)$, som jeg tror på en eller anden måde baserer sig på $Q_j(p)$. Jeg har derfor et par spørgsmål:

1. Hvordan skal ligheden mellem value-function condition (4) og det rekursive Q-learning forhold (5) forstås? Er andet led i sidste ligning i (5), $\delta \pi (p_{it}, s_{t+1})$ nødt til at tage forventingen, $E_{p_{j,t+1}}$, som argument, dvs. $s_{t+1}=E_{p_{j,t+1}}$?

2. Såfremt dette er tilfældet, hvordan kan vi approksimere denne forventningsværdi? Tager vi gennemsnittet af prishistorikken? Der står eksplicit i Klein(2021) (side 553), at algoritmen under Markov-antagelsen ikke må betinge vores priser på historikken af tidligere priser, der ikke længere er relevante for den nuværende profit. 

3. Hvad er fordelingen af reaktionsfunktionen $R_j(p)$? Kender vi den overhovedet?

4. I det generelle case hvor Q-learneren skal spille mod en vilkårlig agent (f.eks. en undercutter eller triggerstrategi), hvad skal Q-learneren så trække  sin næste state $s_{t+1}$ fra? Vi kan nok ikke bare indføre modstanderens strategi i Q-learnerens "gæt" direkte, da vi så ville afsløre strategien, og Q-learneren ikke selv lærer sin modstanders strategi. 

### Undercutter
Klein (2021) siger også i afsnittet om teoretiske begrænsninger (side 546), at Q-learnere er garanterede til at konvergere mod optimale strategier, hvis modstanderen spiller en fixed strategi, f.eks. undercutting. Hvis ikke vi får samme resultat, kan det være, vi har gjort noget galt. Vores Q-learner får totalt bank af undercutteren, hvilket er lidt pudsigt. 

### Optimalitet
Vi mangler at indføre målet for optimalitet, $\Gamma_i$. Dette er ret vigtigt, da det kan hjælpe os med at afgøre, om udfaldet er en Nash-ligevægt eller ej. Klein(2021) fandt, at $\Gamma_i \approx 1$. Det er ret vigtigt at kunne replikere dette resultat. At beregne optimaliteten kræver dog, at vi finder $max_p Q_{i}^{\*}(p, p_j)$, men algoritmen observerer ikke $Q_{i}^{\*}$. Den skal beregnes ved at loope over alle action-state par indtil ligning (5) konvergerer, men jeg er lidt i tvivl om, hvordan dette skal gøres. Hvordan ved vi, at (5) er konvergeret? Vi kan evt. sige at hvis differenserne er små nok, er den konvergeret. 

### Forced deviation
Calvano et. al. (2019) siger at en af de vigtigste måder at påvise collusion, er ved at se på hvad der sker i et scenarie af forced deviation. Hvis Q-learnerne "straffer" hinanden med priskrig efter et tvunget prisfald, for så derefter at arbejde sig op igen til samarbejde, har vi påvist, at de spiller en collusive strategi. Er denne centrale pointe fra Calvano et. al. (2019) vigtig nok til at vi også bør replikere den i vores opgave, for at være sikker på at Q-learnerne viser collusion?

## TO DO 11/5 (not in priority):
1. Beregn Q-så man ved om learneren, plot differensen mellem Q matricen for periode k og k+1 osv. og plot denne forskel, for at sikre at vi er konvergeret. MødeOptagelse: [00:18:21-12/5]
2. Vi skal afgøre hvilke af simulationerne der ender i fixed prices, og pris cyklus vha. variansplot over priser 2,3 spillere. Hvis der er n-point problems da overvej robuste varianser. MødeOptagelse: [01:07:21-12/5]
3. Find find den pris som er nashligevægten da det er den troværdige og hårde pris [09:07:21-12/5]
4. Find det competitive benchmark for 3 spillere, kig på priscyklus, skriv overvejeler ned ift. ikke at løse analystisk da det ikke er tættere på virkeligheden, forklar mere i dybden omkring priscyklerne. CA. - [21:07:21-12/5]
5. Hvis at der er forced deviation.

## TO DO 11/5 (not in priority):
1. Lav grim trigger om så den trækker rigtigt og lagre informationen i en matrice som Anders forklarede det. 
2. Kog numba problemet ned til Anders og send.
3. Repliker flere priser grafen hvor vi har profitability istedet for intances of collusion på y aksen. 
4. Skriv videre på opgaven
5. tjek 3 player implementering igennem og se om den er korrekt
6. Lav plot der viser profitability fra 0-100% for 2 og 3 player for bestemt prisgrid, se video hvor Anders tegner for at se hvordan plot skal se ud 
7. Opdater opgavestruktur nederest

## Questions Meeting 11/5
1. Competitive benchmark 3 players 

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
1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .20%/1.5side <br />
2 Theory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .85%/0.25side <br />
2.1 Dynamic competition . . . . . . . . . . . . . . . . . . . . . . . . . . 40%/0.5side <br />
2.1.1 Sequential games . . . . . . . . . . . . . . . . . . . . . . . . . . .40%/1side <br />
2.1.1.1 Perioder. . . . . . . . . . . . . . . . . . . . . . . . . ... . . . 0%/0.25side <br />
2.1.1.2 Timing. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 0%/0.25side <br />
2.1.2 Bertrand two and n players . . . . . . . . . . . . . . . . ... . . .. 30%/1side <br />
2.1.2.1 Bertrand spilteori. . . . . . . . . . . . . . . . . . . . ... . . .. 0%/1side <br />
2.1.2.2 Løsning af spillet, vis nashligevægte . . . . . . . . . . ... . . .. 0%/1side <br />
2.1.2.3 Forklar hvordan spillet ændrer sig når der er flere spillere med. .. 0%/1side <br />
2.1.2.4 Diskuter realisme ift. sequentielitet. . . . . . . .. . . . . . . .. 0%/1side <br />
2.1.2.5 Monopolpris . . . . . . . . . . . . . . . . . . . . . . . ... . . .. 100%/1side <br />
2.1.3 Collusion . . . . . . . . . . . . . . . . .. . . . . . . . . . . . . . 0%/2sider <br />
2.1.3.1 Vis tacit collusion . . . .  . . . . . . . . . . . . . . . . . . . . 0%/2sider <br />
2.1.3.2 lav analyse af Bertrand spillet med collusion. . . . . . . . . . . . 0%/2sider <br />
2.1.3.2 Vis Nash-ligevægte og forklar collusion ud fra disse.. . . . . . . . 0%/2sider <br />
2.2 Reinforcement learning .. .. . . . . . . . . . . . . . . . . . . . . ...0%/0.25side <br />
2.2.1 Value-function condition problem . . . .. . . . . . . .. . . . . . ..  80%/0.5sider <br />
2.2.2 Q-learning introduction . . . . . . . . . . . . . . .. . . . . . . .. . . . . . ..  80%/0.5sider <br />
2.2.2.1 Parameters . . . . . . . . . . . . . . . . . .  . .. . . . . . ..  0%/0.5sider <br />
2.2.2.1.1 Delta . . . . . . . . . . . . . . . . . .  . .. . . . . . ..  0%/0.5sider <br />
2.2.2.1.2 Alpha . . . . . . . . . . . . . . . . . .  . .. . . . . . ..  0%/0.5sider <br />
2.2.2.1.3 Theta . . . . . . . . . . . . . . . . . .  . .. . . . . . ..  0%/0.5sider <br />
2.2.2.1.4 Epsilon . . . . . . . . . . . . . . . . . .  . .. . . . . . ..  0%/0.5sider <br />
2.2.2.2 Learning module . . . . . . . . . . . . . . . . . .  . .. . . . . . ..  80%/1sider <br />
2.2.2.3 Action module . . . . . . . . . . . . . . . . . .  . .. . . . . . ..  80%/1sider <br />
2.2.3 Q-learning with more players . . . . . . . . . . . . . . . . . . . ...20%/1side <br />
2.2.3.1 Dimensionality concerns . . . . . . . . . . . . . . . . . . . ...20%/1side <br />
2.2.3.2 hvordan Q-learning learning module ændrer sig. . . . . . . . . . ...20%/1side <br />
2.2.4 Q-learning pricing algorithm Setup . . . . . . . . . . . .... . . . . 0%/1side <br />
2.2.4.1 Vis hele algoritmen som pseudokode for 2 og 3 spillere . ... . . . . 0%/1side <br />
2.3 Trigger . . . . . . . . . . . . . . . . . . . . .  . .. . . . . . ..  65%/0.5sider <br />
2.3.1 Introduction to trigger strategies. . . . . . . .  . .. . . . . . ..  65%/0.5sider <br />
2.3.2 why we use it . . . . . . . . . . . . . . . . . .  . .. . . . . . ..  0%/0.5sider <br />
2.3.3 math behind f table and pseodocode. . . . . .  . .. . . . . . ..  0%/0.5sider <br />
2.4 Performance metrics . . . . . . . ... . . . . . . . . . . . . .... . .….0%/0.25side <br />
2.4.1 Complicity . . . . . . . . . . . . . . . . . . . . . . . . . . . .……..15%/1side <br />
2.4.2 Profitability . . . . . . . . . . . . . . . . . . . . . .. . . . . ………15%/1side <br />
3 Implementation and Optimization . . . . . . . ……. . . . . . .. .. .  .……….0%/0.5side <br />
3.1 Optimization. . . . . . . ……. . . . . . . . . . . . . . . . . .. . . ...0%/0.5side <br />
3.1.1 Numba speedup . . . . . . . . . . . . . . . . . . . . . . . . . . …...0%/1side <br />
3.2 Implementation python . . . . . . . ……. . . . . . . . . . . . . . . . . 0%/1side <br />
3.3 Implementation python . . . . . . . ……. . . . . . . . . . . . . . . . . 0%/1side <br />
4 Results . . . . . . . ……. . . . . . . . . . . . . . . . . . . . . . . ……….0%/0.5side <br />
4.1 Performance . . . . . . . . . . .. . . . . . . ... . .. . .. . . . .……..30%/0.25side <br />
4.1.1 Plot of complicity og profitability over time, 2 and 3 players. . .……..30%/0.25side <br />
4.2 Price varians . . . . . . . . .. . . . . . . . . . . . . . . . . . . . ….0%/1side <br />
4.2.1 Fortolk på variansen ændre det sig fra 2 til 3 spillere . . . . ….0%/1side <br />
4.3 Trigger . . . . . . . . .. . . . . . . . . . . . . . . . . . . . ….0%/1side <br />
4.3.1 Udpensle . . . . . . . . .. . . . . . . . . . . . . . . . . . . . ….0%/1side <br />
4.2.1 Forgiving Grim trigger vs 2 player plot . . . . . . . . . . . . . .  .75%/0side <br />
5 Discussion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . …0%/1side <br />
6 Conclusion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .……..0%/1side <br />
7 Bibliography <br />
I alt 25 sider.
