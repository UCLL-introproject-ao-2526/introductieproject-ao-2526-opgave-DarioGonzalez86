## 28 maart 2026

Vandaag de eerste stappen gezet in het project. Mogelijks nog te vroeg omdat ik nog niet superveel challenges heb gedaan. Maar ik wou toch eens komen kijken wat ik precies moest doen, wat de eerste stappen zijn. Aangezien we ons nu bevinden in de examenperiode van maart en er andere examens op de planning staan, is dit eerder uit verkennend standpunt en wat afwisseling te hebben tussen het studeren.

De video werd volledig bekeken en ondertussen heb ik ook de code aangemaakt in het bestand blackjack.py
Zowel de code van blackjack als het logboek werden vandaag voor de eerste keer gecommit.


## 30 maart 2026

Deze dag heb ik kort nagedacht over de mogelijke aanpassingen. In de tutorial op youtube was er sprake van een soft 17 voor de dealer. Zelf heb ik geen uitgebreide ervaring met blackjack, dus dit zal ik moeten opzoekene wat dit betekent en dan proberen te implementeren.

Andere mogelijke aanpassingen die in mij opkwamen:
- Afbeelding van de kaarten tonen (harten, klaveren, ...). Dit ben ik tegengekomen in 1 van de challenges rond representing data (unicode). Dus ook dit moet ik even verder bekijken hoe te implementeren.
- Achtergrondmuziek toevoegen (met aan/uitknop)
- Een beginscherm toevoegen met het idee om hier een scorebord te kunnen raadplegen (all time scorebord), een naam te kiezen, nieuwe speler aan te maken, ...

Het laatste idee is een idee dat ik gekregen heb nadat ik eens door de cursus van programming 1 en 2 ben gegaan om te zien wat we geleerd hebben. Zo kunnen we bijvoorbeeld werken met een Class voor de spelers, werken met een bestand waar we de geregistreerde spelers aanmaken met een default socre (0-0-0) en dit bestand updaten na elke spel. De Class kan werken met controles, bijvoorbeeld als de naam die ingegeven werd reeds bestaat.

Ik ben begonnen met het toevoegen van de class Player in een apart bestand players.py en het tekstbestand players_history.txt om de scores en spelers te bewaren. 

## 6 april 2026

Na wat proberen met de class player en het bestand, heb ik dit idee even on hold gezet. Ik moet wat verder nadenken over de flow van het programma, want er gaat wat moeten wijzigen om dit nieuw startscherm te tonen. Dit pik ik mogelijks later terug op. 

Ik ben overgeschakeld naar het toevoegen van de kleur (suits) voor de kaarten. De decks werden nu opgebouwd door enkel het cijfertje. Een deck was dan 4 keer het aantal kaarten. Deze logica is nu lichtjes anders natuurlijk. Een deck nu is een combinatie van de kaarten en de 4 kleuren.

De aanpassingen hiervoor moesten gebeuren in het trekken van de kaarten (functie draw_cards) en ook in de berekening van de score (calculate score). De draw_cards voegen we de kleur + waarde toe als nieuwe constante (omdat een kaart nu uit 2 karaters bestaat). Ook voor het tellen moeten we natuurlijk de kleur weghalen om te kunnen tellen. 

Na de eerste test gaf dit een vierkant als afbeelding. Dus de symbolen werden niet herkend. Via google heb ik een nieuw lettertype gevonden dat dit wel ondersteund. Door het veranderen van het lettertype waren de getallen iets te groot naar mijn mening. Deze heb ik dan ook vervanngen door de kleinere variant van het lettertype.

De kaarten zelf waren nu rood en blauw, ik heb dit ook veranderd als de kleur zwart is, dat de kaart zelf zwart werd, en ook voor rood. Dit kwam niet zo mooi uit omwille van de zwarte achtergrond, dus heb ik dit even grijs gemaakt. Dit moet ik later nog herbekijken.


## 10 april 2026

Na een aantal spelletjes om te kijken of de kleuren en kaarten goed zitten, zag ik dat bij mijn eigen hand met A, 6 en A een score werd gegeven van 28. Dit is niet correct, dus er zit ergens een bug in het programma. Omdat de fout hoogstwaarschijnlijk in de functie calculate_score() zit, heb ik deze in een apart bestand gezet (calculate_score.py) zodat ik zelf een hand kon meegeven om te kijken wat er precies gebeurde. 

Bij de eerste test met een hand met 1x A en een 9, gaf de printstatement van het count_aces 0 aan. Hoe het aantal aces geteld wordt zat dus fout en eigenlijk is dat ook logisch. Door de kleuren toe te voegen, bestaat de "hand" niet enkel meer uit A, 1, 2, enz. maar ook de icoontjes zelf. Deze moeten we dus eruit zien te halen. Met de aanpassing lijkt het nu wel te werken. 

Omdat dit moeilijk te na te bootsen valt, heb ik een aantal tests geschreven om te zien of het resultaat van calculat_score is wat ik verwacht. En de 7 testen slagen. Dus dat is goed. Ik heb zowel het aparte bestand met de functie als de testen in een map "oude bestanden" gezet om de rootdirectory niet te vervuilen met allerlei bestanden. 


## 11 april 2026

Vandaag ben ik opnieuw gestart met het nieuwe startscherm. Ik heb via CoPilot een afbeelding met blackjack laten genereren om als achtergrond te gebruiken. Op het startscherm krijg je 2 knoppen te zien: "nieuwe speler" en "bestaande speler". De bedoeling is dat wanneer je kiest voor "nieuwe speler" er in het CSV bestand gekeken wordt of de speler al bestaat. Zo ja, krijg je een foutmelding. Zo nee, wordt de speler aangemaakt met 0-0-0 scores. Dit is ondertussen in orde. De bedoeling is dat we de naam en scores meenemen naar het spel zelf, maar dat is voor later. 

Bij het het klikken op "bestaande speler" moet je uw naam invullen, we gaan dan kijken of de speler bestaat, halen zijn spelhistoriek op, en starten het spel. Hier ben ik nog niet meer begonnen. Dit is dus ook voor later. 

Het gebruik van de CSV leek me makkelijker dan te werken met Classes, dus de code rond de class player heb ik in principe niet meer nodig. Later te bekijken of ik dit ook in de map "oude bestanden" zet. Ook de CSV staat nu nog in de hoofddirectory, mogelijks ga ik deze verplaatsen naar de recent aangemaakte map "assets" waar ik alles zet van afbeeldingen, letterypes, ...


## 13 april 2026

Ik heb eerst wat verder gewerkt aan het scherm voor een nieuwe speler toe te voegen (inputvelden wat verschoven, zelde achtergrond als het startscherm, ...). De volgende stap was deze hele flow afwerken. Dus starten met een nieuwe speler aan te maken, paar spelletjes spelen, zorgen dat de score opgeslaan wordt in het CSV bestand. Dit loopt nu allemaal goed. De CSV wordt aangepast zodra een spel voorbij is met de correcte score. 

Ik heb ook een paar klene aanpassigen gedaan m.b.t. de layout (spelernaam ipv player, even groot speelscherm voor startscherm als blackjack scherm, zelfde knoppen in het blackjack spel zelf, ...). Na de aanpassing gezien dat er nog wat aanpassingen moesten gebeuren. Deze zijn voor een andere dag. Ik weet ook niet of ik de achtergrond hetzelfde ga houden:


![afbeelding](Assets\Images\Aanpassen_achtergrond.jpg)


## 14 april 2026

De knoppen en layout van het speelscherm allemaal aangepast. In principe ben ik klaar met wat ik wou doen voor het starten van een nieuwe speler. De volgende stap gaat zijn de flow voor een bestaande speler voorzien. Ik heb ook nog veel comment in mijn huidige code staan van oude programmatie die ik voorlopig heb laten staan, deze wil ik ook nog opkuisen. En ik zag dat ik ook veel dingen dubbel (of meer) heb staan, dit kan waarschijnlijk ook beter door dit in een aparte functie te zetten en dan de functie aan te roepen. 

Telkens ik een test deed en het venster sloot, kreeg ik de foutmelding "pygame.error: display Surface quit". In de documentatie en op Google zitten zoeken naar de reden, en blijkbaar werd de loop nog verder uitgevoerd en werd er een poging gedaan om te tekenen op een gesloten venster, vandaar de fout met blit(). Dit heb ik ook aangepast met overal waar event QUIT stond, pygame.quit() en sys.exit() toe te voegen. 


## 15 april 2026

De flow voor "bestaande speler" moet zijn:
- Druk op de knop bestaande speler
- Vul naam in
- Controleer of speler bestaat:
    - Zo nee, geef een melding dat speler nog niet bestaat
    - Zo ja, haal gegevens op van de csv
- Start spel

De functie om te kijken of een speler bestaat is er al, enkel wat de functie terug geeft, moet hier anders geïnterpreteerd worden. Ook om het spel te starten, bestaat reeds. Dus enige wat we extra moeten voorzien is het nieuw scherm met inputveld. Een extra optie (later te bekijken) is voor de unhappy flow (speler bestaat nog niet) daar een extra actie te voorzien om een speler aan te maken of terug te kregen naar hoofdscherm. 

Ik merk dat er veel gelijkenissen zijn tussen de 2 functies, later te bekijken of dit eventueel in 1 functie kan, maar met ander input parameters. 


## 15 april (bis)

Het bestand start_screen heb ik volledig aangepakt. Bij het testen zag ik wel dat wanneer ik in het proces van een bestaande speler een naam in kleine letters geef (bijvoorbeeld tom) en de naam staat in het CSV bestand met Tom, dit door de validaties raakt (terecht, want ik gebruik lower). Maar de naam die je ingeeft, wordt ook doorgegeven aan blackjack.py, waardoor de score niet goed opgehaald wordt (omdat er geen tom maar Tom in de CSV staat). Dit moet ik eens zien hoe ik dit kan oplossen.


## 20 april

De easy way zou zijn dat ik de controle van lower() weg laat natuurlijk, en de controle case-sensitive maak. Maar dan heb je zowel "Tom" als "tom" als mogelijke spelers. Een andere oplossing zou zijn dat ik de naam van de csv doorgeef als naam in plaats van de naam van het inputveld. Een 3de oplossing is gebruik maken van mijn class Player. Dit was het eerste wat ik gemaakt had, maar een beetje genegeerd heb achteraf. Dus ik ben voor deze oplossing gegaan.Ik heb de klasse wel lichtjes moeten aanpassen zodat ik de code minimaal moest aanpassen. 

Verder heb ik ook alles in het Engels gezet deze keer. De code van de tutorial, daar waren de comments en functies in het Engels, in mijn player class bestand in het Nederlands. 





