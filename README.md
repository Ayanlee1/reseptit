# Reseptisovellus
Sovellus, jossa käyttäjät voivat jakaa omia ruokareseptejään.

## Tällä hetkellä:
* Käyttäjä pystyy luoman tunnuksen ja kirjautumaan sisään
* Käyttäjä pystyy lisäämään reseptejä
* Käyttäjä näkee sovellukseen lisätyt reseptit
* Käyttäjä pystyy etsimään reseptejä hakusanalla

## Testausohjeet:
1. Lataa projekti tiedostot
2. Asenna kirjastot: pip install flask werkzeug
3. Luo tietokanta: sqlite3 database.db < schema.sql

## Testaaminen:
1. Käynnistä sovellus: flask run
2. Avaa selaimessa osoite: http://localhost:5000
3. Rekisteröi uusi tunnus
4. Kirjaudu sisään
5. Lisää uusi resepti
6. Selaa reseptejä etusivulla
7. Kokeile hakutoimintoa 
