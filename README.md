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
2. Luo tietokanta: sqlite3 database.db < schema.sql
3. Luo virtuaaliympäristö: python3 -m venv venv
4. Aktivoi virtuaaliympäristö: source venv/bin/activate
5. Asenna kirjastot: pip install flask werkzeug
6. Käynnistä sovellus: flask run
7. Avaa selaimessa: http://localhost:5000


## Testaaminen:
1. Luo uusi tunnus
2. Kirjaudu sisään
3. Lisää reseptejä uusi resepti sivulla
4. Kokeile hakutoimintoa
5. Käy katsomassa toisen käyttäjän reseptejä
6. Anna arvostelu reseptille 
  
