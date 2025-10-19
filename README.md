# Reseptisovellus
Sovellus, jossa käyttäjät voivat jakaa omia ruokareseptejään.

## Mitä sovelluksessa voi tehdä:
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan reseptejä
* Käyttäjä näkee sovellukseen lisätyt reseptit
* Käyttäjä pystyy etsimään reseptejä hakusanalla
* Käyttäjä pystyy katsomaan omia reseptejöön ja muita käyttäjiä
* Reseptejä voi lajitella kategorioihin (esim. kasvis, helppo, vegaaninen)
* Käyttäjä pystyy antamaan arvostelun ja kommentin resepteille

## Testausohjeet:
1. Lataa projekti tiedostot
2. Asenna kirjastot: pip install flask werkzeug
3. Luo tietokanta: sqlite3 database.db < schema.sql
4. Testaaminen:
   1. Käynnistä sovellus: flask run
   2. Avaa selaimessa: http://localhost:5000
   3. Luo uusi tunnus
   4. Kirjaudu sisään
   5. Lisää reseptejä etusivulla
   6. Kokeile hakutoimintoa
   7. Käy katsomassa toisen käyttäjän reseptejä
   8. Anna arvostelu reseptille
  
