# Reservations app

Sovellus tulee ajaa python 3.10:llä tai uudemmalla.

## Sisällysluettelo
- [Sovelluksen idea](#sovelluksen-idea)
- [Tarkastajalle](#tarkastajalle)
- [Käyttäjäryhmät ja niiden toiminnot](#käyttäjäryhmät-ja-niiden-toiminnot)
    * [Asiakas (kirjautumaton)](#asiakas-kirjautumaton)
    * [Työntekijä (kirjautunut)](#työntekijä-kirjautunut)
    * [Pääkäyttäjä (kirjautunut)](#pääkäyttäjä-kirjautunut)

<a name="sovelluksen-idea"></a>
## Sovelluksen idea
Kampaamon varausjärjestelmä, jossa asiakkaat voivat varata ajan haluamaansa palveluun, haluamaansa toimipisteeseen ja haluamalleen kampaajalle. Kampaamon työntekijät voivat katsella varauksia ja merkitä niitä tehdyiksi.

<a name="tarkastajalle"></a>
## Tarkastajalle
Sovelluksen fly.io osoite: https://reservations.fly.dev/
Sovelluksen pääkäyttäjän tunnukset löytyvät tiedostosta online.txt. Tällä hetkellä nämä avaavat erilaisen näkymän hallintapanelissa ja antavat mahdollisuuden mm. muiden käyttäjien muokkaamiseen. Ethän tiputa adminkäyttäjän roolia. Tällä käyttäjällä ei pääse tuhoamaan sovelluksessa mitään suurempaa vielä tässä vaiheessa, joten siksi tunnukset ovat repositoryssä. Tulevaisuudessa tilanne voi olla toinen.

Osa sovelluksen palvelinpuolen logiikasta puuttuu vielä, katso alla oleva "Ominaisuudet, jotka toteuttamatta osio".
<br>

Suosittelen käymään läpi etusivulta löytyvät "Tee varaus", "Etsi varaus" ja Sijaintimme kohdat.<br>
Etusivun (esim. localhost:5000/) vasemmassa alakulmassa on hienovarainen linkki tekstillä "Henkilökunnalle", jonka takaata löytyy kirjautumissivu, josta pääsee suoraan henkilökunnan työpöydälle käyttämällä online.txt-tiedoston tunnuksia. Täällä on loput ominaisuuksista.
<br>

Sovelluksessa toimivia ominaisuuksia on:
- Varausta asiakkaana tehdessä voi valita palvelun ja toimipaikan (viimeinen lomake ei toimi vielä)
- Sijaintien tarkastelu
- Käyttäjän kirjautuminen, rekisteröityminen ja uloskirjautuminen
- Käyttäjien listaaminen
- Käyttäjän salliminen henkilökunnan työpöydälle ja tämän oikeuden poistaminen
- Käyttäjän roolin vaihtaminen käyttäjästä pääkäyttäjäksi ja toisin päin
- Palveluiden ja toimipaikkojen luominen, listaaminen ja poistaminen (muokkaaminen toteuttamatta)
- Oman käyttäjän tietojen muokkaus
- Varattavien aikojen (näitä asiakkaat voivat varailla sitten) luominen ja listaaminen
- Pelkästään pääkäyttäjälle tarkoitettujen osioiden piilotus työpöydältä, jos kirjaudutaan normaalina käyttäjänä.
<br>

Muistathan, että rekisteröityneet käyttäjät tulee hyväksyä pääkäyttäjän toimesta Käyttäjät välilehdeltä ennen kuin tämä rekisteröitynyt käyttäjä pääsee kirjautumaan sisään.

## Ominaisuudet, jotka toteuttamatta
#### Etusivu
- Varauksen vieminen loppuun, palvelun ja toimipaikan valinta toimii, omien tietojen syöttölomake ei vielä.
- Varauksen etsiminen
- Sijaintimme sivun kortit saman kokoisiksi
- Valitse palvelu kortin napit järkevän näköiseksi (toimi kahdella, ei näköjään kolmella)
##### Varaukset välilehti
- Asiakkaiden tekemien varauksien listaaminen (pelkkä design tehtynä)
- Asiakkaiden varauksien tarkastelynäkymä (pelkkä design tehtynä)
- Asiakkaan varauksen asettaminen suoritetuksi tai poistaminen (pelkkä design tehtynä)

##### Varattavat ajat välilehti
- Luotujen "Varattavien aikojen" poistaminen
- Luonnin yhteydessä tapahtuneiden virheviestien näyttäminen, erityisesti syötteen formatointivirheet

##### Palvelut ja toimipaikat välilehdet
- Estä palvelun tai toimipaikan poistaminen, jos sillä on varattavia aikoja (heittää tällä hetkellä virheen vain)
- Toimipaikkakortit saman korkuisiksi


## Sovelluksen käynnistäminen
1. Siirry projektin juurikansioon `reservations`
2. Asenna tarvittavat riippuvuudet
```shell
python3 -m pip install -r ./requirements.txt
```
3. Käynnistä Flask palvelin
```shell
python3 -m flask run
```

_Kohdan 3. komennon tulisi automaattisesti löytää juurihakemistossa oleva app.py ja käynnistää web-palvelin, mutta jos näin ei tapahdu käytä alla olevaa komentoa._
```shell
python3 -m flask --app app.py run
```

Sovelluksen käynnistäminen edellyttää, että postgres tietokannassa on tables.sql kuvaamat tietokantataulut.
<br>
Tarvittavat environment variablet löytyvät .env-example tiedostosta. Kopioi tämä tiedost .env tiedostoksi ja aseta muuttujiin asianmukainen sisältö.
Ilman asianmukaisia tietokantatauluja ja .env-tiedostoa sisältöineen ei sovellus tule toimimaan.

<a name="käyttäjäryhmät-ja-niiden-toiminnot"></a>
## Käyttäjäryhmät ja niiden toiminnot
Käyttäjäryhmät ovat järjestyksessä pienemmistä oikeuksista suurimpiin oikeuksiin. Suuremman oikeuden käyttäjäryhmä saa kaikkien alempien käyttäjäryhmien oikeudet myös käyttöönsä.

<a name="asiakas-kirjautumaton"></a>
### Asiakas (kirjautumaton)
- Luoda varaus
  - Valitsee toimipisteen, palvelun ja kampaajan
  - Syöttää omat tiedot ja mahdollisesti viestin kampaajalle
- Muokata tekemäänsä varausta
  - Oman varauksen löytää varauksen tunnisteella ja sen luonnin yhteydessä saadulla pin-koodilla.
  - Varauksen omia tietoja voi muokata ja sen voi perua
- Tarkastella verkkosivuilla toimipisteitä

<a name="työntekijä-kirjautunut"></a>
### Työntekijä (kirjautunut)
- Muokata omia käyttäjätietojaan
  - Nimi, sähköpostiosoite
- Tarkastella tulevia varauksia
- Tarkastella yhtä varausta
  - Näkee asiakkaan tarkemmat tiedot ja viestin
  - Voi poistaa tai merkitä varauksen suoritetuksi

<a name="pääkäyttäjä-kirjautunut"></a>
### Pääkäyttäjä (kirjautunut)
- Muokata varattavia aikoja (timeslots)
  - Luo siis vapaat ajat, joita asiakas voi varata sekä määrittelee niille palvelun ja työntekijän
  - Poistaa varattavissa olevia aikoja, joita ei ole vielä varattu
- Muokata käyttäjiä
  - Hyväksyä rekisteröityneet käyttäjät (eli päästää heidät järjestelmään)
  - Muokata käyttäjien käyttäjäroolia (työntekijä/pääkäyttäjä)
  - Poistaa käyttäjiä käytöstä (tiedot jää, mutta käyttäjä ei pääse järjestelmään käsiksi eikä se näy varaussivulla)
- Muokata varattavia palveluita
  - Luoda ja poistaa palveluita (palvelulla on nimi ja hinta)
- Muokata toimipisteitä
  - Luoda, muokata ja poistaa toimipisteitä
    - Toimipisteellä on nimi, osoite ja kuva (URL)