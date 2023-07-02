User manual CTF
För att starta spelet behöver man befinna sig i rätt working directory. Detta rätta working directory bör innehålla alla filer som tillhör spelet. Sedan för att köra spelet bör filen ctf.py köras för att få igång spelet. När spelet körs kommer man först till en meny där man kan välja vilken karta som spelet ska köras på. Start startar spelet och det finns en möjlighet att modifiera spelet genom att att välja i menyn och sedan trycka enter. 

I själva koden finns det möjlighet att välja följande alternativ för att modifiera spelet.

fog of war som begränsar synen
unfair_AI som förbättrar ai förmåga att spela
win_cone_time som ställer in spelet på tid,  win_con_total_rounds som stoppar spelet när en spelare har fått ett visst antal poäng
hotseatmultiplayer som gör det möjligt att spela två
Text som visar resultatet och hur många flaggor som varje pansarvagn har hämtat hem.
ljud som spelas i flera olika situationer
hitpoints 
menu där det går att välja karta och inställningar,

Dessa kan aktiveras genom att sättas till True i koden.



ctf-filen
Filen används för att köra det huvudprogrammet och för att få pygame att visas när man kör. I filen finns också en del olika funktioner som har direkt påverkan på spelet. Där finns också funktioner som skapar exempelvis lådor. De flesta av våra features finns också  i ctf,  Här ligger också main loopen som kör hela programmet och exempelvis collision handler som styr lite fysiken i spelet.
ai-filen 
Används för att botarna i spelet ska kunna fungera själv och ta egna beslut för att vinna spelet. Exempelvis används breadth first search algoritmen för att hitta lämpliga rutor att gå till. Samt funktioner som maybe shoot klargör om det går att skjuta ett visst objekt. Dessa algoritmer och funktioner som  används sedan i ctf filen där main loopen. 

Gameobjects 
här finns klasserna som gör att det går att modifiera pansarvagnarna och ge dem förmågor som sedan appliceras i ctf. Inne i dessa klasser finns också funktioner som exempelvis shoot, som direkt används av både spelare och ai. Sedan finns det också funktioner som tillför till spelupplevelsen och hur spelet körs. Exempelvis används update funktionen för en mängd olika saker.

Settings
Innehåller alla settings som att byta wincon spela med fog of war osv... Det är från den är modulen som spelet skapar olika saker baserad på vad man väljer. Här kan man byta win cons, fog of war och alla andra inställningar som ändrar hur spelet skapas. 

menu
Här skapas menun för spelet och där man kan ändra vissa settings på spelet. Till exempel här skapas menu klassen som skapar en menu där vi kan ändra på vilken map och om hot_seat_multipler är på eller inte. Desutom har vi en map preview som visar vilken map som är på för tillfället.

Images
Innehåller en funktion som används för att ladda in bilder till spelet, samt laddar in de bilder som ska användas i spelet, med hjälp av den innan nämnda funktionen.


Maps
Innehåller klassen Maps som används som mall för att skapa andra maps. Inne i filen finns 
också maps gjorde bestående av rutnät med siffror. Där varje siffra har en sak bunden till sig.


Andra ändringar:

    För att spelet ska vara flyttande har vi valt att göra så metal lådorna går att ta sönder om deras liv går ner till 0 från 3