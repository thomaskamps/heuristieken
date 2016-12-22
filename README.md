# Rush Hour
Minor Programmeren 16/17

Vak: Heuristieken

Studenten: Martijn de Jong (10774807), Thomas Kamps (10758151), Rick Vergunst (10793925)

---

###Beschrijving:
In deze repository kan je de uitwerking van de Rush Hour case vinden voor het vak Heuristieken aan de Universiteit van Amsterdam.

---

###Opdrachten:
1. Los op games 1,2 en 3 op. Doe hoe je dat goed lijkt. Het is natuurlijk goed om daar een programma te schrijven, maar als je een ander idee hebt, of het met de hand kunt, mag dat ook.

2. Verzin een implementatie voor het bord, en schrijf een algoritme dat series van zetten uitvoert. Laat het algoritme games 4, 5 en 6 oplossen. Kortere series zijn betere series.

3. Los game 7 op. Pas je algoritme aan indien dat nodig is.

4. [Advanced] Probeer te achterhalen wat het verschil is tussen een moeilijke rushhour-opgave en een evengrote makkelijk rushhour opgave. Ook aantonen waar de moeilijkheid niet aan ligt is waardevol.

Volledige beschrijving van de opdracht:
http://heuristieken.nl/wiki/index.php?title=Rush_Hour

---

###Installatie

Voor het uitvoeren van alles in deze repository zijn de volgende installaties vereist:  
1 - Python 2.7  
2 - PyGame  

---

###Algoritmen uitvoeren  
####Argumenten  
#####Verplicht  
--config (nummer) : Geeft de mogelijkheid om een bord uit te kiezen met als opties 1 tot en met 7 (vb. --config 3)  
--algo (algoritme) : Keuze van het algoritme, opties zijn a_star, best_first, beam, bfs, dfs, hybrid_beam (vb. --algo bfs)    
#####Verplicht voor a_star  
--heur (nummers) : Bepaald welke heuristieken worden toegepast voor a_star, keuze uit 1 tot en met 4, meerdere heuristieken worden gescheiden met komma en zonder spaties (vb. --heur 1,3)    
#####Optioneel
--print : print het gevonden aantal oplossing uit  
--vis/--visual : Genereert een visualisatie die de gevonden oplossing laat zien. (Meer opties via de GUI, zie onderaan)

---

###Voorbeelden algoritmen  
#####A Star  
python rushHourSolver.py --algo a_star --config 3 --heur 1,2,4  
#####Best First  
python rushHourSolver.py --algo best_first --config 1  
#####BFS
python rushHourSolver.py --algo bfs --config 4 --vis
#####Beam
python rushHourSolver.py --algo beam --config 1 --print  
#####DFS  
python rushHourSolver.py --algo dfs --config 2  
#####Hybrid Beam  
python rushHourSolver.py --algo hybrid_beam --config 6 --print

---

###GUI aanroepen
python gui.py
