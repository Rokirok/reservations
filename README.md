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
Sovelluksessa on jo tehtynä käyttöliittymä, mutta mitään palvelinpuolen logiikkaa ei ole olemassa. Kyseistä käyttöliittymää voi kuitenkin käyttää ja siitä saa hyvän kuvan miltä sovellus visuaalisesti tulee näyttämään sekä sen toiminnalisuuksista. Koodi löytyy kansioista `/templates` ja `/static`
<br>

Suosittelen käymään läpi sisäänkirjautumisesta löytyvät "Tee varaus", "Etsi varaus" ja Sijaintimme kohdat. Napit toimivat tällä hetkellä linkkeinä eteenpäin ja kenttiin ei tarvitse syöttää mitään tietoa.
Etusivun (esim. localhost:5000/) vasemmassa alakulmassa on hienovarainen linkki tekstillä "Henkilökunnalle", jonka takaata löytyy kirjautumissivu, josta pääsee suoraan painamalla kirjaudu nappia henkilökunnan työpöydälle. Täällä on loput ominaisuuksista. Suosittelen käymään nämä paikat läpi, sillä ne toimivat hyvin kuvauksena siitä, mitä sovellus tulee pitämään sisällään.
Kaikki napit ovat tällä hetkellä linkkejä ja johtavat sille sivulle, jolle päädyttäisiin myös lopullisessa sovelluksessa onnistuneen tapahtuman johdosta. Jos jokin nappi ei johda minnekkään niin sen takaa löytyvää käyttöliittymää ei ole suunniteltu. Näitä ei kuitenkaan pitäisi olla kuin ihan muutama.
<br>
Tietyt viimeistelyn kannalta kivat ominaisuudet kuten valitun kohteen korostaminen "dashboardin" sivupanelissa ei ole vielä toiminnassa.


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